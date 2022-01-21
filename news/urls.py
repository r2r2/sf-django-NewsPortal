from django.conf.urls.static import static
from django.urls import path

from NewsPortal import settings
from .views import *

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('<int:pk>/edit', NewsUpdate.as_view(), name='update'),
    path('<int:pk>/delete', NewsDelete.as_view(), name='delete'),
    path('search/', NewsSearch.as_view(), name='search'),
    path('add/', NewsCreate.as_view(), name='create'),
    path('upgrade/', upgrade_to_author, name='upgrade'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
