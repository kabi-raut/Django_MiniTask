from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.db.models import Q, Avg, Count, F, FloatField, ExpressionWrapper
from django.utils import timezone
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django import forms
from django.contrib.auth import authenticate, login, logout as auth_logout
from datetime import timedelta

from .models import Quiz, Question, Choice, QuizAttempt, QuestionAnswer
from .forms import QuizForm, QuestionForm, ChoiceFormSet, QuizTakeForm


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


class QuizLoginView(FormView):
    """Custom login view for quiz system supporting both users and hardcoded admin"""
    form_class = CustomAuthenticationForm
    template_name = 'chapter9_quiz_system/quiz_login.html'
    success_url = reverse_lazy('chapter9_quiz_system:quiz_list')
    
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        if form.cleaned_data['is_admin_login']:
            # For hardcoded admin, get or create the admin user
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
        """Redirect to next page or quiz list"""
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('chapter9_quiz_system:quiz_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Quiz System - Login'
        return context


def quiz_logout(request):
    """Log out any authenticated user (regular or admin) from quiz system."""
    auth_logout(request)
    return redirect('chapter9_quiz_system:login')


class QuizListView(LoginRequiredMixin, ListView):
    """View for listing all quizzes"""
    model = Quiz
    template_name = 'chapter9_quiz_system/quiz_list.html'
    context_object_name = 'quizzes'
    paginate_by = 10
    
    def get_queryset(self):
        return Quiz.objects.filter(is_active=True).annotate(
            total_attempts=Count('attempts'),
            avg_score=Avg('attempts__score')
        )


class QuizDetailView(LoginRequiredMixin, DetailView):
    """View for quiz details and start page"""
    model = Quiz
    template_name = 'chapter9_quiz_system/quiz_detail.html'
    context_object_name = 'quiz'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.get_object()
        
        # Get user's previous attempts
        user_attempts = QuizAttempt.objects.filter(
            quiz=quiz,
            user=self.request.user
        ).order_by('-started_at')
        
        context['user_attempts'] = user_attempts
        context['total_questions'] = quiz.questions.count()
        context['total_points'] = sum(q.points for q in quiz.questions.all())
        
        return context


@login_required
def start_quiz(request, pk):
    """Start a quiz attempt"""
    quiz = get_object_or_404(Quiz, pk=pk, is_active=True)
    
    # Create a new quiz attempt
    attempt = QuizAttempt.objects.create(
        quiz=quiz,
        user=request.user,
        total_points=sum(q.points for q in quiz.questions.all())
    )
    
    # Create empty question answers for each question
    for question in quiz.questions.all():
        QuestionAnswer.objects.create(
            attempt=attempt,
            question=question
        )
    
    return redirect('chapter9_quiz_system:take_quiz', attempt_id=attempt.id)


@login_required
def take_quiz(request, attempt_id):
    """View for taking a quiz"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    
    # Verify user owns this attempt
    if attempt.user != request.user:
        return HttpResponseForbidden()
    
    # Check if already completed
    if attempt.is_completed:
        return redirect('chapter9_quiz_system:quiz_results', attempt_id=attempt.id)
    
    quiz = attempt.quiz
    
    # Check time limit
    if quiz.time_limit_minutes:
        time_elapsed = timezone.now() - attempt.started_at
        time_limit = timedelta(minutes=quiz.time_limit_minutes)
        if time_elapsed > time_limit:
            attempt.completed_at = timezone.now()
            attempt.calculate_score()
            return redirect('chapter9_quiz_system:quiz_results', attempt_id=attempt.id)
    
    if request.method == 'POST':
        # Process form submission
        questions = quiz.questions.all()
        
        for question in questions:
            field_name = f'question_{question.id}'
            text_field_name = f'question_text_{question.id}'
            typed_answer = request.POST.get(text_field_name, '').strip()

            # Get the question answer
            try:
                answer = QuestionAnswer.objects.get(
                    attempt=attempt,
                    question=question
                )

                if question.question_type == 'short_answer':
                    answer.answer_text = typed_answer
                    answer.selected_choice = None
                    answer.save()
                    continue

                selected_value = request.POST.get(field_name)
                if not selected_value:
                    # Allow typed text input when no option is selected.
                    answer.selected_choice = question.choices.filter(choice_text__iexact=typed_answer).first() if typed_answer else None
                    answer.answer_text = typed_answer
                    answer.save()
                    continue

                if question.question_type == 'true_false':
                    choice = question.choices.filter(choice_text__iexact=selected_value).first()
                else:
                    choice = question.choices.filter(id=selected_value).first()

                answer.selected_choice = choice
                answer.answer_text = typed_answer
                answer.save()
            except QuestionAnswer.DoesNotExist:
                pass
        
        # Mark as completed and calculate score
        attempt.completed_at = timezone.now()
        attempt.calculate_score()
        
        return redirect('chapter9_quiz_system:quiz_results', attempt_id=attempt.id)
    
    # GET request - display the form
    form = QuizTakeForm(quiz, initial={})
    questions = quiz.questions.all()
    user_answers = {answer.question_id: answer for answer in attempt.answers.all()}
    
    # Calculate time remaining
    time_remaining = None
    if quiz.time_limit_minutes:
        time_elapsed = timezone.now() - attempt.started_at
        time_remaining = quiz.time_limit_minutes * 60 - int(time_elapsed.total_seconds())
        if time_remaining < 0:
            time_remaining = 0
    
    context = {
        'quiz': quiz,
        'attempt': attempt,
        'form': form,
        'questions': questions,
        'user_answers': user_answers,
        'time_remaining': time_remaining,
    }
    
    return render(request, 'chapter9_quiz_system/take_quiz.html', context)


@login_required
def quiz_results(request, attempt_id):
    """View for displaying quiz results"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    
    # Verify user owns this attempt
    if attempt.user != request.user:
        return HttpResponseForbidden()
    
    # Get all answers with question and choice details
    answers = attempt.answers.select_related('question', 'selected_choice')
    
    context = {
        'attempt': attempt,
        'answers': answers,
        'quiz': attempt.quiz,
    }
    
    return render(request, 'chapter9_quiz_system/quiz_results.html', context)


class QuizCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View for admin to create quizzes"""
    model = Quiz
    form_class = QuizForm
    template_name = 'chapter9_quiz_system/quiz_form.html'
    success_url = reverse_lazy('chapter9_quiz_system:quiz_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class QuizUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for admin to edit quizzes"""
    model = Quiz
    form_class = QuizForm
    template_name = 'chapter9_quiz_system/quiz_form.html'
    success_url = reverse_lazy('chapter9_quiz_system:quiz_list')
    
    def test_func(self):
        quiz = self.get_object()
        return self.request.user.is_staff and quiz.created_by == self.request.user


class QuizDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for admin to delete quizzes"""
    model = Quiz
    template_name = 'chapter9_quiz_system/quiz_confirm_delete.html'
    success_url = reverse_lazy('chapter9_quiz_system:quiz_list')
    
    def test_func(self):
        quiz = self.get_object()
        return self.request.user.is_staff and quiz.created_by == self.request.user


class QuestionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View for admin to create questions"""
    model = Question
    form_class = QuestionForm
    template_name = 'chapter9_quiz_system/question_form.html'
    
    def test_func(self):
        quiz = Quiz.objects.get(pk=self.kwargs['quiz_pk'])
        return self.request.user.is_staff and quiz.created_by == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ChoiceFormSet(self.request.POST)
        else:
            context['formset'] = ChoiceFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if not formset.is_valid():
            return self.form_invalid(form)

        quiz = Quiz.objects.get(pk=self.kwargs['quiz_pk'])
        form.instance.quiz = quiz
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('chapter9_quiz_system:quiz_edit', kwargs={'pk': self.kwargs['quiz_pk']})


class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for admin to edit questions"""
    model = Question
    form_class = QuestionForm
    template_name = 'chapter9_quiz_system/question_form.html'
    
    def test_func(self):
        question = self.get_object()
        return self.request.user.is_staff and question.quiz.created_by == self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        
        if self.request.POST:
            context['formset'] = ChoiceFormSet(self.request.POST, instance=question)
        else:
            context['formset'] = ChoiceFormSet(instance=question)
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('chapter9_quiz_system:quiz_edit', kwargs={'pk': self.object.quiz.pk})


@login_required
def user_dashboard(request):
    """View for user's quiz dashboard"""
    user_attempts = QuizAttempt.objects.filter(user=request.user).select_related('quiz').order_by('-started_at')

    avg_score = user_attempts.filter(score__isnull=False, total_points__gt=0).annotate(
        percentage_value=ExpressionWrapper(
            100.0 * F('score') / F('total_points'),
            output_field=FloatField()
        )
    ).aggregate(avg=Avg('percentage_value'))['avg'] or 0
    
    stats = {
        'total_attempts': user_attempts.count(),
        'total_passed': user_attempts.filter(is_passed=True).count(),
        'avg_score': avg_score,
    }
    
    context = {
        'user_attempts': user_attempts,
        'stats': stats,
    }
    
    return render(request, 'chapter9_quiz_system/user_dashboard.html', context)
