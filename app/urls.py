from django.urls import path

from app.views import *

urlpatterns = [
    path('', DownloadMP3View.as_view(), name="download-mp3"),
    path('mp4', DownloadMP4View.as_view(), name="download-mp4"),
    path('download', downloadVideo, name="download")
]