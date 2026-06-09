"""
URL configuration for assignment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('chapter1/', include('chapter1_calculator.urls')),
    path('chapter2/', include('chapter2_student_records.urls')),
    path('chapter3/', include('chapter3_marks_analyzer.urls')),
    path('chapter4/', include('chapter4_routing.urls')),
    path('chapter5/', include('chapter5_blog_homepage.urls')),
    path('chapter6/', include('chapter6_blog_posts.urls')),
    path('chapter7/', include('chapter7_task_manager.urls')),
    path('chapter8/', include('chapter8_user_dashboard.urls')),
    path('chapter9/', include('chapter9_quiz_system.urls')),
    path('auth/', include('auth_app.urls')),
    path('auth/', include('django.contrib.auth.urls')),
   
]
