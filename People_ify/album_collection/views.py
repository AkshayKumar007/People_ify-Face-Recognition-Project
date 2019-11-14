from . import face_identify
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from album_collection.models import Person_Group, Person_Group_Person, FolderName, Review

# Create your views here.

@login_required(login_url="/login")
def homepage(request, userid):
    if request.method == "GET":
        # to be done by Kanishk
        # 1. get a "list" of all folder_names that are there inside picture/username excluding sample(be careful with paths)
        # 2. add that list to context below so that I can render it on webpage
        folder_list = []
        context = {
            "uname": userid,
            "folders" : folder_list

        }
        return render(request, "album_collection/collection.html", context)
    
        
# export DJANGO_SETTINGS_MODULE=People_ify.settings
@login_required(login_url="/login")
def view_folder(request, folder_name):
    if request.method == "GET":
        folder_name = FolderName.objects.filter(folder_name = folder_name)
        return render(request, )
    pass

@login_required(login_url="/login")
def upload(request):
    # to be done by Kanishk
    # 1. everytime you create a pgp in face_identify, make it's entry in FolderName and all other tables
    # 2. call face_identify passing in PERSON_GROUP_ID = username.lower() as parameter
    pass
