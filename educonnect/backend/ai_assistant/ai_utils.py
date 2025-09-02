from django.conf import settings
from django.db.models import Q
from django.utils import timezone
import openai
import json
import time

from .models import ChatSession, ChatMessage, UserRecommendation
from courses.models import Course


def generate_ai_response(message, session):
    """Generate AI response using OpenAI or fallback logic"""
    if not settings.OPENAI_API_KEY:
        return generate_fallback_response(message)
    
    try:
        # Get conversation history
        messages = session.messages.order_by('timestamp')
        conversation_history = []
        
        for msg in messages[-10:]:  # Last 10 messages for context
            role = 'user' if msg.message_type == 'user' else 'assistant'
            conversation_history.append({
                'role': role,
                'content': msg.content
            })
        
        # Add system prompt
        system_prompt = """You are an AI assistant for EduConnect, a platform that helps students find international university courses. 
        You can help with:
        - Finding courses and universities
        - Comparing educational programs
        - Providing information about admission requirements
        - Suggesting study destinations
        - Answering questions about higher education
        
        Be helpful, informative, and encourage users to explore the platform's features."""
        
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt}
            ] + conversation_history,
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return generate_fallback_response(message)


def generate_fallback_response(message):
    """Generate fallback response when AI is not available"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['course', 'program', 'study']):
        return "I can help you find courses! Try using our search feature to filter by country, field of study, or budget range."
    
    elif any(word in message_lower for word in ['university', 'college', 'school']):
        return "Looking for universities? You can browse our university directory and filter by country, ranking, or specific programs offered."
    
    elif any(word in message_lower for word in ['fee', 'cost', 'tuition', 'price']):
        return "For tuition information, you can use our fee range filters in the search. Each course listing includes detailed fee information."
    
    elif any(word in message_lower for word in ['admission', 'requirement', 'apply']):
        return "Each course page includes detailed admission requirements. You can also save courses to compare requirements side by side."
    
    else:
        return "I'm here to help you find the perfect course! Try asking about specific countries, fields of study, or use our search feature to explore options."


def process_smart_search(query, additional_filters=None):
    """Process natural language search query"""
    if not settings.OPENAI_API_KEY:
        return process_fallback_search(query, additional_filters)
    
    try:
        # Use AI to extract search intent and filters
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        prompt = f"""
        Extract search filters from this natural language query about university courses:
        "{query}"
        
        Return a JSON object with these possible fields:
        - level: bachelor, master, phd, diploma, certificate
        - field_of_study: specific field name
        - country: country name
        - min_fee: minimum tuition fee
        - max_fee: maximum tuition fee
        - is_online: true/false
        - keywords: array of important keywords
        
        Only include fields that are clearly mentioned or implied in the query.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.3
        )
        
        extracted_filters = json.loads(response.choices[0].message.content)
        
        # Apply filters to find courses
        queryset = Course.objects.filter(is_active=True)
        
        if extracted_filters.get('level'):
            queryset = queryset.filter(level=extracted_filters['level'])
        
        if extracted_filters.get('field_of_study'):
            queryset = queryset.filter(field_of_study__icontains=extracted_filters['field_of_study'])
        
        if extracted_filters.get('country'):
            queryset = queryset.filter(university__country__icontains=extracted_filters['country'])
        
        if extracted_filters.get('min_fee'):
            queryset = queryset.filter(tuition_fee__gte=extracted_filters['min_fee'])
        
        if extracted_filters.get('max_fee'):
            queryset = queryset.filter(tuition_fee__lte=extracted_filters['max_fee'])
        
        if extracted_filters.get('is_online') is not None:
            queryset = queryset.filter(is_online=extracted_filters['is_online'])
        
        # Apply additional filters
        if additional_filters:
            for key, value in additional_filters.items():
                if hasattr(Course, key):
                    queryset = queryset.filter(**{key: value})
        
        courses = queryset.order_by('-popularity_score')[:20]
        
        return {
            'processed_query': query,
            'filters': extracted_filters,
            'course_ids': [course.id for course in courses],
            'confidence': 0.85
        }
    
    except Exception as e:
        return process_fallback_search(query, additional_filters)


def process_fallback_search(query, additional_filters=None):
    """Fallback search processing without AI"""
    query_lower = query.lower()
    filters = {}
    
    # Simple keyword extraction
    if 'bachelor' in query_lower:
        filters['level'] = 'bachelor'
    elif 'master' in query_lower:
        filters['level'] = 'master'
    elif 'phd' in query_lower:
        filters['level'] = 'phd'
    
    # Field detection
    fields_map = {
        'computer science': 'Computer Science',
        'engineering': 'Engineering',
        'business': 'Business',
        'medicine': 'Medicine',
        'law': 'Law',
        'arts': 'Arts',
    }
    
    for keyword, field in fields_map.items():
        if keyword in query_lower:
            filters['field_of_study'] = field
            break
    
    # Country detection
    countries = ['usa', 'uk', 'canada', 'australia', 'germany', 'france', 'netherlands']
    for country in countries:
        if country in query_lower:
            filters['country'] = country.title()
            break
    
    # Search courses
    queryset = Course.objects.filter(is_active=True)
    
    # Apply extracted filters
    for key, value in filters.items():
        if key == 'field_of_study':
            queryset = queryset.filter(field_of_study__icontains=value)
        elif key == 'country':
            queryset = queryset.filter(university__country__icontains=value)
        else:
            queryset = queryset.filter(**{key: value})
    
    # Text search
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(university__name__icontains=query)
        )
    
    courses = queryset.order_by('-popularity_score')[:20]
    
    return {
        'processed_query': query,
        'filters': filters,
        'course_ids': [course.id for course in courses],
        'confidence': 0.60
    }


def create_user_recommendations(user):
    """Generate personalized recommendations for a user"""
    recommendations = []
    
    # Based on user preferences
    if user.preferred_study_level:
        courses = Course.objects.filter(
            level=user.preferred_study_level,
            is_active=True
        ).order_by('-popularity_score')[:5]
        
        for course in courses:
            recommendation = UserRecommendation.objects.create(
                user=user,
                recommendation_type='course',
                title=f"Recommended {course.level}: {course.title}",
                description=f"Based on your preferred study level ({course.level})",
                confidence_score=0.80,
                reasoning=f"Matches your preferred study level and is highly rated",
                metadata={'course_id': course.id}
            )
            recommendations.append(recommendation)
    
    return recommendations