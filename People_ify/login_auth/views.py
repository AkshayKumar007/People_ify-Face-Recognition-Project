from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render("People_ify/templates/index.html") #  index.html will be welcome screen

#  very Basic! Will add code to check is user already exists
def register_view(request):
    fname = request.POST["fname"]
    lname = request.POST["lname"]
    email = request.POST["email"]
    uname = request.POST["uname"]
    passwd = request.POST["passwd"] 
    try:
        u = User.objects.create_user(username=uname,first_name=fname, last_name=lname, email=email, password=passwd)
        u.save()
        return HttpResponseRedirect("homepage") #  check
    except:
        context = {
            "message": "Something went wrong!"
        }
        return HttpResponseRedirect("register_view", context)
    

def login_view(request):
    email = request.POST["email"]
    passwd = request.POST["passwd"]
    user = authenticate(request, email=email, password=passwd)
    if user is not None:
        login(request, user)
        return redirect("homepage") #  1. have to create homepage  2. also check for HttpResponseRedirect
    else:
        context = { 
            "message" : "Invalid email or password"
        }
        return redirect("login")

        
@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return redirect("index")

# @login_required(login_url="/login")