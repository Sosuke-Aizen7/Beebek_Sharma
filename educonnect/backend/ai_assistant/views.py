from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
import uuid
import time

from .models import ChatSession, ChatMessage, UserRecommendation, SmartSearchQuery
from .serializers import (
    ChatSessionSerializer, ChatSessionListSerializer, ChatMessageSerializer,
    UserRecommendationSerializer, SmartSearchQuerySerializer,
    ChatQuerySerializer, SmartSearchRequestSerializer
)
from courses.models import Course
from courses.serializers import CourseListSerializer


class ChatSessionListView(generics.ListCreateAPIView):
    serializer_class = ChatSessionListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        session_id = str(uuid.uuid4())
        serializer.save(user=self.request.user, session_id=session_id)


class ChatSessionDetailView(generics.RetrieveAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

    def get_object(self):
        session_id = self.kwargs.get('session_id')
        return generics.get_object_or_404(self.get_queryset(), session_id=session_id)


class UserRecommendationListView(generics.ListAPIView):
    serializer_class = UserRecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserRecommendation.objects.filter(
            user=self.request.user,
            is_dismissed=False
        )