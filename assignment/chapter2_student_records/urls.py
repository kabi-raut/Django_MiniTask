from django.urls import path
from . import views

app_name = 'chapter2_student_records'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list_students, name='list_students'),
    path('add/', views.add_student, name='add_student'),
    path('search/', views.search_student, name='search_student'),
    path('update/<str:roll_no>/', views.update_student, name='update_student'),
    path('delete/<str:roll_no>/', views.delete_student, name='delete_student'),
]
