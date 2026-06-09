from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, signup_view

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
