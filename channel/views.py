from django.shortcuts import get_object_or_404, render

from .models import Channel
from core.models import Video

# Create your views here.
def channel_profile(request, channel_name):
  channel = get_object_or_404(Channel, id=channel_name)

  # Getting Popular Videos
  videos = Video.objects.filter(user=channel.user, visibility="public").order_by("-views")
  try:
    video_featured = Video.objects.get(user=channel.user, featured=True)
  except:
    video_featured = None
    # messages.warning(request, f"Only one video can be featured!")
        
  context = {
    "videos": videos,
    "channel": channel,
    "video_featured": video_featured
  }

  return render(request, "channel/channel.html", context)

def channel_videos(request, channel_name):
  channel = get_object_or_404(Channel, id=channel_name)
  videos = Video.objects.filter(user=channel.user, visibility="public").order_by("-date")
        
  context = {
      "videos":videos,
      "channel":channel,
  }

  return render(request, "channel/channel-videos.html", context)