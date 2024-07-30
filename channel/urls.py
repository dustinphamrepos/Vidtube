from django.urls import path
from channel import views

urlpatterns = [
  path("<channel_id>/", views.channel_profile, name="channel-profile"),
  path("<channel_id>/video/", views.channel_videos, name="channel-videos"),
  path("<channel_id>/about/", views.channel_about, name="channel-about"),
  path("<channel_id>/community/", views.channel_community, name="channel-community"),
  path("<channel_id>/community/<int:community_id>", views.channel_community_detail, name="channel-community-detail"),
  # Create Comment URL
  path("community/<int:community_id>/create-comment/", views.create_comment, name="community-create-comment"),
  # Delete Comment URL
  path("community/<int:community_id>/<int:comment_id>/", views.delete_comment, name="community-delete-comment"),
  # Like Community Posts URL
  path("community/<int:community_id>/like/", views.like_community_post, name="community-post-like"),
  # Uploading video URL
  path("channel/create/video/", views.video_upload, name="upload-video"),
  # Edit video URL
  path("channel/edit-video/<channel_id>/<video_id>/", views.video_edit, name="video-edit"),
  # Create community post URL
  path("channel/create-community-post/<channel_id>/", views.create_community_post, name="create-community-post"),
  # Edit community post URL
  path("channel/edit-community-post/<channel_id>/<community_post_id>/", views.edit_community_post, name="edit-community-post"),
  # Delete community post URL
  path("channel/delete-community-post/<channel_id>/<community_post_id>/", views.delete_community_post, name="delete-community-post"),
]