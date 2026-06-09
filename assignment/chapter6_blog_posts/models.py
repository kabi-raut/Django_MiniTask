from django.db import models
from django.utils import timezone


class Category(models.Model):
    """Blog category model"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    """Blog post model"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    content = models.TextField()
    excerpt = models.CharField(max_length=300)
    featured_image = models.CharField(max_length=200, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_published']),
        ]

    def __str__(self):
        return self.title

    def get_published_posts(self):
        """Get all published posts"""
        return Post.objects.filter(is_published=True)

    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])
