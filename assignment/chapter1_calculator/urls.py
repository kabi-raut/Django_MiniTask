from django.urls import path
from . import views

app_name = 'chapter1_calculator'

urlpatterns = [
    path('', views.index, name='index'),
    path('calculator/', views.calculator_page, name='calculator'),
    path('guessing-game/', views.guessing_game, name='guessing_game'),
    path('reset-game/', views.reset_game, name='reset_game'),
]
