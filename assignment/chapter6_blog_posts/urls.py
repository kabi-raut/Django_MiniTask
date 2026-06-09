from django.urls import path
from . import views

app_name = 'chapter6_blog_posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('categories/', views.categories_list, name='categories_list'),
]
