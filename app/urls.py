from django.urls import path

from app.views import *

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('download', downloadVideo, name="download")
]