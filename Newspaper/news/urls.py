from django.urls import path
from .views import *

urlpatterns = [
	path('', NewsList.as_view(), name='News_list'),
	path('<int:pk>', NewsDetail.as_view(), name='News_detail'),
	path('search/', NewsSearch.as_view(), name='News_search'),
	# path('create/', create_news, name='news_create'),
	path('create/', NewsCreate.as_view(), name='News_create'),
	path('<int:pk>/edit/', NewsUpdate.as_view(), name='News_update'),
	path('<int:pk>/delete/', NewsDelete.as_view(), name='News_delete'),
	path('article/create', ArticleCreate.as_view(), name='Article_create'),
	path('article/<int:pk>/edit', ArticleUpdate.as_view(), name='Article_update'),
	path('article/<int:pk>/delete', ArticleDelete.as_view(), name='Article_delete'),
	path('subscriptions/', subscriptions, name='subscriptions'),
	# path('hello', IndexView.as_view()),
]