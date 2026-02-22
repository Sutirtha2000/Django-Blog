from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.http import Http404

from .models import Category, Blog
# Create your views here.
def home(request):
    featured_posts = Blog.objects.filter(is_featured=True).order_by("updated_at")
    posts = Blog.objects.filter(is_featured=False, status='1')
    context = {
        'featured_posts' : featured_posts,
        'posts' : posts
    }
    return render(request, 'home.html', context=context)

class CategoryView(View):
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