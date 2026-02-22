from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATUS_CHOICE = (
    ('0' , 'Draft'),
    ('1' , 'Published'),
    ('2' , 'Deleted')
)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False, related_name='blogs')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    status = models.CharField(choices=STATUS_CHOICE, default='0', max_length=10)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'blog'
        verbose_name_plural = 'blogs'