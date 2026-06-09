from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chapter9_quiz_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(
                choices=[
                    ('multiple_choice', 'Multiple Choice'),
                    ('true_false', 'True/False'),
                    ('short_answer', 'Short Answer'),
                ],
                default='multiple_choice',
                max_length=15,
            ),
        ),
        migrations.AddField(
            model_name='questionanswer',
            name='answer_text',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
