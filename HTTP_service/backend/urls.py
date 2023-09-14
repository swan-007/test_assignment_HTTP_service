from rest_framework.routers import DefaultRouter
from django.urls import path
from backend.views import (
    UploadViewFile,
    UserServiceApi,
    DataFile,
    RegisterAccount,
    LoginAccount,
)

router = DefaultRouter()
router.register("UploadViewFile", UploadViewFile)
router.register("user", UserServiceApi)

urlpatterns = [
    path("datafile/", DataFile.as_view()),
    path("register/", RegisterAccount.as_view()),
    path("login/", LoginAccount.as_view()),
] + router.urls
