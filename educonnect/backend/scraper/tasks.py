from celery import shared_task
from django.utils import timezone
from .scraper_engine import run_scraping_job, run_all_scraping_jobs
from .models import ScrapingJob


@shared_task
def scrape_university_courses(university_id):
    """Celery task to scrape courses for a specific university"""
    try:
        job = run_scraping_job(university_id)
        return {
            'status': 'success',
            'job_id': job.id,
            'courses_found': job.courses_found,
            'courses_created': job.courses_created,
            'courses_updated': job.courses_updated
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


@shared_task
def scrape_all_universities():
    """Celery task to scrape courses from all universities"""
    try:
        results = run_all_scraping_jobs()
        return {
            'status': 'success',
            'results': results,
            'timestamp': timezone.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


@shared_task
def cleanup_old_scraping_jobs():
    """Clean up old scraping jobs and data"""
    from datetime import timedelta
    
    # Delete jobs older than 30 days
    cutoff_date = timezone.now() - timedelta(days=30)
    old_jobs = ScrapingJob.objects.filter(created_at__lt=cutoff_date)
    
    deleted_count = old_jobs.count()
    old_jobs.delete()
    
    return {
        'status': 'success',
        'deleted_jobs': deleted_count
    }