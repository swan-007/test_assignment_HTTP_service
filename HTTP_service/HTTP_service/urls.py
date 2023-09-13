from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from backend.views import UploadViewFile, UserServiceApi, DownloadFile, DataFile


router = DefaultRouter()
router.register("UploadViewFile", UploadViewFile)
router.register("user", UserServiceApi)

urlpatterns = [
    path("datafile/", DataFile.as_view()),
    path("downloadfile/<pk>/", DownloadFile.as_view()),
] + router.urls
