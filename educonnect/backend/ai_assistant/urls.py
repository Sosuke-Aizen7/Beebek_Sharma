from django.urls import path
from . import views, api_views

urlpatterns = [
    path('chat/sessions/', views.ChatSessionListView.as_view(), name='chat-sessions'),
    path('chat/sessions/<str:session_id>/', views.ChatSessionDetailView.as_view(), name='chat-session-detail'),
    path('chat/query/', api_views.chat_query, name='chat-query'),
    path('search/smart/', api_views.smart_search, name='smart-search'),
    path('recommendations/', views.UserRecommendationListView.as_view(), name='user-recommendations'),
    path('recommendations/generate/', api_views.generate_recommendations, name='generate-recommendations'),
    path('recommendations/<int:recommendation_id>/dismiss/', api_views.dismiss_recommendation, name='dismiss-recommendation'),
]