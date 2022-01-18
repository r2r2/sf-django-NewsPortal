
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from news.filters import PostFilter
from news.forms import PostForm
from news.models import Post


class NewsList(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    ordering = ['-id']
    paginate_by = 10


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/detail_news.html'
    context_object_name = 'detail_news'


class NewsSearch(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'news'
    ordering = ['-id']
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsSearch, self).get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewsCreate(CreateView):
    template_name = 'news/create_news.html'
    form_class = PostForm


class NewsUpdate(UpdateView):
    template_name = 'news/create_news.html'
    form_class = PostForm

    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(DeleteView):
    template_name = 'news/delete_news.html'
    queryset = Post.objects.all()
    success_url = '/news/'





















