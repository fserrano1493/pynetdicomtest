from pydicom.dataset import Dataset

from pynetdicom import (AE, evt, build_role,
    PYNETDICOM_IMPLEMENTATION_UID,
    PYNETDICOM_IMPLEMENTATION_VERSION)
from pynetdicom.sop_class import CTImageStorage

# Initialise the Application Entity
ae = AE()

# Add a requested presentation context
ae.add_requested_context(CTImageStorage)


# Read in our DICOM CT dataset
meta = Dataset()
#meta.MediaStorageSOPClassUID = ds.SOPClassUID
#meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
#meta.ImplementationClassUID = PYNETDICOM_IMPLEMENTATION_UID
#meta.ImplementationVersionName = PYNETDICOM_IMPLEMENTATION_VERSION
meta.TransferSyntaxUID = '1.2.840.10008.1.2'

ds = Dataset()
ds.PatientName = ''
ds.PatientID = '8435'
ds.SOPInstanceUID = '1.2.3'
ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
ds.SeriesInstanceUID = '1.2.3.4'
ds.StudyInstanceUID = '1.2.3'
#ds.is_implicit_VR
#ds.is_little_endian
#ds.TransferSyntaxUID.file_meta=
ds.file_meta=meta
ds.QueryRetrieveLevel = 'SERIE'


# Associate with peer AE at IP 127.0.0.1 and port 11112
assoc = ae.associate('medicac.fortiddns.com', 4006)

if assoc.is_established:
    # Use the C-STORE service to send the dataset
    # returns the response status as a pydicom Dataset
    status = assoc.send_c_store(ds)

    # Check the status of the storage request
    if status:
        # If the storage request succeeded this will be 0x0000
        print('C-STORE request status: 0x{0:04x}'.format(status.Status))
        for a in status.keys():
            print(status.get_item(a))
           
    else:
        print('Connection timed out, was aborted or received invalid response')

    # Release the association
    assoc.release()
else:
    print('Association rejected, aborted or never connected')

   