from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm, ArtcileForm
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required

from datetime import datetime


# Create your views here.

class NewsList(ListView):
	model = Post
	ordering = 'dateCreation'
	template_name = 'Newspaper.html'
	context_object_name = 'Newspaper'
	paginate_by = 10

class NewsSearch(ListView):
	model = Post
	template_name = 'News_search.html'
	context_object_name = 'News_paper'
	paginate_by = 1

	def get_queryset(self):
		queryset = super().get_queryset()
		self.filterset = PostFilter(self.request.GET, queryset)
		return self.filterset.qs

	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	context['time_now'] = datetime.utcnow()
	# 	context['next_publication'] = None
	# 	return context

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['filterset'] = self.filterset
		return context

class NewsDetail(DetailView):
	model = Post
	template_name = 'News.html'
	context_object_name = 'News'

# def create_news(request):
# 	form = PostForm()
# 	if request.method == 'POST':
# 		form = PostForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			return HttpResponseRedirect('/news/')
#
# 	return render(request, 'News_create.html', {'form': form})

class NewsCreate(LoginRequiredMixin, CreateView):
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


class NewsUpdate(UpdateView):
	form_class = PostForm
	model = Post
	template_name = 'News_create.html'

class NewsDelete(DeleteView):
	model = Post
	template_name = 'News_delete.html'
	success_url = reverse_lazy('News_list')

class ArticleCreate(CreateView):
	form_class = ArtcileForm
	model = Post
	template_name = 'Article_create.html'

	def form_valid(self, form):
		post = form.save(commit=False)
		post.categoryType = 'ARTICLE'
		return super().form_valid(form)

class ArticleUpdate(UpdateView):
	form_class = ArtcileForm
	model = Post
	template_name = 'Article_create.html'

class ArticleDelete(DeleteView):
	form_post = ArtcileForm
	model = Post
	template_name = 'Article_delete.html'
	success_url = reverse_lazy('News_list')