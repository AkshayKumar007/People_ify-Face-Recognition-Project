from django.urls import path, re_path
from . import views

urlpatterns = [
    path("<str:userid>", views.homepage, name="homepage")
]