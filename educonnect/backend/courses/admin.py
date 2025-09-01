from django.contrib import admin
from .models import University, Course, SavedCourse, SearchLog, CourseReview, UniversityContact


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'city', 'ranking_global', 'student_population', 'is_active')
    list_filter = ('country', 'is_active', 'established_year')
    search_fields = ('name', 'country', 'city')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'country', 'city', 'website', 'logo', 'description')
        }),
        ('Rankings & Stats', {
            'fields': ('ranking_global', 'ranking_national', 'established_year', 'student_population', 'acceptance_rate')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'address')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'university', 'level', 'field_of_study', 'tuition_fee', 'currency', 'is_active')
    list_filter = ('level', 'field_of_study', 'currency', 'is_online', 'is_part_time', 'is_active')
    search_fields = ('title', 'university__name', 'field_of_study', 'description')
    ordering = ('-popularity_score', 'title')
    readonly_fields = ('created_at', 'updated_at', 'popularity_score')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'university', 'level', 'field_of_study', 'description')
        }),
        ('Duration & Fees', {
            'fields': ('duration_value', 'duration_unit', 'tuition_fee', 'currency', 'application_fee')
        }),
        ('Requirements', {
            'fields': ('admission_requirements', 'language_requirements', 'prerequisites', 'gpa_requirement', 'credits')
        }),
        ('Dates & Links', {
            'fields': ('application_deadline', 'start_date', 'course_url')
        }),
        ('Options', {
            'fields': ('is_online', 'is_part_time', 'is_active')
        }),
        ('Additional Info', {
            'fields': ('career_prospects', 'popularity_score')
        }),
    )


@admin.register(SavedCourse)
class SavedCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'course__title', 'course__university__name')
    ordering = ('-created_at',)


@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'results_count', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__email', 'query')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'title', 'is_verified', 'created_at')
    list_filter = ('rating', 'is_verified', 'created_at')
    search_fields = ('user__email', 'course__title', 'title', 'content')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UniversityContact)
class UniversityContactAdmin(admin.ModelAdmin):
    list_display = ('university', 'admissions_email', 'international_office_email')
    search_fields = ('university__name', 'admissions_email', 'international_office_email')
    readonly_fields = ('created_at', 'updated_at')