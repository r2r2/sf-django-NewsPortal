from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.shortcuts import redirect
from django.template.loader import render_to_string


from NewsPortal.settings import DEFAULT_FROM_EMAIL
from news.models import Post, Category
from pytils.translit import slugify


# @receiver(m2m_changed, sender=Post.category.through)
# def notify_subscribers(sender, instance, **kwargs):
#     """Информируем пользователей о новой статье в их подписках"""
#     post_info = instance.category.all()
#     for category in post_info:
#         if category.subscribers:
#             sendNewPost(category.pk, instance.pk)


def sendNewPost(category_id, instance_id):
    """Рассылка оповещений о новой статье"""
    category = Category.objects.get(id=category_id)
    post = Post.objects.get(id=instance_id)
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


# @receiver(pre_save, sender=Post)
# def populate_slug(sender, instance, *args, **kwargs):
#     """Генерируем slug для поста"""
#     if not instance.url:
#         instance.url = slugify(instance.post_title)
