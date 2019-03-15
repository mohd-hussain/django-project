from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView 
	)
from .models import Post
# from django.http import httpResponse


# posts = [
# 	{
# 		'author': 'Mohammed Hussain',
# 		'title': 'Blog Post 1',
# 		'content': 'First Page content',
# 		'date_posted': 'March 5, 2018'
# 	},

# 	{
# 		'author': 'Mohammed Rizwan',
# 		'title': 'Blog Post 2',
# 		'content': 'Second Page content',
# 		'date_posted': 'March 6, 2018'
# 	},

# 	{
# 		'author': 'Mohammed Atay',
# 		'title': 'Blog Post 3',
# 		'content': 'Third Page content',
# 		'date_posted': 'March 7, 2018'
# 	}
# ]



def home(request):
	context = {
		'posts':Post.objects.all()
	}
	return render(request, 'blog/home.html',context)
	# return render(request, 'blog/home.html')
	# return httpResponse('<h1> BLog-Home</h1>')


class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'   #<app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 2


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'   #<app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 2

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
	model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title' , 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title' , 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False



def about(request):
	# return render(request, 'blog/about.html')
	return render(request, 'blog/about.html',{'title':'About New'})

