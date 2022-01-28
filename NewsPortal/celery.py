import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'notify_subs_about_new_article': {
        'task': 'news.tasks.notify_subscribers',

    }
}

app.conf.beat_schedule = {
    'notify_subs_every_week': {
        'task': 'news.tasks.send_mail_to_subs',
        'schedule': crontab(day_of_week='monday', hour=8, minute=0),
    }
}
