from django.db import models
from users.models import User


class ChatSession(models.Model):
    """Model to track chat sessions with the AI assistant"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions', blank=True, null=True)
    session_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        user_info = self.user.email if self.user else "Anonymous"
        return f"Chat session {self.session_id} - {user_info}"

    class Meta:
        db_table = 'chat_sessions'
        ordering = ['-updated_at']


class ChatMessage(models.Model):
    """Model to store individual chat messages"""
    
    MESSAGE_TYPE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES)
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)  # For storing additional context
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}..."

    class Meta:
        db_table = 'chat_messages'
        ordering = ['timestamp']


class UserRecommendation(models.Model):
    """Model to store AI-generated recommendations for users"""
    
    RECOMMENDATION_TYPE_CHOICES = [
        ('course', 'Course Recommendation'),
        ('university', 'University Recommendation'),
        ('field', 'Field of Study Recommendation'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    recommendation_type = models.CharField(max_length=20, choices=RECOMMENDATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    confidence_score = models.DecimalField(max_digits=3, decimal_places=2)  # 0.00 to 1.00
    reasoning = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)  # Store course/university IDs, etc.
    is_dismissed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recommendation_type} for {self.user.email}: {self.title}"

    class Meta:
        db_table = 'user_recommendations'
        ordering = ['-confidence_score', '-created_at']


class SmartSearchQuery(models.Model):
    """Model to store and analyze smart search queries"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='smart_searches', blank=True, null=True)
    original_query = models.TextField()
    processed_query = models.TextField()
    extracted_filters = models.JSONField(default=dict, blank=True)
    suggested_courses = models.ManyToManyField('courses.Course', blank=True)
    confidence_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    processing_time = models.DecimalField(max_digits=5, decimal_places=3, default=0.000)  # in seconds
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_info = self.user.email if self.user else "Anonymous"
        return f"Smart search by {user_info}: {self.original_query[:50]}"

    class Meta:
        db_table = 'smart_search_queries'
        ordering = ['-created_at']