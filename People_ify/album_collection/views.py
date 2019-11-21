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
        folder_list=[]
        path = settings.BASE_DIR + "/static/" + userid.lower()  # may need to change
        folder_list = os.listdir(path)
        
        context = {
            "uname": request.user.username,
            "folders" : folder_list
        }
        return render(request, "album_collection/collection.html", context)
    
        
@login_required(login_url="/login")
def view_folder(request, folder_name):
    if request.method == "GET":
        folder = FolderName.objects.get(folder_name = folder_name)
        folder_path = folder.folder_path
        folder_path1 = folder_path.replace('/home/akshay/Code_/code/People_ify/People_ify/static/','',1)
        print(folder)
        images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        image_path = []
        for i in images:
            x = folder_path1 + "/" + i  # "file://" + 
            image_path.append(x)
        context = {
            "images" : image_path,
        }
        return render(request, "album_collection/folder_view.html", context)


@login_required(login_url="/login")
def upload(request, userid):
    if request.method == "GET":
        return render(request, 'album_collection/upload.html', {"uname": (request.user.username).lower() })

    elif request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        print((request.user.username).lower())
        face_identify.main((request.user.username).lower())  # run function after image is uploaded
        # return render(request, "album_collection/collection.html", {"uname": request.user.username })
        folder_list=[]
        path = settings.BASE_DIR + "/static/" + userid.lower()  # may need to change
        folder_list = os.listdir(path)
        
        context = {
            "uname": request.user.username,
            "folders" : folder_list
        }
        return render(request, "album_collection/collection.html", context)

def review_view(request,userid):
    if request.method == "POST":
        star = request.POST["rate"]
        revw = request.POST["revw"]
        usr = Person_Group.objects.get(pg_name=(request.user.username).lower())
        new_rev = Review.objects.create(pg_id=usr, review=revw, rev_star=star)
        rev_list = Review.objects.all()
        context = {
            "stars" : [1,2,3,4,5],
            "uname": request.user.username,
            "result" : rev_list,
        }
        return render(request, "album_collection/review.html", context)

    elif request.method == "GET":
        rev_list = Review.objects.all()
        context = {
            "stars" : [1,2,3,4,5],
            "uname": request.user.username,
            "result" : rev_list,
        }
        return render(request, "album_collection/review.html", context)
    





# c5229c3363cb4d659aea93939677eaa1
# https://centralindia.api.cognitive.microsoft.com/