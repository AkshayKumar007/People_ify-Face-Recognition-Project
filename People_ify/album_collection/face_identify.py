# <snippet_imports>
import asyncio, io, glob, os, sys, time, uuid, requests, shutil, random
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
from django.conf import settings
from .models import FolderName, Person_Group, Person_Group_Person

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
	# PERSON_GROUP_ID = PERSON_GROUP_ID.lower()
	print(PERSON_GROUP_ID)
	# i=0
	d={}

	test_folder = settings.BASE_DIR + "/media/"
	sample_images = [f for f in os.listdir(test_folder) if os.path.isfile(os.path.join(test_folder, f))]
	image_paths = []
	for j in sample_images:
		x = test_folder + j
		image_paths.append(x)

	for group_photo in image_paths:
		image = open(group_photo, 'r+b')

		# Detect faces
		face_ids = []
		faces = face_client.face.detect_with_stream(image)
		# time.sleep(60)
		for face in faces:
		    face_ids.append(face.face_id)
	
		results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
		
		if not results:
			miscdirc = settings.BASE_DIR + "/static/" + PERSON_GROUP_ID + "/" + "Miscellaneous"
			os.makedirs(miscdirc)
			shutil.move(group_photo, miscdirc)
			# continue
			mis = Person_Group_Person(pg_id=PERSON_GROUP_ID, pgp_name="miscellaneous", person_id="0000000")  # change
			mis.save()

		for person in results:
			if len(person.candidates)>0: #Face has been matched

				my_image = open(group_photo, 'r+b')
				face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, person.candidates[0].person_id, my_image)

				p_name = Person_Group_Person.objects.get(person_id=person.candidates[0].person_id)  # change
				f_name = FolderName.objects.get(pgp_id=p_name)
				# per = Person_Group_Person(pg_id=PERSON_GROUP_ID, pgp_name="", person_id=person.candidates[0].person_id)  

				#print('The person belongs to {}'.format(d[person.candidates[0].person_id]))
				userdirc = settings.BASE_DIR + "/static/" + PERSON_GROUP_ID + "/" + f_name.folder_name
				shutil.move(group_photo, userdirc)
			else: #Face not matched so create a new person group person
				i = int()
				while True:
					try:
						i = random.randint(0, 1000)
						x = FolderName.objects.get(folder_name="New_FACE"+str(i))
					except:
						break
				#creating a new person group person
				my_image_2 = open(group_photo, 'r+b')
				new_face = face_client.person_group_person.create(PERSON_GROUP_ID, "New_FACE"+str(i))

				p = Person_Group.objects.get(pg_name=PERSON_GROUP_ID)
				per = Person_Group_Person(pg_id=p, pgp_name="New_FACE"+str(i), person_id=new_face.person_id)  # change
				per.save()
				try:
					face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, new_face.person_id, my_image_2)
				except:
					pass
				userdirc = settings.BASE_DIR + "/static/" + PERSON_GROUP_ID + "/" + "New_FACE"+str(i)
				os.makedirs(userdirc)

				fname = FolderName(pg_id=per.pg_id, pgp_id=per, folder_name="New_FACE"+str(i), folder_path=userdirc)  # change
				fname.save()

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
	# sudo -u postgres psql postgres

	
if __name__ == "__main__":
	main()
