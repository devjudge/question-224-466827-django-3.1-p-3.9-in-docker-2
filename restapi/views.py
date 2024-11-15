# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
# from django.shortcuts import render

# Create your views here.


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import VideoSegment
from .serializers import VideoSegmentSerializer
from .utils import segment_video, combine_videos

@api_view(['POST'])
def process_interval(request):
    video_link = request.data.get("video_link")
    interval_duration = request.data.get("interval_duration")

    if not video_link or not interval_duration:
        return Response({"reason": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Perform video segmentation
        segmented_videos = segment_video(video_link, interval_duration)
        if not segmented_videos:
            return Response({"reason": "Invalid interval duration"}, status=status.HTTP_400_BAD_REQUEST)

        # Save segmented videos to the database
        for video_url in segmented_videos:
            VideoSegment.objects.create(video_url=video_url, duration=interval_duration)

        serializer = VideoSegmentSerializer(VideoSegment.objects.all(), many=True)
        return Response({"interval_videos": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"reason": "Could not process file"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['POST'])
def process_combine(request):
    video_links = request.data.get("video_links")
    resolution = request.data.get("resolution")

    if not video_links or not resolution:
        return Response({"reason": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        combined_video = combine_videos(video_links, resolution)
        if not combined_video:
            return Response({"reason": "Failed to combine videos"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"combined_video_url": combined_video}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"reason": "Could not process file"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
