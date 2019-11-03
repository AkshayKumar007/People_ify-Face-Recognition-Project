from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request,"templates/login_auth/index.html")  # index.html will be welcome screen


def register_view(request):
    if request.method == "GET":
        return render(request,"templates/login_auth/register.html")

    elif request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        uname = request.POST["uname"]
        passwd = request.POST["passwd"] 
        res1 = User.objects.get(email=email)
        res2 = User.objects.get(username=uname)
        if res1 is not None:
            return JsonResponse({"message": "email already registered! Please sign-in or use other email."}) 
        elif res2 is not None:
            return JsonResponse({"message": "username already registered! Please use other Username."})
        else:
            try:
                u = User.objects.create_user(username=uname,first_name=fname, last_name=lname, email=email, password=passwd)
                u.save()
                # change for album_collection 
                return redirect("homepage", userid=request.user.userid)  # try HttpResponseRedirect
            except:
                return JsonResponse({"message": "Something went wrong!"})


def login_view(request):
    if request.method == "GET":
        return render(request,"templates/login_auth/login.html")

    elif request.method == "POST":
        email = request.POST["email"]
        passwd = request.POST["passwd"]
        user = authenticate(request, email=email, password=passwd)
        if user is not None:
            login(request, user)
            return redirect("homepage", userid=request.user.userid)  # 1. have to create homepage 2. also check for HttpResponseRedirect
        else:
            return JsonResponse({"message": "Incorrect email or Password"})

        
@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return redirect("index")

# @login_required(login_url="/login")