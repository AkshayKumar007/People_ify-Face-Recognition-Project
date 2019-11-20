# <snippet_imports>
import asyncio, io, glob, os, sys, time, uuid, requests, shutil
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
from django.conf import settings

KEY = os.environ['FACE_SUBSCRIPTION_KEY']

ENDPOINT = 'https://centralindia.api.cognitive.microsoft.com/'

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
# </snippet_auth>

#print("started")

# <snippet_persongroup_create>

# Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
#print('Person group:', PERSON_GROUP_ID)
# PERSON_GROUP_ID = 'my-unique-person-group-9'
# face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

def main(PERSON_GROUP_ID):
	# sample_images = [file for file in glob.glob('*.jpg') if file.startswith("sample_image")]
	# media = os.path.join(os.path.dirname(os.path.realpath(__file__))) + "/uploads"
	# sample_images = [f for f in os.listdir(media) if os.path.isfile(os.path.join(media, f))]
	# sample = face_client.person_group_person.create(PERSON_GROUP_ID, "Sample")
	# for img in sample_images:
	# 	w = open(img, 'r+b')
	# 	face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, sample.person_id, w)


	# #print('Training the person group...')
	# # Train the person group
	# face_client.person_group.train(PERSON_GROUP_ID)

	# while (True):
	#     training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
	#     #print("Training status: {}.".format(training_status.status))
	#     if (training_status.status is TrainingStatusType.succeeded):
	#         break
	#     elif (training_status.status is TrainingStatusType.failed):
	#         sys.exit('Training the person group has failed.')
	#     time.sleep(5)
	# # </snippet_persongroup_train>

	# # <snippet_identify_testimage>

	# # Reference image for testing against
	PERSON_GROUP_ID = PERSON_GROUP_ID.lower()
	print(PERSON_GROUP_ID)
	i=0
	d={}

	# test_folder=os.listdir(os.path.join(os.getcwd(),'testfolder'))
	# base = settings.BASE_DIR
	test_folder = settings.BASE_DIR + "/media/"
	sample_images = [f for f in os.listdir(test_folder) if os.path.isfile(os.path.join(test_folder, f))]
	image_paths = []
	for j in sample_images:
		x = test_folder + "/" + j
		image_paths.append(x)

	for group_photo in image_paths:
		image = open(group_photo, 'r+b')

		# Detect faces
		face_ids = []
		faces = face_client.face.detect_with_stream(image)
		# time.sleep(60)
		for face in faces:
		    face_ids.append(face.face_id)
		# </snippet_identify_testimage>

		# <snippet_identify>
		# Identify faces
		results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
		#print('Identifying faces::')
		if not results:
		    #print('No person identified in the person group for faces from the {}.'.format(os.path.basename(image.name)))
		    continue

		for person in results:
			if len(person.candidates)>0: #Face has been matched
				#print('Person for face ID {} is identified in {} with a confidence of {}.'.format(person.face_id, os.path.basename(image.name), person.candidates[0].confidence))

				my_image = open(group_photo, 'r+b')
				face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, person.candidates[0].person_id, my_image)

				#print('The person belongs to {}'.format(d[person.candidates[0].person_id]))
				userdirc = settings.BASE_DIR + "/pictures/" + PERSON_GROUP_ID + "/" + d[person.candidates[0].person_id]
				shutil.move(group_photo, userdirc)
			else: #Face not matched so create a new person group person
				#print("Face cannot be matched so I am creating a new person group person")
				i+=1
				#creating a new person group person
				my_image_2 = open(group_photo, 'r+b')
				new_face = face_client.person_group_person.create(PERSON_GROUP_ID, "New_FACE"+str(i))
				face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, new_face.person_id, my_image_2)
				d[new_face.person_id]='New_FACE'+str(i)

				# if not os.path.exists('New_FACE'+str(i)):
				userdirc = settings.BASE_DIR + "/pictures/" + PERSON_GROUP_ID + "/" + d[new_face.person_id]
				os.makedirs(userdirc)
				# os.mkdir(userdirc)
				shutil.move(group_photo, userdirc)





			#print('Training the person group AGAIN...')

				# Train the person group AGAIN
			face_client.person_group.train(PERSON_GROUP_ID)

			while (True):
				training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
				#print("Training status: {}.".format(training_status.status))
				if (training_status.status is TrainingStatusType.succeeded):
					break
				elif (training_status.status is TrainingStatusType.failed):
					sys.exit('Training the person group has failed.')
				time.sleep(5)
		image.close()
		#os.remove(group_photo)

	# </snippet_identify>


	# <snippet_deletegroup>
	# Delete the main person group.
	face_client.person_group.delete(person_group_id=PERSON_GROUP_ID)
	#print("Deleted the person group {} from the source location.".format(PERSON_GROUP_ID))
	# </snippet_deletegroup>

	#print("completed")
if __name__ == "__main__":
	main()