from .models import Category

def blog_categories(request):
    categories = Category.objects.all()
    return {
        'categories' : categories
    }