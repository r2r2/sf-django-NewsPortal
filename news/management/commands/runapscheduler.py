import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from NewsPortal.settings import DEFAULT_FROM_EMAIL
from news.models import Post, Category

logger = logging.getLogger(__name__)


def send_mail_to_subs():
    """Еженедельная отправка подписчикам списка новых статей"""

    post_list = Post.objects.filter(date_creation__range=[datetime.now() - timedelta(days=7), datetime.now()])
    categories = Category.objects.all()
    for category in categories:
        subs = category.subscribers.filter(category__category_name=category).distinct()
        posts = post_list.filter(category__category_name=category)
        for user in subs:
            html_content = render_to_string(
                'news/weekly_subs_email.html',
                {
                    'posts': posts,
                    'user': user,
                    'category': category,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f"NewsPortal: Зацени новые статьи за неделю",
                from_email=DEFAULT_FROM_EMAIL,
                to=[user.email],
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            send_mail_to_subs,
            trigger=CronTrigger(day="*/7"),
            id="send_mail_to_subs",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_mail_to_subs'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
