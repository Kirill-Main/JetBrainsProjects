from abc import ABC

from rest_framework import serializers

from .models import Feedback


class FeedbackSerializer(serializers.Serializer):
    class Meta:
        model = Feedback
        fields = ('user.name', 'published', 'content', 'is_recommended')