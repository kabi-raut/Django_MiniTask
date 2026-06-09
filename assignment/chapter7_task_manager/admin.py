from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'due_date', 'created_at')
    list_filter = ('priority', 'status', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description')
        }),
        ('Details', {
            'fields': ('priority', 'status', 'due_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
