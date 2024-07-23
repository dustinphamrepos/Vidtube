from django.shortcuts import render

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

  context = {
    "video":video,
  }
  return render(request, "video-detail.html", context)
