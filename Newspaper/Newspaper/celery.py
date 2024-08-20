import os
from celery import Celery
from celery.schedules import crontab, solar


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Newspaper.settings')

app = Celery('Newspaper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_monday_8pm': {
    'task': 'news.tasks.post_created',
    'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

app.conf.beat_schedule = {
    'action_monday_8pm': {
    'task': 'news.tasks.news_of_week',
    'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

# app.conf.beat_schedule = {
#     'action_monday_8pm': {
#     'task': 'action',
#     'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
#     'args': (args)
#     },
# }