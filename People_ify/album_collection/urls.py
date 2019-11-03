from django.urls import path
from . import views

urlpatterns = [
    path("album-collection/<int:userid>", views.homepage, name="homepage")
]