from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('set-password/', views.change_password_view1, name='set_password'),
]
