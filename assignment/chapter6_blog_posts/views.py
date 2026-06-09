from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Category


def post_list(request):
    """Display all published posts with pagination"""
    posts = Post.objects.filter(is_published=True).select_related('category')
    
    # Pagination
    paginator = Paginator(posts, 5)  # 5 posts per page
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    
    context = {
        'posts': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'chapter6_blog_posts/post_list.html', context)


def post_detail(request, slug):
    """Display single post detail"""
    post = get_object_or_404(Post, slug=slug, is_published=True)
    post.increment_views()
    
    # Get related posts from same category
    related_posts = Post.objects.filter(
        category=post.category, 
        is_published=True
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'chapter6_blog_posts/post_detail.html', context)


def category_posts(request, slug):
    """Display posts by category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(
        category=category, 
        is_published=True
    ).select_related('category')
    
    # Pagination
    paginator = Paginator(posts, 5)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    
    context = {
        'category': category,
        'posts': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'chapter6_blog_posts/category_posts.html', context)


def categories_list(request):
    """Display all categories"""
    categories = Category.objects.annotate(
        post_count=Count('posts', filter=Q(posts__is_published=True))
    )
    
    context = {
        'categories': categories,
    }
    return render(request, 'chapter6_blog_posts/categories_list.html', context)


from django.db.models import Count, Q


def index(request):
    """Blog homepage"""
    featured_posts = Post.objects.filter(is_published=True)[:3]
    latest_posts = Post.objects.filter(is_published=True)[:5]
    categories = Category.objects.all()
    
    context = {
        'featured_posts': featured_posts,
        'latest_posts': latest_posts,
        'categories': categories,
        'total_posts': Post.objects.filter(is_published=True).count(),
    }
    return render(request, 'chapter6_blog_posts/index.html', context)
