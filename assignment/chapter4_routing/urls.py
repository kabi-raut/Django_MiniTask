from django.urls import path
from . import views

app_name = 'chapter4_routing'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('portfolio/', views.portfolio, name='portfolio'),
]
