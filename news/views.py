
from django.views.generic import ListView, DetailView

from news.models import Post


class NewsList(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/detail_news.html'
    context_object_name = 'detail_news'
