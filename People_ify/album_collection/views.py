import os
from . import face_identify
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from album_collection.models import Person_Group, Person_Group_Person, FolderName, Review
from django.conf import settings
# Create your views here.

@login_required(login_url="/login")
def homepage(request, userid):
    if request.method == "GET":
        # to be done by Kanishk
        # 1. get a "list" of all folder_names that are there inside picture/username excluding sample(be careful with paths)
        # 2. add that list to context below so that I can render it on webpage
        folder_list=[]
        path = settings.BASE_DIR + "/pictures/" + userid  # may need to change
        folder_list = os.listdir(path)
        
        context = {
            "uname": userid,
            "folders" : folder_list
        }
    return render(request, "album_collection/collection.html", context)
    
        
@login_required(login_url="/login")
def view_folder(request, folder_name):
    if request.method == "GET":
        folder = FolderName.objects.get(folder_name = folder_name)
        print(type(folder))
        folder_path = folder.folder_path
        images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        image_path = []
        for i in images:
            x = folder_path + "/" + i
            image_path.append(x)
        context = {
            "images" : image_path,
        }
        return render(request, "folder_view.html", context)


@login_required(login_url="/login")
def upload(request, userid):
    # to be done by Kanishk
    # 1. everytime you create a pgp in face_identify, make it's entry in FolderName and all other tables
    # 2. see media upload documentation in django before proceeding
    # 3. call face_identify passing in PERSON_GROUP_ID = (requset.user.username).lower() as parameter
    if request.method == "GET":
        return render(request, 'album_collection/upload.html')

    elif request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        print((request.user.username).lower())
        face_identify.main((request.user.username).lower())  # run function after image is uploaded
        return redirect("homepage", permanent=True)
        
        # return render(request, 'core/simple_upload.html', {
        #     'uploaded_file_url': uploaded_file_url
        # })
    
# c5229c3363cb4d659aea93939677eaa1
# https://centralindia.api.cognitive.microsoft.com/