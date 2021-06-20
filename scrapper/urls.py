from django.urls import path
from scrapper.api.youtube_scrapper import YoutubeVideo

urlpatterns = [
    path(r"videos/", YoutubeVideo.as_view(), name="Fetch videos"),
]
