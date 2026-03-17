from django.urls import path

from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    #  Category app
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('categories/add/', views.AddCategoryView.as_view(), name='add_category'),
    path('categories/edit/<int:pk>/', views.EditCategoryView.as_view(), name='edit_category'),
    path('categories/delete/<int:pk>/', views.DeleteCategoryView.as_view(), name='delete_category'),

    # Blog App
    path('blogs/', views.AllBlogsView.as_view(), name='blogs'),
    path('blogs/create/', views.AddBlogView.as_view(), name='add_blog'),
    path('blogs/edit/<slug:slug>/', views.EditBlogView.as_view(), name='edit_blog'),
    path('blogs/delete/<slug:slug>/',views.DeleteBlogView.as_view(), name='delete_blog'),

    # Users App
    path('users/', views.AllUsersView.as_view(), name='users'),
    path('users/create/', views.AddUserView.as_view(), name='add_user'),
    path('users/edit/<int:pk>/', views.EditUserView.as_view(), name='edit_user'),
    path('users/delete/<int:pk>/', views.DeleteUserView.as_view(), name='delete_user'),
]