from django.shortcuts import render, redirect
from django.http import Http404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from blogs.models import Blog, Category
from blogs.forms import CategoryForm
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


class DeleteViewClass(LoginRequiredMixin, View):
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