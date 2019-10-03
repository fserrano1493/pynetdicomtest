from pydicom.dataset import Dataset

from pynetdicom import AE
from pynetdicom.sop_class import StudyRootQueryRetrieveInformationModelFind

# Initialise the Application Entity
ae = AE()

# Add a requested presentation context
#ae.add_requested_context('1.2.840.10008.5.1.4.1.2.1.1')
ae.add_requested_context(StudyRootQueryRetrieveInformationModelFind)

# Create our Identifier (query) dataset
meta = Dataset()
#meta.MediaStorageSOPClassUID = ds.SOPClassUID
#meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
#meta.ImplementationClassUID = PYNETDICOM_IMPLEMENTATION_UID
#meta.ImplementationVersionName = PYNETDICOM_IMPLEMENTATION_VERSION
meta.TransferSyntaxUID = '1.2.840.10008.1.2'

ds = Dataset()
ds.PatientName = 'CITIZEN^Ramos'
ds.PatientID = ''
ds.SOPInstanceUID = '1.2.3'
ds.SOPClassUID = '1.2.840.10008.5.1.4.1.2.1.1'
#ds.is_implicit_VR
#ds.is_little_endian
#ds.TransferSyntaxUID.file_meta=
ds.file_meta=meta
ds.QueryRetrieveLevel = 'PATIENT'

# Associate with peer AE at IP 127.0.0.1 and port 11112
print("Comienza la asociación")
assoc = ae.associate('medicac.fortiddns.com', 4006)
for cx in assoc.accepted_contexts:
    print('Contextos aceptados: {}, SCP role: {}, SCU role: {}'.format(cx.abstract_syntax, cx.as_scp, cx.as_scu))


for rj in assoc.rejected_contexts:
    print('Contextos Rechazados: Context: {}, SCP role: {}, SCU role: {}'.format(rj.abstract_syntax, rj.as_scp, rj.as_scu))

if assoc.is_established:
    # Use the C-FIND service to send the identifier
    responses = assoc.send_c_find(ds, StudyRootQueryRetrieveInformationModelFind)

    for (status, identifier) in responses:
        if status:
            print('C-FIND query status: 0x{0:04x}'.format(status.Status))

            # If the status is 'Pending' then identifier is the C-FIND response
            if status.Status in (0xFF00, 0xFF01):
                print(identifier)
        else:
            print('Connection timed out, was aborted or received invalid response')

     # Release the association
    assoc.release()
else:
    print('Error: Association rejected, aborted or never connected')

# from pydicom.dataset import Dataset
# from pynetdicom import (
# 	AE, build_context, build_role, StoragePresentationContexts,
# 	PYNETDICOM_IMPLEMENTATION_UID,
# 	PYNETDICOM_IMPLEMENTATION_VERSION)
# from pynetdicom.pdu_primitives import SCP_SCU_RoleSelectionNegotiation
# from pynetdicom.sop_class import (
# 	PatientRootQueryRetrieveInformationModelGet, PatientRootQueryRetrieveInformationModelMove,
# 	CTImageStorage, DigitalMammographyXRayImagePresentationStorage)
# import logging

# LOGGER = logging.getLogger('pynetdicom')
# LOGGER.setLevel(logging.DEBUG)

# ae = AE(ae_title='TITLE_SCU')

# ae.add_requested_context(DigitalMammographyXRayImagePresentationStorage)
# ae.add_requested_context(PatientRootQueryRetrieveInformationModelGet)


# # Patient Root Query/Retrieve Information Model – GET  ... Digital Mammography X-Ray Image Storage – for Presentation
# uids = ['1.2.840.10008.5.1.4.1.2.1.3', '1.2.840.10008.5.1.4.1.1.1.2','1.2.840.10008.5.1.4.1.2.2.1']
# ext_neg = []
# for uid in uids:
#     tmp = SCP_SCU_RoleSelectionNegotiation()
#     tmp.sop_class_uid = uid
#     tmp.scu_role = False
#     tmp.scp_role = True

#     ext_neg.append(tmp)
#     ae.add_supported_context(uid)
	

# def on_c_store(ds, context, info):

# 	print("ON_C_STORE")
	
# 	meta = Dataset()
# 	meta.MediaStorageSOPClassUID = ds.SOPClassUID
# 	meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
# 	meta.ImplementationClassUID = PYNETDICOM_IMPLEMENTATION_UID
# 	meta.ImplementationVersionName = PYNETDICOM_IMPLEMENTATION_VERSION
# 	meta.TransferSyntaxUID = context.transfer_syntax

# 	ds.file_meta = meta
# 	ds.is_little_endian = context.transfer_syntax.is_little_endian
# 	ds.is_implicit_VR = context.transfer_syntax.is_implicit_VR
# 	ds.save_as(ds.SOPInstanceUID, write_like_original=False)

# 	return 0x0000

# ae.on_c_store = on_c_store

# ds = Dataset()
# ds.QueryRetrieveLevel = ''
# ds.PatientID = '633437'
# ds.StudyInstanceUID = ''
# ds.SeriesInstanceUID = ''



# assoc = ae.associate('medicac.fortiddns.com', 4006, ae_title=b'Server', ext_neg=ext_neg)


# for cx in assoc.accepted_contexts:
#     print('Context: {}, SCP role: {}, SCU role: {}'.format(cx.abstract_syntax, cx.as_scp, cx.as_scu))

# if assoc.is_established:
# 	responses = assoc.send_c_get(ds,'Patient Root Query/Retrieve Information Model – GET')
	
# 	for (status, identifier) in responses:
# 		if status:
# 			print('C-GET query status: 0x{0:04x}'.format(status.Status))
# 			if status.Status in (0xFF00, 0xFF01):
# 				print(identifier)
# 		else:
# 			print('Connection timed out, was aborted or received invalid response')
# 	assoc.release()
# else:
# 	print('Association rejected, aborted or never connected')