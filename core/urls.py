from django.urls import path
from core import views

urlpatterns = [
  path("", views.index, name="home"),
  path("watch/<int:pk>/", views.videoDetail, name="video-detail"),

  # Saving comment to db
  path("ajax-save-comment/", views.ajax_save_comment, name="save-comment"),
]