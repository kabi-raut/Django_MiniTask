from django.urls import path
from . import views

app_name = 'chapter9_quiz_system'

urlpatterns = [
    # Login
    path('login/', views.QuizLoginView.as_view(), name='login'),
    path('logout/', views.quiz_logout, name='logout'),
    
    # Quiz listing and details
    path('', views.QuizListView.as_view(), name='quiz_list'),
    path('quiz/<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('quiz/<int:pk>/start/', views.start_quiz, name='start_quiz'),
    
    # Quiz taking and results
    path('attempt/<int:attempt_id>/take/', views.take_quiz, name='take_quiz'),
    path('attempt/<int:attempt_id>/results/', views.quiz_results, name='quiz_results'),
    
    # Quiz management (admin)
    path('create/', views.QuizCreateView.as_view(), name='quiz_create'),
    path('quiz/<int:pk>/edit/', views.QuizUpdateView.as_view(), name='quiz_edit'),
    path('quiz/<int:pk>/delete/', views.QuizDeleteView.as_view(), name='quiz_delete'),
    
    # Question management (admin)
    path('quiz/<int:quiz_pk>/question/create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('question/<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='question_edit'),
    
    # User dashboard
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
]
