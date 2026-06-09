from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'created_at', 'views')
    list_filter = ('is_published', 'category', 'created_at')
    search_fields = ('title', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'views')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author')
        }),
        ('Content', {
            'fields': ('category', 'content', 'excerpt', 'featured_image')
        }),
        ('Status', {
            'fields': ('is_published',)
        }),
        ('Statistics', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
