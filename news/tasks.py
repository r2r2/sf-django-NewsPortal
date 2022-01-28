from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string

from NewsPortal.settings import DEFAULT_FROM_EMAIL
from news.models import Post, Category, PostCategory


@shared_task
def notify_subscribers(pid):
    """Информируем пользователей о новой статье в их подписках"""
    categories = PostCategory.objects.filter(post_id=pid)
    for category in categories:
        if category.subscribers:
            sendNewPost(category.pk, pid)


def sendNewPost(category_id, pid):
    """Рассылка оповещений о новой статье"""
    category = Category.objects.get(id=category_id)
    post = Post.objects.get(id=pid)
    for user in category.subscribers.all():
        html_content = render_to_string(
            'news/subscription_created.html',
            {
                'post': post,
                'user': user,
                'category': category,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f"NewsPortal: {post.post_title}",
            body=post.post_text,
            from_email=DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    return redirect('news:news')


@shared_task
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
