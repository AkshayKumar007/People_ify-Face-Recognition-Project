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
        # get a "list" of all folders that are there inside picture/username excluding sample

        context = {
            "uname": userid
        }

        return render(request, "album_collection/collection.html", context)
    
        
# export DJANGO_SETTINGS_MODULE=People_ify.settings
@login_required(login_url="/login")
def view_folder(request, folder_id):
    if request.method == "GET":

        return render(request, )
    pass

@login_required(login_url="/login")
def upload(request):
    pass
