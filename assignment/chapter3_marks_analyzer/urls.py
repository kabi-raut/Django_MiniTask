from django.urls import path
from . import views

app_name = 'chapter3_marks_analyzer'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_data, name='upload_data'),
    path('view/', views.view_data, name='view_data'),
    path('statistics/', views.statistics, name='statistics'),
    path('grouping/', views.grouping, name='grouping'),
    path('filtering/', views.filtering, name='filtering'),
    path('sorting/', views.sorting, name='sorting'),
]
