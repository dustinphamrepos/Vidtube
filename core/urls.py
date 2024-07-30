from django.urls import path
from core import views

urlpatterns = [
  path("", views.index, name="index"),
  path("watch/<int:pk>/", views.videoDetail, name="video-detail"),

  # Saving comment to db
  path("ajax-save-comment/", views.ajax_save_comment, name="save-comment"),
  path("ajax-delete-comment/", views.ajax_delete_comment, name="delete-comment"),

  # Subscribe function
  path("add-sub/<int:id>/", views.add_new_subscribers, name="add-sub"),
  path("sub-load/<int:id>/", views.load_channel_subs, name="sub-load"),

  # Like Function
  path("add-like/<int:id>/", views.add_new_like, name="add-like"),
  path("likes-load/<int:id>/", views.load_video_likes, name="like-load"),

  # Saving video to profile
  path("save-video/<video_id>/", views.save_video, name="save-video"),
  # Search URL
  path("video/search/", views.search_view, name="search"),
  # Tag URL
  path("tags/video/<slug:tag_slug>", views.tag_list, name="tags"),
  # Trending URL
  path("trending/", views.trending, name="trending"),
  # Saved video URL
  path("saved-videos/", views.saved_videos, name="saved-videos"),
]