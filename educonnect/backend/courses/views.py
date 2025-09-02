from rest_framework import generics, filters, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg, Count
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import University, Course, SavedCourse, SearchLog, CourseReview
from .serializers import (
    UniversitySerializer, UniversityListSerializer, CourseSerializer,
    CourseListSerializer, SavedCourseSerializer, CourseReviewSerializer,
    CourseComparisonSerializer, SearchLogSerializer
)


class UniversityListView(generics.ListAPIView):
    queryset = University.objects.filter(is_active=True)
    serializer_class = UniversityListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country']
    search_fields = ['name', 'country', 'city']
    ordering_fields = ['name', 'ranking_global', 'student_population']
    ordering = ['ranking_global']


class UniversityDetailView(generics.RetrieveAPIView):
    queryset = University.objects.filter(is_active=True)
    serializer_class = UniversitySerializer
    permission_classes = [AllowAny]


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.filter(is_active=True).select_related('university')
    serializer_class = CourseListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['level', 'field_of_study', 'university__country', 'is_online', 'is_part_time', 'currency']
    search_fields = ['title', 'field_of_study', 'university__name', 'description']
    ordering_fields = ['title', 'tuition_fee', 'duration_value', 'popularity_score']
    ordering = ['-popularity_score']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Custom filters
        min_fee = self.request.query_params.get('min_fee')
        max_fee = self.request.query_params.get('max_fee')
        countries = self.request.query_params.getlist('countries')
        levels = self.request.query_params.getlist('levels')
        fields = self.request.query_params.getlist('fields')
        
        if min_fee:
            queryset = queryset.filter(tuition_fee__gte=min_fee)
        if max_fee:
            queryset = queryset.filter(tuition_fee__lte=max_fee)
        if countries:
            queryset = queryset.filter(university__country__in=countries)
        if levels:
            queryset = queryset.filter(level__in=levels)
        if fields:
            queryset = queryset.filter(field_of_study__in=fields)
            
        return queryset

    def list(self, request, *args, **kwargs):
        # Log search query
        query = request.query_params.get('search', '')
        if query:
            SearchLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                query=query,
                filters_applied=dict(request.query_params),
                results_count=self.get_queryset().count(),
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        
        return super().list(request, *args, **kwargs)


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.filter(is_active=True).select_related('university')
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]


class SavedCourseListView(generics.ListCreateAPIView):
    serializer_class = SavedCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavedCourse.objects.filter(user=self.request.user).select_related('course', 'course__university')


class SavedCourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SavedCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavedCourse.objects.filter(user=self.request.user)


class CourseReviewListView(generics.ListCreateAPIView):
    serializer_class = CourseReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return CourseReview.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        serializer.save(course=course)


@api_view(['POST'])
@permission_classes([AllowAny])
def course_comparison(request):
    """Compare multiple courses side by side"""
    course_ids = request.data.get('course_ids', [])
    
    if not course_ids or len(course_ids) < 2:
        return Response(
            {'error': 'At least 2 course IDs are required for comparison'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if len(course_ids) > 5:
        return Response(
            {'error': 'Maximum 5 courses can be compared at once'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    courses = Course.objects.filter(id__in=course_ids, is_active=True).select_related('university')
    serializer = CourseComparisonSerializer(courses, many=True, context={'request': request})
    
    return Response({
        'courses': serializer.data,
        'comparison_date': timezone.now()
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def course_statistics(request):
    """Get general statistics about courses and universities"""
    stats = {
        'total_universities': University.objects.filter(is_active=True).count(),
        'total_courses': Course.objects.filter(is_active=True).count(),
        'countries_count': University.objects.filter(is_active=True).values('country').distinct().count(),
        'fields_of_study': Course.objects.filter(is_active=True).values('field_of_study').distinct().count(),
        'average_tuition_fee': Course.objects.filter(is_active=True).aggregate(avg_fee=Avg('tuition_fee'))['avg_fee'],
        'level_distribution': {},
        'top_countries': []
    }
    
    # Level distribution
    for level, _ in Course.LEVEL_CHOICES:
        count = Course.objects.filter(level=level, is_active=True).count()
        stats['level_distribution'][level] = count
    
    # Top countries by course count
    top_countries = University.objects.filter(is_active=True).values('country').annotate(
        course_count=Count('courses', filter=Q(courses__is_active=True))
    ).order_by('-course_count')[:10]
    
    stats['top_countries'] = list(top_countries)
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([AllowAny])
def popular_courses(request):
    """Get popular/trending courses"""
    courses = Course.objects.filter(is_active=True).select_related('university').order_by('-popularity_score')[:20]
    serializer = CourseListSerializer(courses, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def featured_universities(request):
    """Get featured universities"""
    universities = University.objects.filter(is_active=True).order_by('ranking_global')[:10]
    serializer = UniversityListSerializer(universities, many=True)
    return Response(serializer.data)