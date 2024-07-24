from django.shortcuts import render
from django.db.models import Count, Q

from .models import Video

# Create your views here.
def index(request):
  video = Video.objects.filter(visibility="public").order_by("-date")
  context = {
    "video":video
  }
  return render(request, "index.html", context)
def videoDetail(request, pk):
  video = Video.objects.get(id=pk)
  
  video.views = video.views + 1
  video.save()

  # Suggesting Video
  video_tags_id = video.tags.values_list("id", flat=True)
  similar_videos = Video.objects.filter(tags__in=video_tags_id).exclude(id=video.id)
  similar_videos = similar_videos.annotate(same_tags=Count("tags", filter=Q(tags__in=video_tags_id))).order_by("-same_tags", "-date")[:25]

  context = {
    "video": video,
    "similar_videos": similar_videos,
  }
  return render(request, "video-detail.html", context)
