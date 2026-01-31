# youtube/videos/management/commands/generate_thumbnails.py
from django.core.management.base import BaseCommand
from videos.models import Video
from cloudinary.utils import cloudinary_url
from cloudinary.uploader import upload
import requests, tempfile, logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Generate Cloudinary thumbnails for existing videos"

    def handle(self, *args, **options):
        for video in Video.objects.all():
            if video.thumbnail:
                self.stdout.write(self.style.NOTICE(f"Skipping {video.title}, already has thumbnail"))
                continue

            if not video.video_file:
                self.stdout.write(self.style.WARNING(f"Skipping {video.title}, no video file"))
                continue

            try:
                # Full public ID (keep folder, strip extension)
                public_id = video.video_file.name.rsplit('.', 1)[0]

                # Build Cloudinary thumbnail URL
                thumb_url, _ = cloudinary_url(
                    public_id,
                    resource_type="video",
                    format="jpg",
                    transformation=[
                        {"start_offset": "1"},
                        {"width": 400, "height": 225, "crop": "fill"}
                    ]
                )

                self.stdout.write(f"Generated thumbnail URL for {video.title}: {thumb_url}")

                # Try fetching the frame
                response = requests.get(thumb_url)
                if response.status_code == 200:
                    with tempfile.NamedTemporaryFile(delete=True) as tmp:
                        tmp.write(response.content)
                        tmp.flush()
                        uploaded = upload(tmp.name, folder="thumbnails/")
                        video.thumbnail = uploaded["secure_url"]
                        video.save(update_fields=["thumbnail"])
                        self.stdout.write(self.style.SUCCESS(f"Thumbnail saved for {video.title}"))
                else:
                    self.stdout.write(self.style.ERROR(
                        f"Failed to fetch thumbnail for {video.title} — status {response.status_code}"
                    ))

            except Exception as e:
                logger.error(f"Thumbnail generation failed for {video.title}: {e}")
                self.stdout.write(self.style.ERROR(f"Error on {video.title}: {e}"))