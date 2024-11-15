from rest_framework import serializers
from .models import VideoSegment

class VideoSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoSegment
        fields = ['id', 'video_url', 'duration', 'created_at']
