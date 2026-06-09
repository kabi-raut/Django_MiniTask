from django.urls import path
from . import views

app_name = 'chapter8_user_dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
]
