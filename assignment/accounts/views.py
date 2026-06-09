from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render


class SignUpForm(UserCreationForm):
    """Signup form for new users."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CustomAuthenticationForm(forms.Form):
    """Custom login form that supports both users and hardcoded admin"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            # Check for hardcoded admin credentials
            if username == 'admin' and password == 'admin':
                self.cleaned_data['is_admin_login'] = True
            else:
                # Try regular authentication
                user = authenticate(username=username, password=password)
                if user is None:
                    raise forms.ValidationError(
                        'Invalid username or password.',
                        code='invalid_login'
                    )
                self.cleaned_data['is_admin_login'] = False
        return cleaned_data


class CustomLoginView(FormView):
    """Custom login view supporting both users and hardcoded admin"""
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('chapter9_quiz_system:quiz_list')
    
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        if form.cleaned_data['is_admin_login']:
            # For hardcoded admin, create a temporary session as admin
            # Get or create the admin user
            from django.contrib.auth.models import User
            try:
                admin_user = User.objects.get(username='admin')
            except User.DoesNotExist:
                admin_user = User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin'
                )
            login(self.request, admin_user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            # Regular user authentication
            user = authenticate(username=username, password=password)
            if user is not None:
                login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Redirect to next page or home"""
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


def signup_view(request):
    """Signup endpoint for new users."""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('chapter9_quiz_system:quiz_list'))

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please sign in.')
            return HttpResponseRedirect(reverse_lazy('accounts:login'))
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form, 'title': 'Sign Up'})
