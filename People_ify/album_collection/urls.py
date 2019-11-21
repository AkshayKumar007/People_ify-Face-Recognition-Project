from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

# app_name='album_collection'

urlpatterns = [
    path("<str:userid>", views.homepage, name="homepage"),
    path("view_folder/<str:folder_name>", views.view_folder, name="view_folder"),
    path("<str:userid>/upload", views.upload ,name="upload"),
    path("review/<str:userid>", views.review_view, name="review_view"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)