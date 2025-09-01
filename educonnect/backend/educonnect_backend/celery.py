import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educonnect_backend.settings')

app = Celery('educonnect_backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'scrape-all-universities-daily': {
        'task': 'scraper.tasks.scrape_all_universities',
        'schedule': 86400.0,  # 24 hours
    },
    'cleanup-old-jobs-weekly': {
        'task': 'scraper.tasks.cleanup_old_scraping_jobs',
        'schedule': 604800.0,  # 7 days
    },
}

app.conf.timezone = 'UTC'