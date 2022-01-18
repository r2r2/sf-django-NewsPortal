import django_filters
from django.forms import DateInput
from django_filters import FilterSet
from .models import Post, Author, Category


class PostFilter(FilterSet):

    post_title = django_filters.CharFilter(field_name='post_title', lookup_expr='icontains', label='Заголовок:')
    # author = django_filters.CharFilter(field_name='author_id__author_name_id__username', label='Автор:', lookup_expr='icontains')
    date_creation = django_filters.DateFilter(label='Дата:', lookup_expr='gte', widget=DateInput(attrs={'type': 'date'}))
    category = django_filters.ModelChoiceFilter(lookup_expr='exact', queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ['date_creation', 'post_title', 'author', 'category']


