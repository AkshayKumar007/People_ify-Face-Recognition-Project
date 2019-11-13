from django.urls import path
from . import views

urlpatterns = [
    path("album-collection/<str:userid>", views.homepage, name="homepage")
]