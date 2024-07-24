from django.urls import path
from channel import views

urlpatterns = [
  path("<channel_name>/", views.channel_profile, name="channel-profile"),
  path("<channel_name>/video/", views.channel_videos, name="channel-videos"),
  path("<channel_name>/about/", views.channel_about, name="channel-about"),
]