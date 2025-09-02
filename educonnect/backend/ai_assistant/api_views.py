from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.utils import timezone
import uuid
import time

from .models import ChatSession, ChatMessage, SmartSearchQuery
from .serializers import ChatQuerySerializer, SmartSearchRequestSerializer
from .ai_utils import generate_ai_response, process_smart_search, create_user_recommendations
from courses.serializers import CourseListSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def chat_query(request):
    """Handle chat queries with AI assistant"""
    serializer = ChatQuerySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    message = serializer.validated_data['message']
    session_id = serializer.validated_data.get('session_id')
    
    # Get or create chat session
    if session_id:
        try:
            if request.user.is_authenticated:
                session = ChatSession.objects.get(session_id=session_id, user=request.user)
            else:
                session = ChatSession.objects.get(session_id=session_id, user=None)
        except ChatSession.DoesNotExist:
            session = ChatSession.objects.create(
                session_id=str(uuid.uuid4()),
                user=request.user if request.user.is_authenticated else None
            )
    else:
        session = ChatSession.objects.create(
            session_id=str(uuid.uuid4()),
            user=request.user if request.user.is_authenticated else None
        )
    
    # Save user message
    ChatMessage.objects.create(
        session=session,
        message_type='user',
        content=message
    )
    
    # Generate AI response
    try:
        ai_response = generate_ai_response(message, session)
        
        # Save AI response
        ChatMessage.objects.create(
            session=session,
            message_type='assistant',
            content=ai_response
        )
        
        # Update session title if it's the first exchange
        if not session.title:
            session.title = message[:50] + '...' if len(message) > 50 else message
            session.save()
        
        return Response({
            'session_id': session.session_id,
            'response': ai_response,
            'timestamp': timezone.now()
        })
    
    except Exception as e:
        # Save error message
        error_msg = "I'm sorry, I'm having trouble processing your request right now. Please try again later."
        ChatMessage.objects.create(
            session=session,
            message_type='assistant',
            content=error_msg,
            metadata={'error': str(e)}
        )
        
        return Response({
            'session_id': session.session_id,
            'response': error_msg,
            'timestamp': timezone.now()
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def smart_search(request):
    """Handle smart/natural language search queries"""
    serializer = SmartSearchRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    query = serializer.validated_data['query']
    additional_filters = serializer.validated_data.get('filters', {})
    
    start_time = time.time()
    
    try:
        # Process the natural language query
        processed_result = process_smart_search(query, additional_filters)
        
        processing_time = time.time() - start_time
        
        # Create smart search record
        smart_search = SmartSearchQuery.objects.create(
            user=request.user if request.user.is_authenticated else None,
            original_query=query,
            processed_query=processed_result['processed_query'],
            extracted_filters=processed_result['filters'],
            confidence_score=processed_result['confidence'],
            processing_time=processing_time
        )
        
        # Add suggested courses
        if processed_result['course_ids']:
            courses = Course.objects.filter(id__in=processed_result['course_ids'])
            smart_search.suggested_courses.set(courses)
        
        return Response({
            'query_id': smart_search.id,
            'processed_query': processed_result['processed_query'],
            'extracted_filters': processed_result['filters'],
            'suggested_courses': CourseListSerializer(
                smart_search.suggested_courses.all(), 
                many=True, 
                context={'request': request}
            ).data,
            'confidence': processed_result['confidence'],
            'processing_time': processing_time
        })
    
    except Exception as e:
        return Response(
            {'error': 'Failed to process search query', 'details': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dismiss_recommendation(request, recommendation_id):
    """Dismiss a recommendation"""
    try:
        recommendation = UserRecommendation.objects.get(
            id=recommendation_id, 
            user=request.user
        )
        recommendation.is_dismissed = True
        recommendation.save()
        return Response({'message': 'Recommendation dismissed'})
    except UserRecommendation.DoesNotExist:
        return Response(
            {'error': 'Recommendation not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_recommendations(request):
    """Generate new recommendations for the user"""
    try:
        recommendations = create_user_recommendations(request.user)
        from .serializers import UserRecommendationSerializer
        serializer = UserRecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': 'Failed to generate recommendations', 'details': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )