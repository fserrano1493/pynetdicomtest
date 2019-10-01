import os

from pydicom import dcmread
from pydicom.dataset import Dataset

from pynetdicom import AE, StoragePresentationContexts, evt
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelMove

from pynetdicom import AE

ae = AE(ae_title=b'Server')
    # Verification SOP Class has a UID of 1.2.840.10008.1.1
    #   we can use the UID string directly when requesting the presentation
    #   contexts we want to use in the association
ae.add_requested_context('1.2.840.10008.1.1')

    # Associate with a peer DICOM AE
assoc = ae.associate('medicac.fortiddns.com', 4006)

if assoc.is_established:
        # Send a DIMSE C-ECHO request to the peer
        # `status` is a pydicom Dataset object with (at a minimum) a
        #   (0000,0900) Status element
        # If the peer hasn't accepted the requested context then this
        #   will raise a RuntimeError exception
    status = assoc.send_c_echo()

        # Output the response from the peer
    if status:
        print('C-ECHO Response: 0x{0:04x}'.format(status.Status))

        # Release the association
    assoc.release()