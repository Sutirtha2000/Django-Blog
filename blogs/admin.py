from django.contrib import admin

from .models import Category, Blog

# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }
    list_display = ('title', 'category', 'status', 'image', 'is_featured')
    search_fields = ('title', 'category__name', 'status')
    list_editable = ('is_featured', 'status')


admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)