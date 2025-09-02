from django.contrib import admin
from .models import ScrapingJob, ScrapingRule, ScrapedData


@admin.register(ScrapingJob)
class ScrapingJobAdmin(admin.ModelAdmin):
    list_display = ('university', 'status', 'courses_found', 'courses_created', 'courses_updated', 'started_at', 'completed_at')
    list_filter = ('status', 'started_at', 'completed_at')
    search_fields = ('university__name',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'courses_found', 'courses_created', 'courses_updated')


@admin.register(ScrapingRule)
class ScrapingRuleAdmin(admin.ModelAdmin):
    list_display = ('university', 'base_url', 'use_selenium', 'wait_time', 'is_active')
    list_filter = ('use_selenium', 'is_active', 'created_at')
    search_fields = ('university__name', 'base_url')
    ordering = ('university__name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ScrapedData)
class ScrapedDataAdmin(admin.ModelAdmin):
    list_display = ('scraping_job', 'source_url', 'processed', 'course', 'created_at')
    list_filter = ('processed', 'created_at')
    search_fields = ('source_url', 'scraping_job__university__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)