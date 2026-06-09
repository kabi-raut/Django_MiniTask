from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .forms import RegisterForm, UserPostForm
from .models import UserPost


def _assign_post_permissions(group):
	content_type = ContentType.objects.get_for_model(UserPost)
	permissions = Permission.objects.filter(
		content_type=content_type,
		codename__in=['add_userpost', 'change_userpost'],
	)
	group.permissions.add(*permissions)


def home(request):
	return render(request, 'chapter8_user_dashboard/home.html')


def register_view(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			user_group, _ = Group.objects.get_or_create(name='blog_users')
			_assign_post_permissions(user_group)
			user.groups.add(user_group)
			messages.success(request, 'Registration successful. Please login.')
			return redirect('chapter8_user_dashboard:login')
	else:
		form = RegisterForm()
	return render(request, 'chapter8_user_dashboard/register.html', {'form': form})


def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('chapter8_user_dashboard:dashboard')
		messages.error(request, 'Invalid credentials')
	return render(request, 'chapter8_user_dashboard/login.html')


def logout_view(request):
	logout(request)
	messages.info(request, 'Logged out successfully')
	return redirect('chapter8_user_dashboard:home')


@login_required
def dashboard(request):
	posts = UserPost.objects.filter(user=request.user)
	return render(request, 'chapter8_user_dashboard/dashboard.html', {'posts': posts})


@login_required
@permission_required('chapter8_user_dashboard.add_userpost', raise_exception=True)
def create_post(request):
	if request.method == 'POST':
		form = UserPostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.save()
			messages.success(request, 'Post created successfully')
			return redirect('chapter8_user_dashboard:dashboard')
	else:
		form = UserPostForm()
	return render(request, 'chapter8_user_dashboard/create_post.html', {'form': form})


@login_required
@permission_required('chapter8_user_dashboard.change_userpost', raise_exception=True)
def edit_post(request, post_id):
	post = get_object_or_404(UserPost, id=post_id, user=request.user)
	if request.method == 'POST':
		form = UserPostForm(request.POST, instance=post)
		if form.is_valid():
			form.save()
			messages.success(request, 'Post updated successfully')
			return redirect('chapter8_user_dashboard:dashboard')
	else:
		form = UserPostForm(instance=post)
	return render(request, 'chapter8_user_dashboard/edit_post.html', {'form': form, 'post': post})
