from django.urls import path
from core import views

urlpatterns = [
  path("", views.index, name="home"),
  path("watch/<int:pk>/", views.videoDetail, name="video-detail"),

  # Saving comment to db
  path("ajax-save-comment/", views.ajax_save_comment, name="save-comment"),
  path("ajax-delete-comment/", views.ajax_delete_comment, name="delete-comment"),

  # Subscribe function
  path("add-sub/<int:id>/", views.add_new_subscribers, name="add-sub"),
  path("sub-load/<int:id>/", views.load_channel_subs, name="sub-load"),
]