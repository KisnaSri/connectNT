from . models import Author, BlogPost, Contact, Search, Advertisement, Subscriber, PostImages
from . forms import ContactForm, SubscriberForm
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.forms import modelform_factory
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.forms import ModelForm


flag = 0
PAGINATION_NUMBER = 8
categories = {'Technology' : 1, 'Politics' : 2, 'Society' : 3, 'Economics' : 4, 'Education' : 1, 'Tourism' : 2,
                'Development' : 3,'Food' : 4, 'Fashion' : 1, 'Health' : 2, 'Entertainment' : 3, 'International' : 4}

def popular_posts_details():
    popular_posts_details = BlogPost.objects.order_by('-hit_count_generic__hits')[:4]
    popular_posts_details_categories = [post.category for post in popular_posts_details]
    popular_posts_details_colors = [categories[category] for category in popular_posts_details_categories]
    return zip(popular_posts_details, popular_posts_details_colors)


def advertisement(request):    
    context = {
        'main_adv':main_adv(),
        'side_adv':side_adv()
    }
    return render(request, 'home/advertisement.html', context)

def main_adv():
    return Advertisement.objects.all().filter(type='Main')

def side_adv():
    return Advertisement.objects.all().filter(type='Side') 

def categories_counts(posts):
    post_categories = [post.category for post in posts]
    categories_count = [post_categories.count(key) for key in categories.keys()] 
    return zip(categories.keys(), categories.values(), categories_count)

def home(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            subscriber = form.cleaned_data['subscriber']
            try:
                send_mail(subject="Subscription Message", message="Welcome to our Newsletter!! \nYou won't miss our recent updates. \nThanks.", from_email=settings.EMAIL_HOST_USER, recipient_list=[subscriber], fail_silently=False)
            except:
                pass

            try:
                subscriber = Subscriber(subscriber=subscriber)
                subscriber.save()
                messages.success(request, 'Subscribed Successfully, Congratulations!!!')
            except:
                messages.error(request, 'Welcome Back!!, Already Subscribed' )
        else:
            messages.error(request, 'Error!! Invalid Email, TRY AGAIN !!')

    posts = BlogPost.objects.all()
    featured_posts = posts.filter(featured = 'True')[:3]
    categories_colors_counts = categories_counts(posts)

    post_categories = [post.category for post in posts]
    colors = [categories[category] for category in post_categories]  
    featured_post_categories = [post.category for post in featured_posts]
    featured_colors = [categories[category] for category in featured_post_categories]    
    
    hero_posts = zip(posts[0:2], colors[0:2])    
    recent_posts = zip(posts[2:8], colors[2:8])
    sub_hero_posts = zip(posts[8:9], colors[8:9])
    sub_posts = zip(posts[9:15], colors[9:15])
    featured_posts = zip(featured_posts, featured_colors)

    context = {
        'hero_posts': hero_posts, 
        'recent_posts': recent_posts,
        'sub_hero_posts': sub_hero_posts,
        'sub_posts': sub_posts,
        'featured_posts': featured_posts,
        'popular_posts': BlogPost.objects.order_by('-hit_count_generic__hits')[:10],
        'popular_posts_details': popular_posts_details(),
        'categories_colors_counts': categories_colors_counts,
        'form': SubscriberForm(),
        'main_adv': main_adv(),
        'side_adv': side_adv()
    }
    return render(request, 'home/index.html', context)


def details(request, slug):
    global flag
    if flag == 0:    
        posts = BlogPost.objects.all()
        my_posts = posts
    else:
        posts = my_posts
        flag = 1
    print(flag)
    categories_colors_counts = categories_counts(posts)
    count_hit = True
    post = get_object_or_404(BlogPost, slug = slug) #after hitcount_tag added at posts.html
    hit_count = HitCount.objects.get_for_object(post)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    context={
        'post':post,
        'categories_colors_counts':categories_colors_counts,
        'main_adv':main_adv(),
        'side_adv':side_adv()
        }
    return render (request, 'home/post-details.html', context)


def posts(request, category):
    all_posts = BlogPost.objects.all()
    search_query = request.GET.get('q')
    search_message = ''
    PAGE_RANGE = ''
    if search_query:
        searched_posts = all_posts.filter(Q(title__icontains = search_query))
        posts = searched_posts
        search = Search(user=request.user, search=search_query)
        search.save()
        if not posts:
            search_message = '<h3> Sorry, your search hit no results. </h3>'
    else:
        if category == 'posts':
            posts = all_posts
        elif category == 'Popular':
            posts = BlogPost.objects.order_by('-hit_count_generic__hits')
        else:
            posts = all_posts.filter(category = category)

    paginator = Paginator(posts, PAGINATION_NUMBER)
    page = request.GET.get('page', 1)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(PAGINATION_NUMBER)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    index = posts.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    categories_colors_counts = categories_counts(all_posts)

    post_categories = [post.category for post in posts]
    colors = [categories[category] for category in post_categories]
    posts_colors = zip(posts, colors) 
    
    context={
        'category':category,
        'posts':posts,
        'posts_colors': posts_colors,
        'popular_posts': BlogPost.objects.order_by('-hit_count_generic__hits')[:10],
        'query': search_query,
        'page_range': page_range,
        'categories_colors_counts': categories_colors_counts,
        'search_message': search_message, 
        'main_adv': main_adv(),
        'side_adv': side_adv()
    }
    return render(request, 'home/posts.html', context)


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                contact = Contact(email=email, subject=subject, message=message)
                contact.save()
                messages.success(request, 'Submitted Successfully, Thank You!!')
                return redirect('home')
            except:
                messages.error(request, "Error Sending Message, Please Try Again !!")
                return render(request,'home/contact.html', context={'form':form})
        else:
            messages.error(request, 'Error Sending Message, Please Try Again !!')
            return render(request, "home/contact.html", context={'form':form})
    return render(request,'home/contact.html', context={'form':form})


def about(request):
    context ={
        'authors': Author.objects.all(),
        'main_adv':main_adv(),
        'side_adv':side_adv()
    }
    return render(request, 'home/about.html', context)

    
def join(request):    
    context = {
        'main_adv':main_adv(),
        'side_adv':side_adv()
    }
    return render(request, 'home/join.html', context)

def privacy(request):
    return render(request, 'home/privacy.html')

def test(request):
    posts = BlogPost.objects.all()
    return render(request, 'home/test.html', {'posts':posts})

def error_404(request, exception):
    return render(request, 'home/error_404.html', status='404')

def error_500(request):
    return render(request, 'home/error_500.html', status='500')