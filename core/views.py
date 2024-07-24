from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db.models import Count, Q
from django.views.decorators.csrf import csrf_exempt

from channel.models import Channel

from .models import Video, Comment

# Create your views here.
def index(request):
  video = Video.objects.filter(visibility="public").order_by("-date")
  context = {
    "video":video
  }
  return render(request, "index.html", context)
def videoDetail(request, pk):
  video = Video.objects.get(id=pk)
  channel = Channel.objects.get(user=video.user)
  
  video.views = video.views + 1
  video.save()

  # Suggesting Video
  video_tags_id = video.tags.values_list("id", flat=True)
  similar_videos = Video.objects.filter(tags__in=video_tags_id).exclude(id=video.id)
  similar_videos = similar_videos.annotate(same_tags=Count("tags", filter=Q(tags__in=video_tags_id))).order_by("-same_tags", "-date")[:25]

  # Getting all comment related to a video
  comment = Comment.objects.filter(active=True, video=video).order_by("-date")
  
  context = {
    "video": video,
    "similar_videos": similar_videos,
    "comment": comment,
    "channel": channel,
  }
  return render(request, "video-detail.html", context)

def ajax_save_comment(request):
  if request.method == "POST":
    pk = request.POST.get("id")

    comment = request.POST.get("comment")
    video = Video.objects.get(id=pk)
    user = request.user

    new_comment = Comment.objects.create(comment=comment, user=user, video=video)
    new_comment.save()

    response = "Comment Posted"
    return HttpResponse(response)
  
@csrf_exempt
def ajax_delete_comment(request):
  if request.method == "POST":
    id = request.POST.get("cid")
    comment = Comment.objects.get(id=id)
    comment.delete()
    return JsonResponse({"status":1})
  else:
    return JsonResponse({"status":2})

# Subscribe Functions
def add_new_subscribers(request, id):
  channel = Channel.objects.get(id=id)
  user = request.user

  if user in channel.subscribers.all():
    channel.subscribers.remove(user)
    response = "Subscribe"
    return JsonResponse(response, safe=False, status=200)
  else:
    channel.subscribers.add(user)
    response = "Unsubscribe"
    return JsonResponse(response, safe=False, status=200)

# Load channel subs
def load_channel_subs(request, id):
  channel = Channel.objects.get(id=id)
  sub_lists = list(channel.subscribers.values())
  return JsonResponse(sub_lists, safe=False, status=200)

def add_new_like(request, id):
  video = Video.objects.get(id=id)
  user = request.user

  if user in video.likes.all():
    video.likes.remove(user)
    like_response = '<i class="fa fa-thumbs-up"></i>'
    return JsonResponse(like_response, safe=False, status=200)
  else:
    video.likes.add(user)
    like_response = '<i class="fa fa-thumbs-up"></i>'
    return JsonResponse(like_response, safe=False, status=200)

def load_video_likes(request, id):
  video = Video.objects.get(id=id)
  likes_lists = list(video.likes.values())
  return JsonResponse(likes_lists, safe=False, status=200)


