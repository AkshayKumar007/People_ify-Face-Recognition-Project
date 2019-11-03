# <snippet_imports>
import asyncio, io, glob, os, sys, time, uuid, requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
import shutil
# </snippet_imports>

'''
Face Quickstart
Examples include:
    - Detect Faces: detects faces in an image. 
    - Find Similar: finds a similar face in an image using ID from Detect Faces. 
    - Verify: compares two images to check if they are the same person or not.
    - Person Group: creates a person group and uses it to identify faces in other images. 
    - Large Person Group: similar to person group, but with different API calls to handle scale.

    - Face List: creates a list of single-faced images, then gets data from list.
    - Large Face List: creates a large list for single-faced images, trains it, then gets data.

    - Snapshot: copies a person group from one region to another, or from one Azure subscription to another.
Prerequisites:
    - Python 3+
    - Install Face SDK: pip install azure-cognitiveservices-vision-face
    - Sample images (download and include in your local root folder):
      https://github.com/Azure-Samples/cognitive-services-sample-data-files/tree/master/Face/images
How to run:
    - Run from command line or an IDE
    - If the Person Group or Large Person Group (or Face List / Large Face List) examples get 
      interrupted after creation, be sure to delete your created person group (lists) from the API, 
      as you cannot create a new one with the same name. Use 'Person group - List' to check them all, 
      and 'Person Group - Delete' to remove one. The examples have a delete function in them, but at the end.
      Person Group API: https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395244 
      Face List API: https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f3039524d
References: 
    - Documentation: https://docs.microsoft.com/en-us/azure/cognitive-services/face/
    - SDK: https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-vision-face/azure.cognitiveservices.vision.face?view=azure-python
    - All Face APIs: https://docs.microsoft.com/en-us/azure/cognitive-services/face/APIReference
'''

# <snippet_subvars>
# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = os.environ['FACE_SUBSCRIPTION_KEY']

# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = 'https://centralindia.api.cognitive.microsoft.com/'
# </snippet_subvars>

# <snippet_persongroupvars>
# Used in the Person Group Operations,  Snapshot Operations, and Delete Person Group examples.
# You can call list_person_groups to print a list of preexisting PersonGroups.
# SOURCE_PERSON_GROUP_ID should be all lowercase and alphanumeric. For example, 'mygroupname' (dashes are OK).
PERSON_GROUP_ID = 'my-unique-person-group'

'''
Authenticate
All examples use the same client, except for Snapshot Operations.
'''
# <snippet_auth>
# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
# </snippet_auth>
'''
END - Authenticate
'''


'''
Create/Train/Detect/Identify Person Group 
This example creates a Person Group, then trains it. It can then be used to detect and identify faces in other group images.
'''
print('-----------------------------')
print() 
print('PERSON GROUP OPERATIONS')
print() 
# <snippet_persongroup_create>
''' 
Create the PersonGroup
'''
# Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
print('Person group:', PERSON_GROUP_ID)
face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)





sample_images = [file for file in glob.glob('*.jpg') if file.startswith("sample_image")]

sample = face_client.person_group_person.create(PERSON_GROUP_ID, "Sample")
for img in sample_images:
	w = open(img, 'r+b')
	face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, sample.person_id, w)

print()
print('Training the person group...')
# Train the person group
face_client.person_group.train(PERSON_GROUP_ID)

while (True):
    training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
    print("Training status: {}.".format(training_status.status))
    print()
    if (training_status.status is TrainingStatusType.succeeded):
        break
    elif (training_status.status is TrainingStatusType.failed):
        sys.exit('Training the person group has failed.')
    time.sleep(5)
# </snippet_persongroup_train>

# <snippet_identify_testimage>
'''








#Testing starts
Identify a face against a defined PersonGroup
'''
# Reference image for testing against
i=0
d={}

test_folder=os.listdir(os.path.join(os.getcwd(),'testfolder'))

for group_photo in test_folder:
	image = open(os.path.join(os.getcwd(),'testfolder',group_photo), 'r+b')
	
	# Detect faces
	face_ids = []
	faces = face_client.face.detect_with_stream(image)
	for face in faces:
	    face_ids.append(face.face_id)
	# </snippet_identify_testimage>

	# <snippet_identify>
	# Identify faces
	results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
	print('Identifying faces::')
	if not results:
	    print('No person identified in the person group for faces from the {}.'.format(os.path.basename(image.name)))
	    continue

	for person in results:
		if len(person.candidates)>0: #Face has been matched
			print('Person for face ID {} is identified in {} with a confidence of {}.'.format(person.face_id, os.path.basename(image.name), person.candidates[0].confidence))
			
			my_image = open(os.path.join(os.getcwd(),'testfolder',group_photo), 'r+b')
			face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, person.candidates[0].person_id, my_image)

			print('The person belongs to {}'.format(d[person.candidates[0].person_id]))
			shutil.copy(os.path.join(os.getcwd(),'testfolder',group_photo) , os.path.join(os.getcwd(),d[person.candidates[0].person_id],group_photo))
		else: #Face not matched so create a new person group person
			print("Face cannot be matched so I am creating a new person group person")
			i+=1
			
			#creating a new person group person
			my_image_2 = open(os.path.join(os.getcwd(),'testfolder',group_photo), 'r+b')
			new_face = face_client.person_group_person.create(PERSON_GROUP_ID, "New_FACE"+str(i))
			face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, new_face.person_id, my_image_2)
			d[new_face.person_id]='New_FACE'+str(i)
			
			if not os.path.exists('New_FACE'+str(i)):
				os.mkdir('New_FACE'+str(i))
			shutil.copy(os.path.join(os.getcwd(),'testfolder',group_photo) , os.path.join(os.getcwd(),'New_FACE'+str(i),group_photo))
			



		
		print('Training the person group AGAIN...')
			
			# Train the person group AGAIN
		face_client.person_group.train(PERSON_GROUP_ID)

		while (True):
			training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
			print("Training status: {}.".format(training_status.status))
			print()
			if (training_status.status is TrainingStatusType.succeeded):
				break
			elif (training_status.status is TrainingStatusType.failed):
				sys.exit('Training the person group has failed.')
			time.sleep(5)
	image.close()
	#os.remove(group_photo)

# </snippet_identify>
'''
END - Create/Train/Detect/Identify Person Group example
'''




'''
Delete Person Group
For testing purposes, delete the person group made in the Person Group Operations, 
and the target person group from the Snapshot Operations (uses a different client).
List the person groups in your account through the online testing console to check:
https://westus2.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395248
'''
print('-----------------------------')
print() 
print('DELETE PERSON GROUP')
print() 



# <snippet_deletegroup>
# Delete the main person group.
face_client.person_group.delete(person_group_id=PERSON_GROUP_ID)
print("Deleted the person group {} from the source location.".format(PERSON_GROUP_ID))
print()
# </snippet_deletegroup>


print()
print('-----------------------------')
print()
print('End of quickstart.')
