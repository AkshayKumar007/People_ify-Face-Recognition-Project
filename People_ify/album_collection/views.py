from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User

# Create your views here.

@login_required(login_url="/login")
def homepage(request, userid):
    if request.method == "GET":
        context = {
            "uname": userid
        }
        print("I'm here!")
        return render(request, "album_collection/collection.html", context)
        # return JsonResponse({"message":"OK"})
        
# export DJANGO_SETTINGS_MODULE=People_ify.settings
