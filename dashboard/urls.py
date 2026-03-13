from django.urls import path

from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('categories/add/', views.AddCategoryView.as_view(), name='add_category'),
    path('categories/edit/<int:pk>/', views.EditCategoryView.as_view(), name='edit_category'),
    path('categories/delete/<int:pk>/', views.DeleteViewClass.as_view(), name='delete_category'),
]