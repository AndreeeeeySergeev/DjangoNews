from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Subscription, Category
from .filters import PostFilter
from .forms import PostForm, ArtcileForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.db.models import Exists, OuterRef
from django.views import View
# from .tasks import hello
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.translation import gettext as _
from django.utils.translation import activate, get_supported_language_variant
from django.http.response import HttpResponse
from django.utils import timezone
import logging, pytz


from datetime import datetime

logger = logging.getLogger(__name__)

# Create your views here.
# class IndexView(View):
# 	def get(self, request):
# 		# hello.delay()
# 		string = _('Hello, world!')
# 		return HttpResponse(string)

# class IndexView(View):
# 	def get(self, request):
# 		models = Post.objects.all()
#
# 		context = {
# 			'models': models,
# 			}
# 		return HttpResponse(render(request, 'i18n.html', context)



@login_required
@csrf_protect
@cache_page(60 * 15)
def subscriptions(request):
	if request.method == 'POST':
		category_id = request.POST.get('category_id')
		category = Category.objects.get(id=category_id)
		action = request.POST.get('action')

		if action == 'subscribe':
			Subscription.objects.create(user=request.user, category=category)
		elif action == 'unsubscribe':
			Subscription.objects.filter(user=request.user, category=category).delete()
	categories_with_subscriptions = Category.objects.annotate(
		user_subscribed=Exists(
			Subscription.objects.filter(
				user=request.user,
				category=OuterRef('pk')),
		)
	).order_by('name')
	return render(request, 'subscriptions.html', {'categories': categories_with_subscriptions},)

class IndexView(View):
	def get(self, request):
		models = Post.objects.all()

		context = {
			'models': models,
			'current_time': timezone.localtime(timezone.now()),
			'timezones': pytz.common_timezones
			}
		return HttpResponse(render(request, 'i18n.html', context))

	def post(self, request):
		request.session['django_timezone'] = request.POST['timezone']
		return redirect('/')

class NewsList(ListView):
	model = Post
	ordering = 'dateCreation'
	template_name = 'Newspaper.html'
	context_object_name = 'Newspaper'
	paginate_by = 10


class NewsDetail(DetailView):
	model = Post
	template_name = 'News.html'
	context_object_name = 'News'

	def get_news(self, *args, **kwargs):
		news = cache.get(f'post-{self.kwargs["pk"]}', None)
		if not news:
			news = super().get_object(queryset=self.queryset)
			cache.set(f'post-{self.kwargs["pk"]}', news)
		return news

# def create_news(request):
# 	form = PostForm()
# 	if request.method == 'POST':
# 		form = PostForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			return HttpResponseRedirect('/news/')
#
# 	return render(request, 'News_create.html', {'form': form})

class NewsSearch(ListView):
	model = Post
	template_name = 'News_search.html'
	context_object_name = 'News_paper'
	paginate_by = 1

	def get_queryset(self):
		queryset = super().get_queryset()
		self.filterset = PostFilter(self.request.GET, queryset)
		return self.filterset.qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['filterset'] = self.filterset
		return context


	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	context['time_now'] = datetime.utcnow()
	# 	context['next_publication'] = None
	# 	return context


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	permission_required = ('news.create_news',)
	form_class = PostForm
	raise_exception = True
	model = Post
	template_name = 'News_create.html'

	def form_valid(self, form):
		post = form.save(commit=False)
		post.categoryType = 'NEWS'
		return super().form_valid(form)


	# @login_required
	# def show_protected_page(request):
		# pass


class NewsUpdate(PermissionRequiredMixin, UpdateView):
	permission_required = ('news.change_news',)
	form_class = PostForm
	model = Post
	template_name = 'News_create.html'

class NewsDelete(PermissionRequiredMixin, DeleteView):
	permission_required = ('news.delete_news',)
	model = Post
	template_name = 'News_delete.html'
	success_url = reverse_lazy('News_list')

class ArticleCreate(PermissionRequiredMixin, CreateView):
	permission_required = ('news.delete_article',)
	form_class = ArtcileForm
	model = Post
	template_name = 'Article_create.html'

	def form_valid(self, form):
		post = form.save(commit=False)
		post.categoryType = 'ARTICLE'
		return super().form_valid(form)

class ArticleUpdate(PermissionRequiredMixin, UpdateView):
	permission_required = ('news.change_article',)
	form_class = ArtcileForm
	model = Post
	template_name = 'Article_create.html'

	def get_article(self, *args, **kwargs):
		article = cache.get(f'post-{self.kwargs["pk"]}', None)
		if not article:
			article = super().get_object(queryset=self.queryset)
			cache.set(f'post-{self.kwargs["pk"]}', article)
		return article



class ArticleDelete(PermissionRequiredMixin, DeleteView):
	permission_required = ('news.delete_article',)
	form_post = ArtcileForm
	model = Post
	template_name = 'Article_delete.html'
	success_url = reverse_lazy('News_list')