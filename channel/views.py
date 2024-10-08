from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CommunityForm, VideoForm
from .models import Channel, Community, CommunityComment
from core.models import Video

# Create your views here.
def channel_profile(request, channel_id):
  channel = get_object_or_404(Channel, id=channel_id)

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

def channel_videos(request, channel_id):
  channel = get_object_or_404(Channel, id=channel_id)
  videos = Video.objects.filter(user=channel.user, visibility="public").order_by("-date")
        
  context = {
      "videos":videos,
      "channel":channel,
  }

  return render(request, "channel/channel-videos.html", context)

def channel_about(request, channel_id):
  channel = get_object_or_404(Channel, id=channel_id)
        
  context = {
    "channel":channel,
  }

  return render(request, "channel/channel-about.html", context)

def channel_community(request, channel_id):
  channel = get_object_or_404(Channel, id=channel_id)
  community = Community.objects.filter(channel=channel, status="active").order_by("-date")

  context = {
    "channel": channel,
    "community": community,
  }

  return render(request, "channel/channel-community.html", context)


def channel_community_detail(request, channel_id, community_id):
  channel = get_object_or_404(Channel, id=channel_id)
  community = Community.objects.get(channel=channel, id=community_id, status="active")

  comments = CommunityComment.objects.filter(active=True, community=community).order_by("-date")

  context = {
    "channel": channel,
    "community": community,
    "comments": comments,
  }

  return render(request, "channel/channel-community-detail.html", context)

@login_required
def create_comment(request, community_id):
  if request.method == "POST":
    community = Community.objects.get(id=community_id, status="active")
    comment = request.POST.get("comment")
    user = request.user 

    new_comment = CommunityComment.objects.create(community=community, user=user, comment=comment)
    new_comment.save()
    messages.success(request, f"Comment posted.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
  
@login_required
def delete_comment(request, community_id, comment_id):
  community = Community.objects.get(id=community_id)
  comment = CommunityComment.objects.get(id=comment_id, community=community)

  comment.delete()
  messages.success(request, f"Comment deleted.")

  return redirect("channel-community-detail", community.channel.id, community.id)

@login_required
def like_community_post(request, community_id):
  community = Community.objects.get(id=community_id)
  user = request.user

  if user in community.likes.all():
    community.likes.remove(user)
  else:
    community.likes.add(user)
    
  return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@login_required
def video_upload(request):
  user = request.user
  if request.method == "POST":
    form = VideoForm(request.POST, request.FILES)
    if form.is_valid():
      new_form = form.save(commit=False)
      new_form.user = user
      new_form.save()
      form.save_m2m()
      messages.success(request, f"Video uploaded successfully.")
      return redirect("channel-profile", user.channel.id)
  else:
    form = VideoForm()
  context = {
    "form": form,
  }
  return render(request, "channel/upload-video.html", context)

@login_required
def video_edit(request, channel_id, video_id):
  video = Video.objects.get(id=video_id)
  user = request.user

  if request.method == "POST":
    form = VideoForm(request.POST, request.FILES, instance=video)
    if form.is_valid():
      new_form = form.save(commit=False)
      new_form.user = user
      new_form.save()
      form.save_m2m()
      messages.success(request, f"Video Edited Successfully.")
      return redirect("studio")
  else:
    form = VideoForm(instance=video)
  context = {
    "form": form,
    "video": video,
  }
  return render(request, "channel/upload-video.html", context)

@login_required
def video_delete(request, video_id):
  video = Video.objects.get(id=video_id)

  if request.user == video.user:
    video.delete()
    return redirect("studio")
  else:
    return HttpResponse("You are not allowed to delete this video")
    
@login_required
def create_community_post(request, channel_id):
  channel = Channel.objects.get(id=channel_id)

  if request.method == "POST":
    form = CommunityForm(request.POST, request.FILES)
    if form.is_valid():
      new_form = form.save(commit=False)
      new_form.channel = channel
      new_form.save()
      post_id = new_form.id
      messages.success(request, "Post created.")
      return redirect("channel-community-detail", channel.id, post_id)
  else:
    form = CommunityForm()
  context = {
    "form":form,
  }
  return render(request, "channel/create-community-post.html", context)

@login_required
def edit_community_post(request, channel_id, community_post_id):
  channel = Channel.objects.get(id=channel_id)
  community = Community.objects.get(id=community_post_id)

  if request.method == "POST":
    form = CommunityForm(request.POST, request.FILES, instance=community)
    if form.is_valid():
      new_form = form.save(commit=False)
      new_form.channel = channel
      new_form.save()
      community_id = new_form.id
      messages.success(request, "Post edited.")
      return redirect("channel-community-detail", channel.id, community_id)
  else:
    form = CommunityForm(instance=community)
  context = {
    "form":form,
  }
  return render(request, "channel/create-community-post.html", context)

@login_required
def delete_community_post(request, channel_id, community_post_id):
  channel = Channel.objects.get(id=channel_id)
  community = Community.objects.get(id=community_post_id)

  community.delete()
  return redirect("channel-community", channel.id)