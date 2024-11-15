# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class VideoSegment(models.Model):
    video_url = models.CharField(max_length=255)
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Segment {self.id} ({self.duration}s)"

