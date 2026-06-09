from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from .models import Quiz, Question, Choice, QuestionAnswer


class QuizForm(forms.ModelForm):
    """Form for creating/editing quizzes"""
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'passing_percentage', 'time_limit_minutes', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter quiz title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter quiz description',
                'rows': 4
            }),
            'passing_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'placeholder': 'Passing percentage (0-100)'
            }),
            'time_limit_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Time limit in minutes (optional)'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class QuestionForm(forms.ModelForm):
    """Form for creating/editing questions"""
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'points', 'order']
        widgets = {
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter question text',
                'rows': 3
            }),
            'question_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'points': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Points for this question'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Question number'
            })
        }


class ChoiceForm(forms.ModelForm):
    """Form for creating/editing choices"""
    class Meta:
        model = Choice
        fields = ['choice_text', 'is_correct', 'order']
        widgets = {
            'choice_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter choice text'
            }),
            'is_correct': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            })
        }


# Formsets for managing multiple choices
ChoiceFormSet = inlineformset_factory(
    Question, 
    Choice,
    form=ChoiceForm,
    extra=4,
    can_delete=True
)


class QuestionAnswerForm(forms.ModelForm):
    """Form for answering questions during quiz"""
    selected_choice = forms.ModelChoiceField(
        queryset=Choice.objects.all(),
        widget=forms.RadioSelect(),
        required=False,
        empty_label=None
    )
    
    class Meta:
        model = QuestionAnswer
        fields = ['selected_choice']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set the queryset based on the question
        if self.instance.pk and self.instance.question:
            self.fields['selected_choice'].queryset = self.instance.question.choices.all()


class QuizTakeForm(forms.Form):
    """Form for taking a quiz - dynamically generated based on quiz"""
    def __init__(self, quiz, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quiz = quiz
        
        # Add a field for each question
        for question in quiz.questions.all():
            if question.question_type == 'true_false':
                # For true/false questions
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    label=question.question_text,
                    choices=[
                        ('True', 'True'),
                        ('False', 'False'),
                    ],
                    widget=forms.RadioSelect(),
                    required=True
                )
            else:
                # For multiple choice questions
                choices = [(choice.id, choice.choice_text) for choice in question.choices.all()]
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    label=question.question_text,
                    choices=choices,
                    widget=forms.RadioSelect(),
                    required=True
                )
