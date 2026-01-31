import tempfile, requests, logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.utils import cloudinary_url
from cloudinary.uploader import upload
from .models import Video

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Video)
def generate_video_thumbnail(sender, instance, created, **kwargs):
    """
    Automatically generate a thumbnail when a new video is uploaded.
    """
    if created and instance.video_file and not instance.thumbnail:
        try:
            public_id = instance.video_file.name.split('/')[-1].rsplit('.', 1)[0]

            thumb_url, _ = cloudinary_url(
                public_id,
                resource_type="video",
                format="jpg",
                transformation=[
                    {"start_offset": "1"},
                    {"width": 400, "height": 225, "crop": "fill"}
                ]
            )

            response = requests.get(thumb_url)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=True) as tmp:
                    tmp.write(response.content)
                    tmp.flush()
                    uploaded = upload(tmp.name, folder="thumbnails/")
                    instance.thumbnail = uploaded["secure_url"]
                    instance.save(update_fields=["thumbnail"])
        except Exception as e:
            logger.error(f"Thumbnail generation failed for {instance.title}: {e}")