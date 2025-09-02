from django.db import models
from courses.models import University, Course


class ScrapingJob(models.Model):
    """Model to track web scraping jobs"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='scraping_jobs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    courses_found = models.PositiveIntegerField(default=0)
    courses_updated = models.PositiveIntegerField(default=0)
    courses_created = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    log_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scraping job for {self.university.name} - {self.status}"

    class Meta:
        db_table = 'scraping_jobs'
        ordering = ['-created_at']


class ScrapingRule(models.Model):
    """Model to store scraping rules for different universities"""
    
    university = models.OneToOneField(University, on_delete=models.CASCADE, related_name='scraping_rule')
    base_url = models.URLField()
    course_list_selector = models.TextField(help_text="CSS selector for course list")
    course_title_selector = models.TextField(help_text="CSS selector for course title")
    course_fee_selector = models.TextField(help_text="CSS selector for course fee")
    course_duration_selector = models.TextField(help_text="CSS selector for course duration")
    course_level_selector = models.TextField(help_text="CSS selector for course level", blank=True)
    course_description_selector = models.TextField(help_text="CSS selector for course description", blank=True)
    course_requirements_selector = models.TextField(help_text="CSS selector for requirements", blank=True)
    pagination_selector = models.TextField(help_text="CSS selector for pagination", blank=True)
    wait_time = models.PositiveIntegerField(default=2, help_text="Wait time between requests (seconds)")
    use_selenium = models.BooleanField(default=False, help_text="Use Selenium for JavaScript-heavy sites")
    custom_headers = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Scraping rule for {self.university.name}"

    class Meta:
        db_table = 'scraping_rules'


class ScrapedData(models.Model):
    """Model to store raw scraped data before processing"""
    
    scraping_job = models.ForeignKey(ScrapingJob, on_delete=models.CASCADE, related_name='scraped_data')
    source_url = models.URLField()
    raw_data = models.JSONField()
    processed = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scraped data from {self.source_url}"

    class Meta:
        db_table = 'scraped_data'
        ordering = ['-created_at']