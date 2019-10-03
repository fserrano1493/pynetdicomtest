import os

from pydicom import dcmread
from pydicom.dataset import Dataset

from pynetdicom import AE, StoragePresentationContexts, evt
from pynetdicom import (
    build_role,
    PYNETDICOM_IMPLEMENTATION_UID,
    PYNETDICOM_IMPLEMENTATION_VERSION
)

from pynetdicom.sop_class import (
    StudyRootQueryRetrieveInformationModelGet,
    CTImageStorage
)

def handle_store(event):
    """Handle a C-STORE request event."""
    ds = event.dataset
    context = event.context

    # Add the DICOM File Meta Information
    meta = Dataset()
    meta.MediaStorageSOPClassUID = ds.SOPClassUID
    meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
    meta.ImplementationClassUID = PYNETDICOM_IMPLEMENTATION_UID
    meta.ImplementationVersionName = PYNETDICOM_IMPLEMENTATION_VERSION
    meta.TransferSyntaxUID = '1.2.840.10008.1.2'

    # Add the file meta to the dataset
    ds.file_meta = meta

    # Set the transfer syntax attributes of the dataset
    ds.is_little_endian = context.transfer_syntax.is_little_endian
    ds.is_implicit_VR = context.transfer_syntax.is_implicit_VR

    # Save the dataset using the SOP Instance UID as the filename
    ds.save_as(ds.SOPInstanceUID, write_like_original=False)

    # Return a 'Success' status
    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]

ae = AE()

ae.add_requested_context(StudyRootQueryRetrieveInformationModelGet)
# Add the requested presentation context (Storage SCP)
ae.add_requested_context(CTImageStorage)

# Create an SCP/SCU Role Selection Negotiation item for CT Image Storage
role = build_role(CTImageStorage, scp_role=True)

# Create our Identifier (query) dataset
# We need to supply a Unique Key Attribute for each level above the
#   Query/Retrieve level
ds = Dataset()
ds.QueryRetrieveLevel = 'SERIES'
# Unique key for PATIENT level
ds.PatientID = '8435'
# Unique key for STUDY level
ds.StudyInstanceUID = '1.2.3'
# Unique key for SERIES level
ds.SeriesInstanceUID = '1.2.3.4'
ds.SOPInstanceUID = '1.2.3'
ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.2'

# Associate with peer AE at IP 127.0.0.1 and port 11112
assoc = ae.associate('medicac.fortiddns.com', 4006, ext_neg=[role], evt_handlers=handlers)

if assoc.is_established:
    # Use the C-GET service to send the identifier
    responses = assoc.send_c_get(ds, StudyRootQueryRetrieveInformationModelGet)

    for (status, identifier) in responses:
        if status:
            print('C-GET query status: 0x{0:04x}'.format(status.Status))

            # If the status is 'Pending' then `identifier` is the C-GET response
            if status.Status in (0xFF00, 0xFF01):
                print(identifier)
        else:
            print('Connection timed out, was aborted or received invalid response')

    # Release the association
    assoc.release()
else:
    print('Association rejected, aborted or never connected')



# Implement the handler for evt.EVT_C_GET
def handle_get(event):
    """Handle a C-GET request event."""
    ds = event.identifier
    if 'QueryRetrieveLevel' not in ds:
        # Failure
        yield 0xC000, None
        return

    # Import stored SOP Instances
    instances = []
    matching = []
    fdir = 'C:/wamp64/'
    for fpath in os.listdir(fdir):
        instances.append(dcmread(os.path.join(fdir, fpath)))

    if ds.QueryRetrieveLevel == 'PATIENT':
        if 'PatientID' in ds:
            matching = [
                inst for inst in instances if inst.PatientID == ds.PatientID
            ]

        # Skip the other possible attributes...

    # Skip the other QR levels...

    # Yield the total number of C-STORE sub-operations required
    yield len(instances)

    # Yield the matching instances
    for instance in matching:
        # Check if C-CANCEL has been received
        if event.is_cancelled:
            yield (0xFE00, None)
            return

        # Pending
        yield (0xFF00, instance)

handlers = [(evt.EVT_C_GET), handle_get]

# Create application entity
ae = AE()

# Add the supported presentation contexts (Storage SCU)
ae.supported_contexts = StoragePresentationContexts

# Accept the association requestor's proposed SCP role in the
#   SCP/SCU Role Selection Negotiation items
for cx in ae.supported_contexts:
    cx.scp_role = True
    cx.scu_role = False

# Add a supported presentation context (QR Get SCP)
ae.add_supported_context(StudyRootQueryRetrieveInformationModelGet)

# Start listening for incoming association requests
ae.start_server(('127.0.0.1', 11112))