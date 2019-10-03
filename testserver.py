from pydicom.dataset import Dataset

from pynetdicom import (
    AE, evt,
    StoragePresentationContexts,
    PYNETDICOM_IMPLEMENTATION_UID,
    PYNETDICOM_IMPLEMENTATION_VERSION
    
)
from pynetdicom.sop_class import StudyRootQueryRetrieveInformationModelFind
from pynetdicom.sop_class import (_BASIC_WORKLIST_CLASSES,_VERIFICATION_CLASSES,_PROTOCOL_APPROVAL_CLASSES,_QR_CLASSES)

# Implement a handler evt.EVT_C_STORE
def handle_store(event):
    """Handle a C-STORE request event."""
    # Decode the C-STORE request's *Data Set* parameter to a pydicom Dataset
    ds = event.dataset

    # Add the File Meta Information
    ds.file_meta = event.file_meta

    # Save the dataset using the SOP Instance UID as the filename
    ds.save_as(ds.SOPInstanceUID, write_like_original=False)

    # Return a 'Success' status
    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]

# Initialise the Application Entity
ae = AE()

# Add the supported presentation contexts
ae.supported_contexts = StoragePresentationContexts
ae.add_requested_context = StudyRootQueryRetrieveInformationModelFind
for wk in _BASIC_WORKLIST_CLASSES:
    ae.add_requested_context = wk

for vf in _VERIFICATION_CLASSES:
    ae.add_requested_context = vf

for pa in _PROTOCOL_APPROVAL_CLASSES:
    ae.add_requested_context = pa

for qr in _QR_CLASSES:
    ae.add_requested_context = qr


# Start listening for incoming association requests
print("servidor en linea")
ae.shutdown()
ae.start_server(('127.0.0.1', 11112), evt_handlers=handlers)

