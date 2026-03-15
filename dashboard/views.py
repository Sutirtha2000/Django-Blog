from django.shortcuts import render, redirect
from django.http import Http404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.template.defaultfilters import slugify

from blogs.models import Blog, Category
from blogs.forms import CategoryForm, BlogForm
# Create your views here.

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        category_count = Category.objects.all().count()
        blogs_count = Blog.objects.all().count()
        # print(category_count, blogs_count)
        context = {
            'category_count' : category_count,
            'blogs_count' : blogs_count
        }
        return render(request, 'dashboard/dashboard.html', context=context)
    

class CategoriesView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        context = {
            'categories' : categories
        }
        return render(request, 'dashboard/categories.html', context=context)


class AddCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        form = CategoryForm()
        context = {
            'form' : form
        }
        return render(request, 'dashboard/add_category.html', context=context)

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Category added Successfully !!!")
            return redirect('categories')
        context = {
            'form' : form
        }
        return render(request, 'dashboard/add_category.html', context=context)


class EditCategoryView(LoginRequiredMixin, View):
    def pre_process(self, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            return category
        except Category.DoesNotExist:
            return None
        
    def get(self, request, pk=None):
        category = self.pre_process(pk=pk)
        if category is None:
            messages.info(request, "This Category does not exist !!!")
            return redirect('categories')
            # raise Http404()

        form = CategoryForm(instance=category)
        context = {
            'form' : form,
            'edit' : True
        }
        return render(request, 'dashboard/add_category.html', context=context)

    def post(self, request, pk=None):
        category = self.pre_process(pk=pk)
        if category is None:
            messages.info(request, "This Category does not exist !!!")
            return redirect('categories')
            # raise Http404()
        
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated Successfully !!!")
            return redirect('categories')
        context = {
            'form' : form,
            'edit' : True
        }
        return render(request, 'dashboard/add_category.html', context=context)


class DeleteCategoryView(LoginRequiredMixin, View):
    def get_category(self, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            return category
        except Category.DoesNotExist:
            return None
        
    def get(self, request, pk=None):
        category = self.get_category(pk=pk)

        if category is None:
            messages.info(request, "This Category does not exist !!!")
            return redirect('categories')
        
        category.delete()
        messages.success(request, "Category deleted Successfully !!!")
        return redirect('categories')


class AllBlogsView(LoginRequiredMixin, View):
    def get(self, request):
        blogs = Blog.objects.all()
        context = {
            'blogs' : blogs
        }
        return render(request, 'dashboard/blogs.html', context=context)


class AddBlogView(LoginRequiredMixin, View):
    def get(self, request):
        form = BlogForm()
        context = {
            'form' : form,
        }
        return render(request, 'dashboard/add_blog.html', context=context)
    
    def post(self, request):
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            title = form.cleaned_data.get('title')
            blog.slug = slugify(title) + "-" + str(blog.id)
            # print(blog)
            blog.save()
            return redirect('blogs')
        context = {
            'form' : form
        }
        return render(request, 'dashboard/add_blog.html', context=context)
    

class EditBlogView(LoginRequiredMixin, View):
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
            return redirect('blogs')
        
        if blog.author != request.user:
            messages.error(request, "You are not allowed to edit this blog.")
            return redirect('blogs')
        
        form = BlogForm(instance=blog)
        context = {
            'form' : form,
            'edit' : True
        }
        return render(request, 'dashboard/add_blog.html', context=context)

    def post(self, request, slug=None):
        blog = self.get_blog(slug=slug)

        if blog is None:
            messages.info(request, "This Blog does not exist !!!")
            return redirect('blogs')
        
        if blog.author != request.user:
            messages.error(request, "You are not allowed to edit this blog.")
            return redirect('blogs')

        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save()
            title = form.cleaned_data.get('title')
            new_slug = slugify(title) + "-" + str(blog.id)
            if new_slug != blog.slug:
                blog.slug = new_slug
            blog.save()
            return redirect('blogs')
        context = {
            'form' : form,
            'edit' : True
        }
        return render(request, 'dashboard/add_blog.html', context=context)


class DeleteBlogView(LoginRequiredMixin, View):
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
            return redirect('blogs')
        
        blog.delete()
        messages.success(request, "Blog deleted Successfully !!!")
        return redirect('blogs')