from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.http import Http404
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Blog, Comment
from assignments.models import About
# Create your views here.
def home(request):
    featured_posts = Blog.objects.filter(is_featured=True).order_by("updated_at")
    posts = Blog.objects.filter(is_featured=False, status='1')
    try:
        about = About.objects.get()
    except About.DoesNotExist:
        about = None
    
    context = {
        'featured_posts' : featured_posts,
        'posts' : posts,
        'about' : about
    }
    return render(request, 'blogs/home.html', context=context)

class CategoryView(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            posts = Blog.objects.filter(status='1', category=category)
        except Category.DoesNotExist:
            messages.info(request, "Not Found")
            return redirect('home')
            # raise Http404
        context = {
            'posts' : posts,
            'category' : category,
        }
        return render(request, 'blogs/post_by_category.html', context=context)


class BlogViewClass(View):
    def get_blog(self, slug=None):
        try:
            blog = Blog.objects.get(slug=slug)
            return blog
        except Blog.DoesNotExist:
            return None
        
    def get(self, request, slug=None):
        
        blog = self.get_blog(slug=slug)

        if blog is None:
            messages.info(request, "This Blog does not exist !!!")
            return redirect('home')
        
        comments = Comment.objects.filter(blog=blog)
        count = comments.count()

        context = {
            'blog' : blog,
            'comments' : comments,
            'comment_count' : count,
        }

        return render(request, 'blogs/blog.html', context=context)
    
    def post(self, request, slug=None):
        blog = self.get_blog(slug=slug)

        if blog is None:
            messages.info(request, "This Blog does not exist !!!")
            return redirect('blogs')
        
        comment = Comment()
        content = request.POST.get('comment')
        comment.content = content
        comment.blog = blog
        comment.user = request.user
        comment.save()
        return HttpResponseRedirect(request.path_info)


class Search(View):
    def get(self, request):
        q = request.GET.get('q')
        blogs = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(category__name__icontains=q), status='1')
        print(blogs)
        context = {
            'blogs' : blogs,
            'q' : q
        }
        return render(request, 'blogs/search.html', context=context)