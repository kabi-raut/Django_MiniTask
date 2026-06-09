from django.shortcuts import render


def index(request):
    """Blog homepage"""
    featured_posts = [
        {
            'id': 1,
            'title': 'Welcome to Our Blog',
            'author': 'Admin',
            'date': '2024-03-28',
            'excerpt': 'This is the first post on our brand new blog platform.',
            'category': 'General'
        },
        {
            'id': 2,
            'title': 'Django Templates Tutorial',
            'author': 'John',
            'date': '2024-03-27',
            'excerpt': 'Learn how to create beautiful Django templates with inheritance.',
            'category': 'Tutorial'
        },
        {
            'id': 3,
            'title': 'Static Files in Django',
            'author': 'Jane',
            'date': '2024-03-26',
            'excerpt': 'Master the art of serving CSS, JavaScript, and images in Django.',
            'category': 'Tutorial'
        },
    ]
    
    recent_posts = [
        {
            'id': 4,
            'title': 'Django Messages Framework',
            'author': 'Bob',
            'date': '2024-03-25',
            'category': 'Tips'
        },
        {
            'id': 5,
            'title': 'Best Practices for Templates',
            'author': 'Alice',
            'date': '2024-03-24',
            'category': 'Best Practices'
        },
    ]
    
    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'total_posts': 5
    }
    return render(request, 'chapter5_blog_homepage/index.html', context)


def post_detail(request, post_id):
    """Display full post"""
    posts = {
        1: {
            'id': 1,
            'title': 'Welcome to Our Blog',
            'author': 'Admin',
            'date': '2024-03-28',
            'category': 'General',
            'content': '''
                Welcome to our Django blog platform! This is built as part of learning Django templates and static files.
                
                In this chapter, you'll learn:
                - Creating Django templates
                - Template inheritance
                - Static files (CSS, JS, images)
                - Django messages framework
                
                Stay tuned for more content!
            '''
        },
        2: {
            'id': 2,
            'title': 'Django Templates Tutorial',
            'author': 'John',
            'date': '2024-03-27',
            'category': 'Tutorial',
            'content': '''
                Django templates are powerful tools for generating HTML dynamically.
                
                Key concepts:
                1. Template variables: {{ variable }}
                2. Template tags: {% tag %}
                3. Template filters: {{ value|filter }}
                
                Template inheritance allows you to create a base template that contains common structure,
                then extend it in child templates using {% extends %} and {% block %}.
            '''
        },
        3: {
            'id': 3,
            'title': 'Static Files in Django',
            'author': 'Jane',
            'date': '2024-03-26',
            'category': 'Tutorial',
            'content': '''
                Django can serve static files like CSS, JavaScript, and images.
                
                Setup static files:
                1. Create a 'static' directory in your app
                2. Use {% load static %} in templates
                3. Reference files with {% static 'path/to/file' %}
                
                This ensures proper file organization and CDN-readiness for production.
            '''
        },
    }
    
    post = posts.get(post_id)
    if post:
        return render(request, 'chapter5_blog_homepage/post_detail.html', {'post': post})
    else:
        return render(request, 'chapter5_blog_homepage/404.html', status=404)
