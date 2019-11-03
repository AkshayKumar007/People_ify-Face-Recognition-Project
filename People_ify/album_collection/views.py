from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User

# Create your views here.

@login_required(login_url="/login")
def homepage(request):
    if request.method == "GET":
        context = {
            "uname": request.user.username
        }
        return render(request, "album_collection/collection.html", context)
