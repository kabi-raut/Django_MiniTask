from django.db import models

class Blog(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        permissions=[
            ('publish_blog','Can publish blog'),
        ]
