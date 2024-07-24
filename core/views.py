from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db.models import Count, Q
from django.views.decorators.csrf import csrf_exempt

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
