import pytz

from django.db import models

from code_service.core.abstract_models import BigIDAbstract


class YoutubeVideo(BigIDAbstract):
    etag = models.CharField(max_length=150)
    video_id = models.CharField(unique=True, db_index=True, max_length=100)
    published_at = models.DateTimeField(db_index=True)
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=5000)
    meta = models.JSONField(default=dict)
