from django.urls import path
from . import views

urlpatterns = [
    path('universities/', views.UniversityListView.as_view(), name='university-list'),
    path('universities/<int:pk>/', views.UniversityDetailView.as_view(), name='university-detail'),
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:course_id>/reviews/', views.CourseReviewListView.as_view(), name='course-reviews'),
    path('saved-courses/', views.SavedCourseListView.as_view(), name='saved-courses'),
    path('saved-courses/<int:pk>/', views.SavedCourseDetailView.as_view(), name='saved-course-detail'),
    path('compare/', views.course_comparison, name='course-comparison'),
    path('statistics/', views.course_statistics, name='course-statistics'),
    path('popular/', views.popular_courses, name='popular-courses'),
    path('featured-universities/', views.featured_universities, name='featured-universities'),
]