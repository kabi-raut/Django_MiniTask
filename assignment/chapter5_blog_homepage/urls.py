from django.urls import path
from . import views

app_name = 'chapter5_blog_homepage'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]
