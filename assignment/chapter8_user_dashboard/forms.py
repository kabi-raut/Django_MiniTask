from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserPost


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ('title', 'content')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5})
        }
