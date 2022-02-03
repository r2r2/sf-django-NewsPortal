from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from NewsPortal import settings
from .views import *

app_name = 'news'

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('<slug:slug>', NewsDetail.as_view(), name='news_detail'),
    path('<slug:slug>/edit', NewsUpdate.as_view(), name='update'),
    path('<slug:slug>/delete', NewsDelete.as_view(), name='delete'),
    path('search/', cache_page(60)(NewsSearch.as_view()), name='search'),
    path('add/', NewsCreate.as_view(), name='create'),
    path('upgrade/', upgrade_to_author, name='upgrade'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns = [
#     path('', NewsList.as_view(), name='news'),
#     path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
#     path('<int:pk>/edit', NewsUpdate.as_view(), name='update'),
#     path('<int:pk>/delete', NewsDelete.as_view(), name='delete'),
#     path('search/', cache_page(60)(NewsSearch.as_view()), name='search'),
#     path('add/', NewsCreate.as_view(), name='create'),
#     path('upgrade/', upgrade_to_author, name='upgrade'),
#     path('subscribe/', SubscribeView.as_view(), name='subscribe'),
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)