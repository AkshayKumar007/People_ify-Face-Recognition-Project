from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
import album_collection

# Create your views here.
def index(request):
    # css_url = url_for('static', filename='js/main.js')
    return render(request,"login_auth/index.html")  # index.html will be welcome screen


def register_view(request):
    if request.method == "GET":
        return render(request,"login_auth/register.html")

    elif request.method == "POST":
        print("I'm here!")
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        uname = request.POST["uname"]
        passwd = request.POST["passwd"] 
        res1 = User.objects.get(email=email)
        res2 = User.objects.get(username=uname)
        if res1 is not None:
            return JsonResponse({"message": "no_email"}) 
        elif res2 is not None:
            return JsonResponse({"message": "no_uname"})
        else:
            try:
                u = User.objects.create_user(username=uname,first_name=fname, last_name=lname, email=email, password=passwd)
                u.save()
                login(request, u)
                # change for album_collection 
                # return redirect("album_collection.views.homepage", userid=request.user.userid)  # try HttpResponseRedirect
                return JsonResponse({"message":"success", "userid":request.user.userid})
            except:
                return JsonResponse({"message": "wrong"})


def login_view(request):
    if request.method == "GET":
        return render(request,"login_auth/login.html")

    elif request.method == "POST":
        print("I'm here")
        email = request.POST["email"]
        passwd = request.POST["passwd"]
        user = authenticate(request, email=email, password=passwd)
        if user is not None:
            login(request, user)
            return redirect("homepage", userid=request.user.userid)  # 1. have to create homepage 2. also check for HttpResponseRedirect
        else:
            return JsonResponse({"message": "Incorrect email or Password"})

        
@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect("index")

# @login_required(login_url="/login")