import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .tasks import *
from NewsPortal.settings import DEFAULT_FROM_EMAIL
from .filters import PostFilter
from .forms import PostForm
from .models import Post, UserCategorySub, Category


logger = logging.getLogger(__name__)


class NewsList(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    ordering = ['-id']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(NewsList, self).get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/detail_news.html'
    context_object_name = 'detail_news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def get_object(self, *args, **kwargs):
        # obj = cache.get(self.kwargs["pk"])  # If the object doesn’t exist in the cache, cache.get() returns None
        #
        # if not obj:
        #     obj = super().get_object(*args, **kwargs)
        #     cache.set(self.kwargs["pk"], obj)

        obj = super().get_object(*args, **kwargs)
        cache.get_or_set(self.kwargs["pk"], obj)

        return obj

class NewsSearch(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'news'
    ordering = ['-id']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(NewsSearch, self).get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        # context['category'] = self.request.GET.get('category', 0)
        # context['is_sub'] = Category.objects.filter(subscribers=self.request.user.id)
        return context


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'news/create_news.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save()
        post.save()
        # notify_subscribers.apply_async([post.pk], countdown=5)  # После создания отправляем подписчикам письмо через Celery
        notify_subscribers.delay(post.pk)  # После создания отправляем подписчикам письмо через Celery
        return redirect(f'/news/{post.pk}')


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'news/create_news.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'news/delete_news.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post',)


class SubscribeView(View):
    """Подписка на рассылку по категориям"""

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        cat_sub = Category.objects.filter(subscribers__email=self.request.user.email).distinct()  # Берем все текущие подписки пользователя
        return render(request, 'news/subscribe.html', context={'categories': categories, 'cat_sub': cat_sub})

    def post(self, request, *args, **kwargs):
        category_name = request.POST.getlist('category_name')
        UserCategorySub.objects.filter(user=request.user).delete()  # Удаляем все подписки этого пользователя из БД

        # Записываем подписки пользователя в БД
        for cat in category_name:
            category = Category.objects.get(category_name=cat)
            subscriber = UserCategorySub(
                user=request.user,
                category=category,
            )
            subscriber.save()

        # send_mail(
        #     subject=f"Спасибо за подписку на NewsPortal",
        #     message=f"Уважаемый {self.request.user.username}, Вы подписались на категории {subscriber.category}",
        #     from_email=DEFAULT_FROM_EMAIL,
        #     recipient_list=[request.user.email]
        # )
        return redirect('news:news')


@login_required
def upgrade_to_author(request):
    """Добавление в группу Authors"""

    user = request.user
    author_group = Group.objects.get(name='authors')
    common_group = Group.objects.get(name='common')  # Если логинится через Гугл
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
        common_group.user_set.add(user)  # Если логинится через Гугл
    return redirect('news:news')






















