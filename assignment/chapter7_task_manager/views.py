from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Task
from .forms import TaskForm


def task_list(request):
	"""List all tasks with pagination and filtering"""
	tasks = Task.objects.all()

	status_filter = request.GET.get('status', '')
	priority_filter = request.GET.get('priority', '')
	search_query = request.GET.get('search', '')

	if status_filter:
		tasks = tasks.filter(status=status_filter)
	if priority_filter:
		tasks = tasks.filter(priority=priority_filter)
	if search_query:
		tasks = tasks.filter(title__icontains=search_query)

	paginator = Paginator(tasks, 5)
	page_num = request.GET.get('page', 1)
	page_obj = paginator.get_page(page_num)

	context = {
		'tasks': page_obj,
		'page_obj': page_obj,
		'status_filter': status_filter,
		'priority_filter': priority_filter,
		'search_query': search_query,
		'status_choices': Task.STATUS_CHOICES,
		'priority_choices': Task.PRIORITY_CHOICES,
	}
	return render(request, 'chapter7_task_manager/task_list.html', context)


def task_create(request):
	"""Create new task"""
	if request.method == 'POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			task = form.save()
			messages.success(request, f'Task "{task.title}" created successfully!')
			return redirect('chapter7_task_manager:task_list')
		messages.error(request, 'Please correct the errors below.')
	else:
		form = TaskForm()

	return render(request, 'chapter7_task_manager/task_form.html', {
		'form': form,
		'title': 'Create Task',
		'button_text': 'Create Task'
	})


def task_detail(request, pk):
	"""View task details"""
	task = get_object_or_404(Task, pk=pk)
	return render(request, 'chapter7_task_manager/task_detail.html', {'task': task})


def task_update(request, pk):
	"""Update existing task"""
	task = get_object_or_404(Task, pk=pk)

	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			messages.success(request, f'Task "{task.title}" updated successfully!')
			return redirect('chapter7_task_manager:task_list')
		messages.error(request, 'Please correct the errors below.')
	else:
		form = TaskForm(instance=task)

	return render(request, 'chapter7_task_manager/task_form.html', {
		'form': form,
		'title': 'Update Task',
		'button_text': 'Update Task'
	})


def task_delete(request, pk):
	"""Delete task"""
	task = get_object_or_404(Task, pk=pk)

	if request.method == 'POST':
		task_title = task.title
		task.delete()
		messages.success(request, f'Task "{task_title}" deleted successfully!')
		return redirect('chapter7_task_manager:task_list')

	return render(request, 'chapter7_task_manager/task_delete.html', {'task': task})
