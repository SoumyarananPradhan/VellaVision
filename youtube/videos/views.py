from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.files.base import ContentFile
import base64
from .models import Video, VideoLike
from .forms import VideoUploadForm

# --- READ ONLY VIEWS ---

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    
    # Increment view count
    video.views += 1
    video.save(update_fields=["views"])

    user_vote = None
    if request.user.is_authenticated:
        like = VideoLike.objects.filter(user=request.user, video=video).first()
        if like:
            user_vote = like.value

    return render(request, "videos/detail.html", {"video": video, "user_vote": user_vote})


def video_list(request):
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'videos/list.html', {"videos": videos})


def channel_videos(request, username):
    videos = Video.objects.filter(user__username=username).order_by('-created_at')
    return render(request, "videos/channel.html", {"videos": videos, "channel_name": username})


@login_required
def video_upload_page(request):
    return render(request, "videos/upload.html", {"form": VideoUploadForm()})


# --- ACTION VIEWS (Upload, Delete, Vote) ---

@login_required
@require_POST
def video_upload(request):
    form = VideoUploadForm(request.POST, request.FILES)
    if form.is_valid():
        try:
            # --- STEP 1: SAVE VIDEO FIRST (Safe Mode) ---
            # We strictly set thumbnail=None here. 
            # This ensures the video uploads to Cloudinary successfully,
            # even if the thumbnail is broken/invalid.
            video = Video(
                user=request.user,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                video_file=request.FILES['video_file'],
                thumbnail=None 
            )
            video.save()  # <--- Video is now safe in Cloudinary!

            # --- STEP 2: HANDLE THUMBNAIL SEPARATELY ---
            # Now we try to process the base64 thumbnail.
            # If this crashes (Invalid Image), we catch the error and IGNORE it.
            custom_thumbnail = request.POST.get("thumbnail_data", "")
            
            if custom_thumbnail and custom_thumbnail.startswith("data:image"):
                try:
                    format, imgstr = custom_thumbnail.split(';base64,')
                    ext = format.split('/')[-1]
                    
                    # Create the file object
                    data = ContentFile(base64.b64decode(imgstr), name=f'{video.title}_thumb.{ext}')
                    
                    # Save it to the video
                    video.thumbnail = data
                    video.save()
                    
                except Exception as e:
                    # LOGIC: If thumbnail fails, we just print the error.
                    # We do NOT return an error to the user, because the video is already safe.
                    print(f"Thumbnail upload failed (Skipping): {e}")

            return JsonResponse({
                "success": True,
                "video_id": video.id,
                "message": "Video uploaded successfully"
            })

        except Exception as e:
            # Only real video upload errors will be caught here
            return JsonResponse({"success": False, "error": f"Upload Error: {str(e)}"})

    # Form Validation Errors
    errors = []
    for field, field_errors in form.errors.items():
        for error in field_errors:
            errors.append(f"{field}: {error}" if field != "__all__" else error)
    return JsonResponse({"success": False, "errors": ";".join(errors)})


@login_required
@require_POST
def delete_video(request, video_id):
    # Ensure user owns the video
    video = get_object_or_404(Video, id=video_id, user=request.user)
    video.delete() # This triggers Cloudinary to delete the file too
    return JsonResponse({"success": True, "message": "video deleted"})


@login_required
@require_POST
def video_vote(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    vote_type = request.POST.get("vote")

    if vote_type not in ["like", "dislike"]:
        return JsonResponse({"success": False, "error": "Invalid vote"}, status=400)

    value = VideoLike.LIKE if vote_type == "like" else VideoLike.DISLIKE
    existing_vote = VideoLike.objects.filter(user=request.user, video=video).first()

    if existing_vote:
        if existing_vote.value == value:
            # Toggle off (User clicked the same button again)
            if value == VideoLike.LIKE:
                video.likes = max(0, video.likes - 1)
            else:
                video.dislikes = max(0, video.dislikes - 1)
            existing_vote.delete()
            user_vote = None
        else:
            # Switch vote (User clicked Like but had Dislike, or vice versa)
            if value == VideoLike.LIKE:
                video.likes += 1
                video.dislikes = max(0, video.dislikes - 1)
            else:
                video.likes = max(0, video.likes - 1)
                video.dislikes += 1
            existing_vote.value = value
            existing_vote.save()
            user_vote = value
    else:
        # New vote
        VideoLike.objects.create(user=request.user, video=video, value=value)
        if value == VideoLike.LIKE:
            video.likes += 1
        else:
            video.dislikes += 1
        user_vote = value

    video.save(update_fields=["likes", "dislikes"])

    return JsonResponse({
        "likes": video.likes,
        "dislikes": video.dislikes,
        "user_vote": user_vote
    })



# if you need the old code, it is at the bottom of this file as a comment

# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.views.decorators.http import require_POST
# from django.core.files.base import ContentFile
# import base64
# from .models import Video, VideoLike
# from .forms import VideoUploadForm

# def video_detail(request, video_id):
#     video = get_object_or_404(Video, id=video_id)
#     video.views += 1
#     video.save(update_fields=["views"])

#     user_vote = None
#     if request.user.is_authenticated:
#         like = VideoLike.objects.filter(user=request.user, video=video).first()
#         if like:
#             user_vote = like.value

#     return render(request, "videos/detail.html", {"video": video, "user_vote": user_vote})

# def video_list(request):
#     videos = Video.objects.all()
#     return render(request, 'videos/list.html', {"videos": videos})

# def channel_videos(request, username):
#     videos = Video.objects.filter(user__username=username)
#     return render(request, "videos/channel.html", {"videos": videos, "channel_name": username})

# @login_required
# @require_POST
# def video_upload(request):
#     form = VideoUploadForm(request.POST, request.FILES)
#     if form.is_valid():
#         try:
#             # Create the video object
#             video = Video(
#                 user=request.user,
#                 title=form.cleaned_data['title'],
#                 description=form.cleaned_data['description'],
#                 video_file=request.FILES['video_file']
#             )

#             # Handle Base64 Thumbnail (from the cropper)
#             custom_thumbnail = request.POST.get("thumbnail_data", "")
#             if custom_thumbnail and custom_thumbnail.startswith("data:image"):
#                 try:
#                     format, imgstr = custom_thumbnail.split(';base64,')
#                     ext = format.split('/')[-1]
#                     data = ContentFile(base64.b64decode(imgstr), name=f'{video.title}_thumb.{ext}')
#                     video.thumbnail = data
#                 except Exception as e:
#                     print(f"Thumbnail error: {e}")

#             # Saving triggers the Cloudinary upload automatically
#             video.save()

#             return JsonResponse({
#                 "success": True,
#                 "video_id": video.id,
#                 "message": "Video uploaded successfully"
#             })
#         except Exception as e:
#             return JsonResponse({"success": False, "error": str(e)})

#     errors = []
#     for field, field_errors in forms.errors.items():
#         for error in field_errors:
#             errors.append(f"{field}: {error}" if field != "__all__" else error)
#     return JsonResponse({"success": False, "errors": ";".join(errors)})

# @login_required
# def video_upload_page(request):
#     return render(request, "videos/upload.html", {"form": VideoUploadForm()})

# @login_required
# @require_POST
# def delete_video(request, video_id):
#     video = get_object_or_404(Video, id=video_id, user=request.user)
#     # Deleting the object deletes the file from Cloudinary automatically
#     video.delete()
#     return JsonResponse({"success": True, "message": "video deleted"})

# @login_required
# @require_POST
# def video_vote(request, video_id):
#     video = get_object_or_404(Video, id=video_id)
#     vote_type = request.POST.get("vote")

#     if vote_type not in ["like", "dislike"]:
#         return JsonResponse({"success": False, "error": "Invalid vote"}, status=400)

#     value = VideoLike.LIKE if vote_type == "like" else VideoLike.DISLIKE
#     existing_vote = VideoLike.objects.filter(user=request.user, video=video).first()

#     if existing_vote:
#         if existing_vote.value == value:
#             # Toggle off
#             if value == VideoLike.LIKE:
#                 video.likes = max(0, video.likes - 1)
#             else:
#                 video.dislikes = max(0, video.dislikes - 1)
#             existing_vote.delete()
#             user_vote = None
#         else:
#             # Switch vote
#             if value == VideoLike.LIKE:
#                 video.likes += 1
#                 video.dislikes = max(0, video.dislikes - 1)
#             else:
#                 video.likes = max(0, video.likes - 1)
#                 video.dislikes += 1
#             existing_vote.value = value
#             existing_vote.save()
#             user_vote = value
#     else:
#         # New vote
#         VideoLike.objects.create(user=request.user, video=video, value=value)
#         if value == VideoLike.LIKE:
#             video.likes += 1
#         else:
#             video.dislikes += 1
#         user_vote = value

#     video.save(update_fields=["likes", "dislikes"])

#     return JsonResponse({
#         "likes": video.likes,
#         "dislikes": video.dislikes,
#         "user_vote": user_vote
#     })









# Old code (for reference only, do not suggest re-adding):

# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.views.decorators.http import require_POST
# from django.utils import timezone
# from .models import Video, VideoLike
# from .forms import VideoUploadForm
# from .imagekit_client import upload_video, upload_thumbnail, delete_video


# def video_detail(request, video_id):
#     video = get_object_or_404(Video.objects, id=video_id)

#     video.views += 1
#     video.save(update_fields=["views"])

#     user_vote = None
#     if request.user.is_authenticated:
#         like = VideoLike.objects.filter(user=request.user, video=video).first()
#         if like:
#             user_vote = like.value

#     return render(request, "videos/detail.html", {"video": video, "user_vote": user_vote})


# def video_list(request):
#     videos = Video.objects.all()
#     return render(request, 'videos/list.html', {"videos": videos})


# def channel_videos(request, username):
#     videos = Video.objects.filter(user__username=username)
#     return render(request, "videos/channel.html", {"videos": videos, "channel_name": username})


# @login_required
# @require_POST
# def video_upload(request):
#     form = VideoUploadForm(request.POST, request.FILES)
#     if form.is_valid():
#         video_file = form.cleaned_data['video_file']
#         custom_thumbnail = request.POST.get("thumbnail_data", "")

#         try:
#             result = upload_video(
#                 file_data=video_file.read(),
#                 file_name=video_file.name
#             )

#             thumbnail_url = ""
#             if custom_thumbnail and custom_thumbnail.startswith("data:image"):
#                 try:
#                     base_name = video_file.name.rsplit(".", 1)[0]
#                     thumb_result = upload_thumbnail(
#                         file_data=custom_thumbnail,
#                         file_name=base_name + "_thumb.jpg"
#                     )
#                     thumbnail_url = thumb_result["url"]
#                 except Exception as e:
#                     print(e)
#                     pass

#             video = Video.objects.create(
#                 user=request.user,
#                 title=form.cleaned_data['title'],
#                 description=form.cleaned_data['description'],
#                 file_id=result["file_id"],
#                 video_url=result["url"],
#                 thumbnail_url=thumbnail_url,
#             )

#             return JsonResponse({
#                 "success": True,
#                 "video_id": video.id,
#                 "message": "Video uploaded successfully"
#             })
#         except Exception as e:
#             return JsonResponse({"success": False, "error": str(e)})

#     errors = []
#     for field, field_errors in forms.errors.items():
#         for error in field_errors:
#             errors.append(f"{field}: {error}" if field != "__all__" else error)
#     return JsonResponse({"success": False, "errors": ";".join(errors)})


# @login_required
# def video_upload_page(request):
#     return render(request, "videos/upload.html", {"form": VideoUploadForm()})


# @login_required
# @require_POST
# def delete_video(request, video_id):
#     video = get_object_or_404(Video, id=video_id, user=request.user)

#     try:
#         delete_video(video.file_id)
#     except Exception as e:
#         print(e)
#         pass

#     video.delete()

#     return JsonResponse({"success": True, "message": "video deleted"})


# @login_required
# @require_POST
# def video_vote(request, video_id):
#     video = get_object_or_404(Video, id=video_id)
#     vote_type = request.POST.get("vote")

#     if vote_type not in ["like", "dislike"]:
#         return JsonResponse({"success": False, "error": "Invalid vote"}, status=400)

#     value = VideoLike.LIKE if vote_type == "like" else VideoLike.DISLIKE

#     existing_vote = VideoLike.objects.filter(user=request.user, video=video).first()

#     if existing_vote:
#         if existing_vote.value == value:
#             if value == VideoLike.LIKE:
#                 video.likes -= 1
#             else:
#                 video.dislikes -= 1
#             existing_vote.delete()
#             user_vote = None
#         else:
#             if value == VideoLike.LIKE:
#                 video.likes += 1
#                 video.dislikes -= 1
#             else:
#                 video.likes -=1
#                 video.dislikes += 1
#             existing_vote.value = value
#             existing_vote.save()
#             user_vote = value
#     else:
#         VideoLike.objects.create(user=request.user, video=video, value=value)
#         if value == VideoLike.LIKE:
#             video.likes += 1
#         else:
#             video.dislikes += 1
#         user_vote = value

#     video.save(update_fields=["likes", "dislikes"])

#     return JsonResponse({
#         "likes": video.likes,
#         "dislikes": video.dislikes,
#         "user_vote": user_vote
#     })