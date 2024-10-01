from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
	path('', cache_page(60)(NewsList.as_view()), name='News_list'),
	path('<int:pk>', cache_page(300)(NewsDetail.as_view()), name='News_detail'),
	path('search/', cache_page(300)(NewsSearch.as_view()), name='News_search'),
	# path('create/', create_news, name='news_create'),
	path('create/', cache_page(300)(NewsCreate.as_view()), name='News_create'),
	path('<int:pk>/edit/', cache_page(300)(NewsUpdate.as_view()), name='News_update'),
	path('<int:pk>/delete/', cache_page(300)(NewsDelete.as_view()), name='News_delete'),
	path('article/create', ArticleCreate.as_view(), name='Article_create'),
	path('article/<int:pk>/edit', ArticleUpdate.as_view(), name='Article_update'),
	path('article/<int:pk>/delete', ArticleDelete.as_view(), name='Article_delete'),
	path('subscriptions/', subscriptions, name='subscriptions'),
	# path('hello', IndexView.as_view()),
	path('translate/', IndexView.as_view, name='translation'),
]