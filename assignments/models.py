from django.db import models

# Create your models here.
class About(models.Model):
    header = models.CharField(max_length=25)
    description = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.header
    
    class Meta:
        verbose_name = 'about'
        verbose_name_plural = 'about'
    

class Social(models.Model):
    platform = models.CharField(max_length=30)
    link = models.URLField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.platform
    
    class Meta:
        verbose_name_plural = 'socials'