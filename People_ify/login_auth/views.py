import os, shutil, sys, time
# azure
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatus

# django
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.conf import settings
from album_collection.models import Person_Group


KEY = os.environ['FACE_SUBSCRIPTION_KEY']
ENDPOINT = os.environ['FACE_ENDPOINT']
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


# Create your views here.
def index(request):
    # css_url = url_for('static', filename='js/main.js')
    return render(request,"login_auth/index.html")  # index.html will be welcome screen


def register_view(request):
    if request.method == "GET":
        return render(request,"login_auth/register.html")

    elif request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        uname = request.POST["uname"]  # username shall always be lowercase 
        passwd = request.POST["passwd"] 
        try:
            res1 = User.objects.get(email=email)
        except:
            res1 = None
        try:
            res2 = User.objects.get(username=uname)
        except:
            res2 = None
        if res1 is not None:
            return JsonResponse({"message": "no_email"}) 
        elif res2 is not None:
            return JsonResponse({"message": "no_uname"})
        else:
            # try:
            u = User.objects.create_user(username=uname,first_name=fname, last_name=lname, email=email, password=passwd)
            u.save()
            login(request, u)
            # create PersonGroup
            PERSON_GROUP_ID = uname.lower()
            face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)
            # base = os.path.abspath(os.path.dirname(__name__))  # point to Project Directory People_ify
            base = settings.BASE_DIR
            userdirc = base + "/static/" + uname.lower()
            os.makedirs(userdirc)  # create a seperate directory for each user
            os.mkdir(userdirc+"/sample")  # create a sample directory for instantiation
            
            shutil.copy(settings.BASE_DIR + '/static/perfect-face.jpg', userdirc+"/sample")
            sample = face_client.person_group_person.create(PERSON_GROUP_ID, "Sample")         
            w = open(userdirc+"/sample/perfect-face.jpg", 'r+b')
            face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, sample.person_id, w)
            face_client.person_group.train(PERSON_GROUP_ID)
            while (True):
                training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
                #print("Training status: {}.".format(training_status.status))
                if (training_status.status is TrainingStatusType.succeeded):
                    print((request.user.username).lower())  # error checking 
                    break
                elif (training_status.status is TrainingStatusType.failed):
                    sys.exit('Training the person group has failed.')
                time.sleep(5)
            new_user = Person_Group.objects.create(pg_name=uname.lower())  # create an entry in table
            new_user.save()
            # change for album_collection 
            return JsonResponse({"message":"success", "userid":uname})
            # except:
            #     return JsonResponse({"message": "wrong"})


def login_view(request):
    if request.method == "GET":
        return render(request,"login_auth/login.html")

    elif request.method == "POST":
        uname = request.POST["uname"]
        passwd = request.POST["passwd"]
        user = authenticate(request, username=uname, password=passwd)
        if user is not None:
            PERSON_GROUP_ID = uname.lower()
            login(request, user)
            return JsonResponse({"message":"success", "userid":uname})
        elif user is None:
            return JsonResponse({"message": "iep"})

        
@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect("index")

# @login_required(login_url="/login")