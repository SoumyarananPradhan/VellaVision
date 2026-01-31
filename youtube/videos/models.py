from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from cloudinary_storage.validators import validate_video
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary import utils

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    # We use FileField now. Cloudinary handles the storage automatically.
    video_file = models.FileField(upload_to='videos/',storage=VideoMediaCloudinaryStorage(),
        validators=[validate_video])
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    # Compatibility properties for your templates
    @property
    def video_url(self):
        if self.video_file:
            return self.video_file.url
        return ""



    @property
    def display_thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
    
        if self.video_file:
            try:
            # We strip the extension to get the 'Public ID' Cloudinary needs
            # Example: 'videos/beach_video.mp4' -> 'videos/beach_video'
                public_id = self.video_file.name.rsplit('.', 1)[0]
            
                url, options = utils.cloudinary_url(
                    public_id,
                    resource_type="video",
                    format="jpg",
                    frame="1",
                    transformation=[
                        {'width': 400, 'crop': "fill", 'aspect_ratio': "16:9"}
                    ]
                )
                return url
            except Exception:
                return ""
        return ""
    # @property
    # def display_thumbnail_url(self):
    #     # 1. Check for manual thumbnail first
    #     if self.thumbnail:
    #         return self.thumbnail.url
        
    #     # 2. If missing, generate one from the video automatically
    #     # This prevents the "AttributeError" on your listing page
    #     if self.video_file:
    #         try:
    #             url, options = utils.cloudinary_url(
    #                 self.video_file.name,
    #                 resource_type="video",
    #                 format="jpg",
    #                 frame="1"
    #             )
    #             return url
    #         except Exception:
    #             return "" # Fallback to empty if Cloudinary fails
    #     return ""


    # @property
    # def display_thumbnail_url(self):
    #     if self.thumbnail:
    #         return self.thumbnail.url
    #     return ""

class VideoLike(models.Model):
    LIKE = 1
    DISLIKE = -1
    LIKE_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="user_likes")
    value = models.SmallIntegerField(choices=LIKE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "video"]

    def __str__(self):
        action = "liked" if self.value == self.LIKE else "disliked"
        return f"{self.user.username} {action} {self.video.title}"


# Old code for reference (commented out)
# from django.db import models
# from django.contrib.auth.models import User
# from .imagekit_client import (
#     get_optimized_video_url, get_streaming_url, get_thumbnail_url, add_image_watermark
# )


# class Video(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")
#     title = models.CharField(max_length=120)
#     description = models.TextField(blank=True)

#     file_id = models.CharField(max_length=200)
#     video_url = models.URLField(max_length=500)
#     thumbnail_url = models.URLField(max_length=500, blank=True)

#     views = models.PositiveIntegerField(default=0)
#     likes = models.PositiveIntegerField(default=0)
#     dislikes = models.PositiveIntegerField(default=0)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     upload_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
#     class Meta:
#         ordering = ["-created_at"]

#     def __str__(self):
#         return self.title

#     @property
#     def display_thumbnail_url(self):
#         if self.thumbnail_url and "/thumbnails/" in self.thumbnail_url:
#             return add_image_watermark(self.thumbnail_url, self.user.username)
#         return self.generated_thumbnail_url

#     @property
#     def generated_thumbnail_url(self):
#         if not self.video_url:
#             return ""
#         return get_thumbnail_url(self.video_url, self.user.username)

#     @property
#     def streaming_url(self):
#         if not self.video_url:
#             return ""
#         return get_streaming_url(self.video_url)

#     @property
#     def optimized_url(self):
#         if not self.video_url:
#             return ""
#         return get_optimized_video_url(self.video_url)


# class VideoLike(models.Model):
#     LIKE = 1
#     DISLIKE = -1
#     LIKE_CHOICES = [
#         (LIKE, "Like"),
#         (DISLIKE, "Dislike")
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="user_likes")
#     value = models.SmallIntegerField(choices=LIKE_CHOICES)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ["user", "video"]

#     def __str__(self):
#         action = "liked" if self.value == self.LIKE else "disliked"
#         return f"{self.user.username} {action} {self.video.title}"