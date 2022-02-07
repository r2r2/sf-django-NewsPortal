import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .tasks import notify_subscribers, sendNewPost, send_mail_to_subs
from NewsPortal.settings import DEFAULT_FROM_EMAIL
from .filters import PostFilter
from .forms import PostForm, CommentForm, RatingForm
from .models import Post, UserCategorySub, Category, Author, Rating, RatingStar

logger = logging.getLogger(__name__)


# class IsNotAuthor:
#     """Проверяем является ли пользователь автором"""
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
#         context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
#         context['star_form'] = RatingForm()
#         return context


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
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['star_form'] = RatingForm()
        context['set_rating'] = Rating.objects.filter(ip=self.request.META.get('REMOTE_ADDR')).exists()
        context['rating'] = Rating.objects.filter(ip=self.request.META.get('REMOTE_ADDR', None))
        if self.request.user.is_authenticated:
            context['author'] = Author.objects.filter(author_name=self.request.user).filter(post__url=self.kwargs['slug'])
        context['form'] = CommentForm()
        return context

    def get_object(self, *args, **kwargs):
        """Берем из кэша"""
        obj = super().get_object(*args, **kwargs)
        cache_obj = cache.get_or_set(self.kwargs["slug"], obj)
        return cache_obj


class NewsSearch(LoginRequiredMixin, ListView):
    """Страница поиска с фильтрами"""
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'news'
    ordering = ['-id']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(NewsSearch, self).get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Добавить статью"""
    template_name = 'news/create_news.html'
    form_class = PostForm
    permission_required = ('news.add_post',)
    slug_field = 'url'

    def form_valid(self, form):
        post = form.save(commit=False)
        try:
            author = Author.objects.get(author_name=self.request.user)
        except Author.DoesNotExist:
            author = Author.objects.create(author_name=self.request.user)
        post.author = author
        post.save()
        # notify_subscribers.apply_async([post.pk], countdown=5)  # После создания отправляем подписчикам письмо через Celery
        notify_subscribers.delay(post.pk)  # После создания отправляем подписчикам письмо через Celery
        return redirect(post.get_absolute_url())


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'news/create_news.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return Post.objects.get(url=slug)


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'news/delete_news.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post',)
    slug_field = 'url'


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


class AddComment(View):
    """Комментарий"""
    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = Post.objects.get(id=pk)
        user = request.user
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.post = post
            form.user = user
            form.save()
        return redirect(post.get_absolute_url())


class AddStarRating(View):
    """Добавление рейтинга статье"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                post_id=int(request.POST.get("post")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)















