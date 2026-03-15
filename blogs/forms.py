from django import forms

from .models import Category, Blog

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            'title',
            'image',
            'status',
            'is_featured',
            'content',
            'category',
        ]