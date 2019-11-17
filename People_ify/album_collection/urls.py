from django.urls import path, re_path
from . import views

urlpatterns = [
    path("<str:userid>", views.homepage, name="homepage"),
    path("<str:userid>/view_folder/<str:folder_name>", views.view_folder, name="view_folder"),
    path("<str:userid>/upload",views.upload,name="upload"),
]