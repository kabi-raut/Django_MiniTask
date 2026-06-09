from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Quiz(models.Model):
    """Model representing a quiz"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    passing_percentage = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    time_limit_minutes = models.IntegerField(null=True, blank=True, help_text="Time limit in minutes (None = no limit)")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Question(models.Model):
    """Model representing a question in a quiz"""
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPES, default='multiple_choice')
    points = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'id']
        unique_together = ('quiz', 'order')
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}: {self.question_text[:50]}"


class Choice(models.Model):
    """Model representing a choice/option for a question"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.question.question_text[:30]} - {self.choice_text[:30]}"


class QuizAttempt(models.Model):
    """Model tracking a user's attempt at a quiz"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    total_points = models.IntegerField(default=0)
    is_passed = models.BooleanField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
        unique_together = ('quiz', 'user', 'started_at')
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.started_at})"
    
    @property
    def percentage(self):
        """Calculate percentage score"""
        if self.total_points == 0:
            return 0
        return round((self.score / self.total_points) * 100, 2) if self.score else 0
    
    @property
    def is_completed(self):
        """Check if attempt is completed"""
        return self.completed_at is not None
    
    def calculate_score(self):
        """Calculate score based on answers"""
        answers = self.answers.all()
        total_score = 0
        for answer in answers:
            if answer.selected_choice and answer.selected_choice.is_correct:
                total_score += answer.question.points
        self.score = total_score
        self.is_passed = self.percentage >= self.quiz.passing_percentage
        self.save()
        return total_score


class QuestionAnswer(models.Model):
    """Model tracking a user's answer to a question"""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True)
    answer_text = models.TextField(blank=True)
    answered_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['question__order']
        unique_together = ('attempt', 'question')
    
    def __str__(self):
        return f"{self.attempt.user.username} - {self.question.question_text[:30]}"
    
    @property
    def is_correct(self):
        """Check if answer is correct"""
        return self.selected_choice and self.selected_choice.is_correct if self.selected_choice else False
