from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from cloudinary_storage.validators import validate_video
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary import CloudinaryImage
import re


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    # Video file stored in Cloudinary
    video_file = models.FileField(
        upload_to='videos/',
        storage=VideoMediaCloudinaryStorage(),
        validators=[validate_video]
    )
    
    # Optional manual thumbnail upload
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

    @property
    def video_url(self):
        """Returns the full Cloudinary video URL"""
        if self.video_file:
            try:
                return self.video_file.url
            except Exception:
                return ""
        return ""

    @property
    def display_thumbnail_url(self):
        """
        Returns thumbnail URL with intelligent fallback:
        1. Manual thumbnail (if uploaded)
        2. Auto-generated from Cloudinary video (first frame)
        3. Empty string (template will use placeholder)
        """
        # Priority 1: Manual thumbnail
        if self.thumbnail:
            try:
                return self.thumbnail.url
            except Exception:
                pass
        
        # Priority 2: Generate from Cloudinary video
        if self.video_file:
            try:
                # Extract the public_id from the video file path
                # Example: videos/sample.mp4 -> videos/sample
                public_id = self.video_file.name
                
                # Remove file extension if present
                if '.' in public_id:
                    public_id = public_id.rsplit('.', 1)[0]
                
                # Generate thumbnail URL using Cloudinary transformation
                # This creates a JPG thumbnail from the first frame (so_0)
                cloudinary_obj = CloudinaryImage(public_id, resource_type='video')
                thumbnail_url = cloudinary_obj.build_url(
                    transformation=[
                        {'start_offset': '0'},  # First frame
                        {'width': 640, 'height': 360, 'crop': 'fill'},  # Resize
                        {'quality': 'auto'},  # Auto quality
                        {'format': 'jpg'}  # Convert to JPG
                    ]
                )
                return thumbnail_url
                
            except Exception as e:
                # Log error for debugging
                print(f"Thumbnail generation failed for video {self.id}: {str(e)}")
                return ""
        
        return ""


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
