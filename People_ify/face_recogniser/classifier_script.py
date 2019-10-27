'''
code to upload images to azure-cognitiveservices-api and group them
'''

import asyncio, io, glob, os, sys, time, uuid, requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw #  Pillow
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType

# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = os.environ['FACE_SUBSCRIPTION_KEY']
# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = os.environ['FACE_ENDPOINT']
# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def main():
    # Detect a face in an image that contains a single face
    # basically code to check if there is a face, if not  
    single_face_image_url = 'https://www.biography.com/.image/t_share/MTQ1MzAyNzYzOTgxNTE0NTEz/john-f-kennedy---mini-biography.jpg'
    single_image_name = os.path.basename(single_face_image_url)
    detected_faces = face_client.face.detect_with_url(url=single_face_image_url)  #  extracing name of file from url
    if not detected_faces:
        raise Exception('No face detected from image {}'.format(single_image_name))
        #  add code to sort in 'objects/ no human' folder


    # Display the detected 'face ID' in the first single-face image.
    # Face IDs are used for comparison to faces (their IDs) detected in other images.
    print('Detected face ID from', single_image_name, ':')
    for face in detected_faces: 
        print (face.face_id)
    print()
    # Save this ID for use in Find Similar
    first_image_face_ID = detected_faces[0].face_id




if "__name__" == "__main__":
    main()