from rest_framework import serializers
from .models import University, Course, SavedCourse, SearchLog, CourseReview, UniversityContact


class UniversityContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityContact
        fields = '__all__'


class UniversitySerializer(serializers.ModelSerializer):
    contact_info = UniversityContactSerializer(read_only=True)
    courses_count = serializers.SerializerMethodField()

    class Meta:
        model = University
        fields = '__all__'

    def get_courses_count(self, obj):
        return obj.courses.filter(is_active=True).count()


class UniversityListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for university lists"""
    courses_count = serializers.SerializerMethodField()

    class Meta:
        model = University
        fields = ('id', 'name', 'country', 'city', 'logo', 'ranking_global', 'courses_count')

    def get_courses_count(self, obj):
        return obj.courses.filter(is_active=True).count()


class CourseSerializer(serializers.ModelSerializer):
    university = UniversityListSerializer(read_only=True)
    duration_display = serializers.ReadOnlyField()
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return None

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedCourse.objects.filter(user=request.user, course=obj).exists()
        return False


class CourseListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for course lists"""
    university_name = serializers.CharField(source='university.name', read_only=True)
    university_country = serializers.CharField(source='university.country', read_only=True)
    duration_display = serializers.ReadOnlyField()
    average_rating = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'id', 'title', 'university_name', 'university_country', 'level', 
            'field_of_study', 'duration_display', 'tuition_fee', 'currency',
            'is_online', 'is_part_time', 'average_rating', 'is_saved'
        )

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 1)
        return None

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedCourse.objects.filter(user=request.user, course=obj).exists()
        return False


class SavedCourseSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = SavedCourse
        fields = ('id', 'course', 'course_id', 'notes', 'created_at')
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CourseReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = CourseReview
        fields = ('id', 'user_name', 'course_title', 'rating', 'title', 'content', 'is_verified', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user_name', 'course_title', 'is_verified', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CourseComparisonSerializer(serializers.ModelSerializer):
    """Serializer for course comparison feature"""
    university = UniversityListSerializer(read_only=True)
    duration_display = serializers.ReadOnlyField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'id', 'title', 'university', 'level', 'field_of_study',
            'duration_display', 'tuition_fee', 'currency', 'application_fee',
            'admission_requirements', 'language_requirements', 'gpa_requirement',
            'is_online', 'is_part_time', 'course_url', 'average_rating'
        )

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 1)
        return None


class SearchLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchLog
        fields = ('query', 'filters_applied', 'results_count')
        read_only_fields = ('timestamp',)