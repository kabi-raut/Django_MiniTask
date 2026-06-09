from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import login, logout
from .middlewares import auth, guest
from chapter8_user_dashboard.models import UserPost


def _assign_post_permissions(group):
    content_type = ContentType.objects.get_for_model(UserPost)
    permissions = Permission.objects.filter(
        content_type=content_type,
        codename__in=['add_userpost', 'change_userpost'],
    )
    group.permissions.add(*permissions)

@guest
def register_view(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            group, created=Group.objects.get_or_create(name='Editor')
            _assign_post_permissions(group)
            user.groups.add(group)
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data={'username':'','password1':'','password2':''}
        form=UserCreationForm(initial=initial_data)
    return render(request,'auth/registration/register.html',{'form':form})

@guest
def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data={'username':'','password':''}
        form=AuthenticationForm(initial=initial_data)
    return render(request,'auth/registration/login.html',{'form':form})
@auth
def logout_view(request):
    logout(request)
    return redirect('login')
@auth
def dashboard_view(request):
    return render(request,'dashboard.html')

@auth
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'auth/registration/changepass.html', {'form': form})

@auth
def change_password_view1(request):
    if request.method == 'POST':
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
    else:
        form = SetPasswordForm(user=request.user)
    return render(request, 'auth/registration/changepass1.html', {'form': form})