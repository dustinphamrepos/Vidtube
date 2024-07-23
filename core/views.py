from django.shortcuts import render
from django.http import HttpResponse

from .models import Video

# Create your views here.
def index(request):
  video = Video.objects.filter(visibility="public").order_by("-date")
  context = {
    "video":video
  }
  return render(request, "index.html", context)
