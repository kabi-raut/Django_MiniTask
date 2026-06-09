from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    """Home page"""
    return render(request, 'chapter4_routing/home.html')


def about(request):
    """About page"""
    context = {
        'title': 'About Us',
        'description': 'Learn more about our web application'
    }
    return render(request, 'chapter4_routing/about.html', context)


def services(request):
    """Services page"""
    services_list = [
        {'name': 'Web Design', 'description': 'Beautiful and responsive web design'},
        {'name': 'Web Development', 'description': 'Full-stack web application development'},
        {'name': 'Database Design', 'description': 'Efficient database architecture'},
        {'name': 'Consulting', 'description': 'Expert consulting for your projects'},
    ]
    context = {'services': services_list}
    return render(request, 'chapter4_routing/services.html', context)


def contact(request):
    """Contact page"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # In a real app, you'd save this to database or send email
        context = {
            'submitted': True,
            'name': name
        }
        return render(request, 'chapter4_routing/contact.html', context)
    
    return render(request, 'chapter4_routing/contact.html')


def blog(request):
    """Blog listing page"""
    posts = [
        {
            'id': 1,
            'title': 'Getting Started with Django',
            'author': 'John Doe',
            'date': '2024-01-15',
            'excerpt': 'Learn the basics of Django web framework...'
        },
        {
            'id': 2,
            'title': 'Python Best Practices',
            'author': 'Jane Smith',
            'date': '2024-01-10',
            'excerpt': 'Write better Python code with these tips...'
        },
        {
            'id': 3,
            'title': 'Web Development Trends 2024',
            'author': 'Bob Johnson',
            'date': '2024-01-05',
            'excerpt': 'Explore the latest trends in web development...'
        },
    ]
    context = {'posts': posts}
    return render(request, 'chapter4_routing/blog.html', context)


def blog_detail(request, post_id):
    """Blog post detail page"""
    posts = {
        1: {
            'id': 1,
            'title': 'Getting Started with Django',
            'author': 'John Doe',
            'date': '2024-01-15',
            'content': 'Django is a powerful web framework. This comprehensive guide will help you get started with Django development. Django follows the MVT (Model-View-Template) architecture...'
        },
        2: {
            'id': 2,
            'title': 'Python Best Practices',
            'author': 'Jane Smith',
            'date': '2024-01-10',
            'content': 'Writing clean Python code is essential. Follow these best practices to improve your code quality. Use meaningful variable names, write docstrings, and follow PEP 8...'
        },
        3: {
            'id': 3,
            'title': 'Web Development Trends 2024',
            'author': 'Bob Johnson',
            'date': '2024-01-05',
            'content': 'The web development landscape is constantly evolving. In 2024, we see trends like AI integration, edge computing, and progressive web apps...'
        },
    }
    
    post = posts.get(post_id)
    if post:
        return render(request, 'chapter4_routing/blog_detail.html', {'post': post})
    else:
        return HttpResponse('Post not found', status=404)


def portfolio(request):
    """Portfolio page"""
    projects = [
        {
            'name': 'E-Commerce Platform',
            'description': 'Full-featured online store with payment integration',
            'technology': 'Django, PostgreSQL, Stripe'
        },
        {
            'name': 'Task Management App',
            'description': 'Collaborative task management tool',
            'technology': 'Django, React, Redis'
        },
        {
            'name': 'Data Analytics Dashboard',
            'description': 'Real-time data visualization and reporting',
            'technology': 'Django, Pandas, Chart.js'
        },
    ]
    context = {'projects': projects}
    return render(request, 'chapter4_routing/portfolio.html', context)
