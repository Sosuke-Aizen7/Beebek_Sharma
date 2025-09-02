from django.contrib import admin
from .models import ChatSession, ChatMessage, UserRecommendation, SmartSearchQuery


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user', 'title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('session_id', 'user__email', 'title')
    ordering = ('-updated_at',)
    readonly_fields = ('session_id', 'created_at', 'updated_at')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'message_type', 'content', 'timestamp')
    list_filter = ('message_type', 'timestamp')
    search_fields = ('session__session_id', 'content')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)


@admin.register(UserRecommendation)
class UserRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'recommendation_type', 'title', 'confidence_score', 'is_dismissed', 'created_at')
    list_filter = ('recommendation_type', 'is_dismissed', 'confidence_score', 'created_at')
    search_fields = ('user__email', 'title', 'description')
    ordering = ('-confidence_score', '-created_at')
    readonly_fields = ('created_at',)


@admin.register(SmartSearchQuery)
class SmartSearchQueryAdmin(admin.ModelAdmin):
    list_display = ('user', 'original_query', 'confidence_score', 'processing_time', 'created_at')
    list_filter = ('confidence_score', 'created_at')
    search_fields = ('user__email', 'original_query', 'processed_query')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'processing_time')