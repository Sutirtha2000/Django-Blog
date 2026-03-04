from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category_view'),
    path('blogs/<slug:slug>/', views.BlogViewClass.as_view(), name='blog_view'),
    path('blog/search/', views.Search.as_view(), name='search'),
]