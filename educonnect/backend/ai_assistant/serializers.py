from rest_framework import serializers
from .models import ChatSession, ChatMessage, UserRecommendation, SmartSearchQuery
from courses.serializers import CourseListSerializer


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('id', 'message_type', 'content', 'metadata', 'timestamp')
        read_only_fields = ('id', 'timestamp')


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ('id', 'session_id', 'title', 'messages', 'message_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'session_id', 'created_at', 'updated_at')

    def get_message_count(self, obj):
        return obj.messages.count()


class ChatSessionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for chat session lists"""
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ('id', 'session_id', 'title', 'message_count', 'last_message', 'updated_at')

    def get_message_count(self, obj):
        return obj.messages.count()

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return {
                'content': last_msg.content[:100] + '...' if len(last_msg.content) > 100 else last_msg.content,
                'timestamp': last_msg.timestamp
            }
        return None


class UserRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecommendation
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at')


class SmartSearchQuerySerializer(serializers.ModelSerializer):
    suggested_courses = CourseListSerializer(many=True, read_only=True)

    class Meta:
        model = SmartSearchQuery
        fields = '__all__'
        read_only_fields = ('id', 'user', 'processed_query', 'extracted_filters', 'confidence_score', 'processing_time', 'created_at')


class ChatQuerySerializer(serializers.Serializer):
    """Serializer for incoming chat queries"""
    message = serializers.CharField(max_length=2000)
    session_id = serializers.CharField(max_length=100, required=False)


class SmartSearchRequestSerializer(serializers.Serializer):
    """Serializer for smart search requests"""
    query = serializers.CharField(max_length=500)
    filters = serializers.JSONField(required=False, default=dict)