import os, shutil
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

KEY = os.environ['FACE_SUBSCRIPTION_KEY']
ENDPOINT = 'https://centralindia.api.cognitive.microsoft.com/'
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
            try:
                u = User.objects.create_user(username=uname,first_name=fname, last_name=lname, email=email, password=passwd)
                u.save()
                login(request, u)
                # create PersonGroup
                PERSON_GROUP_ID = uname.lower()
                face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

               
                # change for album_collection 
                return JsonResponse({"message":"success", "userid":uname})
            except:
                return JsonResponse({"message": "wrong"})


def login_view(request):
    if request.method == "GET":
        return render(request,"login_auth/login.html")

    elif request.method == "POST":
        uname = request.POST["uname"]
        passwd = request.POST["passwd"]
        user = authenticate(request, username=uname, password=passwd)
        if user is not None:
            login(request, user)
            return JsonResponse({"message":"success", "userid":uname})
        elif user is None:
            return JsonResponse({"message": "iep"})

        
@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect("index")

# @login_required(login_url="/login")