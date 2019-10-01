from pydicom.dataset import Dataset

from pynetdicom import AE
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelMove

# Initialise the Application Entity
ae = AE()

# Add a requested presentation context
ae.add_requested_context(PatientRootQueryRetrieveInformationModelMove)

# Create out identifier (query) dataset
ds = Dataset()
ds.QueryRetrieveLevel = 'SERIES'
# Unique key for PATIENT level
ds.PatientID = '8430'
# Unique key for STUDY level
ds.StudyInstanceUID = '1.2.3'
# Unique key for SERIES level
ds.SeriesInstanceUID = '1.2.3.4'

# Associate with peer AE at IP 127.0.0.1 and port 11112
assoc = ae.associate('medicac.fortiddns.com', 4006)

if assoc.is_established:
    # Use the C-MOVE service to send the identifier
    responses = assoc.send_c_move(ds, b'STORE_SCP', PatientRootQueryRetrieveInformationModelMove)

    for (status, identifier) in responses:
        if status:
            print('C-MOVE query status: 0x{0:04x}'.format(status.Status))

            # If the status is 'Pending' then the identifier is the C-MOVE response
            if status.Status in (0xFF00, 0xFF01):
                print(identifier)
        else:
            print('Connection timed out, was aborted or received invalid response')

    # Release the association
    assoc.release()
else:
    print('Association rejected, aborted or never connected')