from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class University(models.Model):
    """Model representing a university"""
    
    name = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    website = models.URLField()
    logo = models.ImageField(upload_to='university_logos/', blank=True, null=True)
    description = models.TextField(blank=True)
    ranking_global = models.PositiveIntegerField(blank=True, null=True)
    ranking_national = models.PositiveIntegerField(blank=True, null=True)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    student_population = models.PositiveIntegerField(blank=True, null=True)
    acceptance_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.country}"

    class Meta:
        db_table = 'universities'
        ordering = ['name']


class Course(models.Model):
    """Model representing a course/program"""
    
    LEVEL_CHOICES = [
        ('bachelor', 'Bachelor\'s'),
        ('master', 'Master\'s'),
        ('phd', 'PhD'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ]
    
    DURATION_UNIT_CHOICES = [
        ('months', 'Months'),
        ('years', 'Years'),
        ('weeks', 'Weeks'),
    ]
    
    title = models.CharField(max_length=300)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='courses')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    field_of_study = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_value = models.PositiveIntegerField()
    duration_unit = models.CharField(max_length=10, choices=DURATION_UNIT_CHOICES, default='years')
    tuition_fee = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    application_fee = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    admission_requirements = models.TextField(blank=True)
    language_requirements = models.TextField(blank=True)
    prerequisites = models.TextField(blank=True)
    career_prospects = models.TextField(blank=True)
    course_url = models.URLField(blank=True)
    application_deadline = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    is_part_time = models.BooleanField(default=False)
    credits = models.PositiveIntegerField(blank=True, null=True)
    gpa_requirement = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(4)]
    )
    is_active = models.BooleanField(default=True)
    popularity_score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.university.name}"

    @property
    def duration_display(self):
        return f"{self.duration_value} {self.duration_unit}"

    class Meta:
        db_table = 'courses'
        ordering = ['-popularity_score', 'title']
        indexes = [
            models.Index(fields=['level', 'field_of_study']),
            models.Index(fields=['tuition_fee']),
            models.Index(fields=['university', 'level']),
        ]


class SavedCourse(models.Model):
    """Model for user's saved courses"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='saved_by_users')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} saved {self.course.title}"

    class Meta:
        db_table = 'saved_courses'
        unique_together = ['user', 'course']


class SearchLog(models.Model):
    """Model to track user search queries for analytics and recommendations"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_logs', blank=True, null=True)
    query = models.TextField()
    filters_applied = models.JSONField(default=dict, blank=True)
    results_count = models.PositiveIntegerField(default=0)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_info = self.user.email if self.user else "Anonymous"
        return f"Search by {user_info}: {self.query[:50]}"

    class Meta:
        db_table = 'search_logs'
        ordering = ['-timestamp']


class CourseReview(models.Model):
    """Model for course reviews by users"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_verified = models.BooleanField(default=False)  # For verified students
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.course.title} ({self.rating}/5)"

    class Meta:
        db_table = 'course_reviews'
        unique_together = ['user', 'course']
        ordering = ['-created_at']


class UniversityContact(models.Model):
    """Model for university contact information"""
    
    university = models.OneToOneField(University, on_delete=models.CASCADE, related_name='contact_info')
    admissions_email = models.EmailField(blank=True)
    admissions_phone = models.CharField(max_length=20, blank=True)
    international_office_email = models.EmailField(blank=True)
    international_office_phone = models.CharField(max_length=20, blank=True)
    financial_aid_email = models.EmailField(blank=True)
    financial_aid_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contact info for {self.university.name}"

    class Meta:
        db_table = 'university_contacts'