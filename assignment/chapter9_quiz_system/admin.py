from django.contrib import admin
from .models import Quiz, Question, Choice, QuizAttempt, QuestionAnswer


class ChoiceInline(admin.TabularInline):
    """Inline admin for choices"""
    model = Choice
    extra = 2
    fields = ['choice_text', 'is_correct', 'order']


class QuestionInline(admin.TabularInline):
    """Inline admin for questions"""
    model = Question
    extra = 1
    fields = ['question_text', 'question_type', 'points', 'order']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin interface for Quiz model"""
    list_display = ['title', 'created_by', 'is_active', 'passing_percentage', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [QuestionInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'created_by', 'is_active')
        }),
        ('Settings', {
            'fields': ('passing_percentage', 'time_limit_minutes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin interface for Question model"""
    list_display = ['question_text', 'quiz', 'question_type', 'points', 'order']
    list_filter = ['quiz', 'question_type', 'created_at']
    search_fields = ['question_text']
    inlines = [ChoiceInline]
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Question Details', {
            'fields': ('quiz', 'question_text', 'question_type', 'order')
        }),
        ('Scoring', {
            'fields': ('points',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """Admin interface for Choice model"""
    list_display = ['choice_text', 'question', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['choice_text', 'question__question_text']
    
    fieldsets = (
        ('Choice Details', {
            'fields': ('question', 'choice_text', 'order')
        }),
        ('Correct Answer', {
            'fields': ('is_correct',)
        }),
    )


class QuestionAnswerInline(admin.TabularInline):
    """Inline admin for question answers"""
    model = QuestionAnswer
    extra = 0
    readonly_fields = ['question', 'selected_choice', 'answered_at', 'is_correct']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    """Admin interface for QuizAttempt model"""
    list_display = ['user', 'quiz', 'score', 'percentage', 'is_passed', 'started_at']
    list_filter = ['quiz', 'is_passed', 'started_at']
    search_fields = ['user__username', 'quiz__title']
    readonly_fields = ['user', 'quiz', 'started_at', 'completed_at', 'percentage']
    inlines = [QuestionAnswerInline]
    
    fieldsets = (
        ('Attempt Information', {
            'fields': ('user', 'quiz')
        }),
        ('Results', {
            'fields': ('score', 'total_points', 'percentage', 'is_passed')
        }),
        ('Timeline', {
            'fields': ('started_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def percentage(self, obj):
        return f"{obj.percentage}%"
    percentage.short_description = 'Score %'


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    """Admin interface for QuestionAnswer model"""
    list_display = ['attempt', 'question', 'selected_choice']
    list_filter = ['answered_at']
    search_fields = ['attempt__user__username', 'question__question_text']
    readonly_fields = ['attempt', 'question', 'answered_at']
    
    fieldsets = (
        ('Answer Information', {
            'fields': ('attempt', 'question', 'selected_choice')
        }),
        ('Validation', {
            'fields': ('is_correct',),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('answered_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
