from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount
from ckeditor_uploader.fields import RichTextUploadingField
from cloudinary.models import CloudinaryField


# Create your models here.

CATEGORY_OPTIONS = (
    ('Technology', 'Technology'),
    ('Health', 'Health'),
    ('International', 'International'),
    ('Politics', 'Politics'),
    ('Society', 'Society'),
    ('Economics', 'Economics'),
    ('Education', 'Education'),
    ('Tourism', 'Tourism'),
    ('Development', 'Development'),
    ('Food', 'Food'),
    ('Fashion', 'Fashion'),
    ('Entertainment', 'Entertainment')
)

FEATURED_OPTIONS = (('True','True'),('False','False'))

class AuthorFollowLinks(models.Model):
    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    google_plus_link = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Authors Follow Link'

    def __str__(self):
        return 'Facebook Link: ' + self.facebook_link


class Author(models.Model):
    first_name = models.CharField(max_length=20, verbose_name = 'First Name')
    last_name = models.CharField(max_length=20, verbose_name = 'Last Name')
    age = models.IntegerField()
    email = models.EmailField(max_length=30, unique=True, verbose_name= 'Email Address')
    phone = models.IntegerField()
    image = CloudinaryField('authorImages')
    #image= models.ImageField(upload_to='authorImages/', blank=True, null =True)
    description = models.CharField(max_length=100, blank=True, null=True, verbose_name="Short Info")
    links = models.ForeignKey(AuthorFollowLinks, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class BlogPost(models.Model):
    title = models.CharField(max_length=500)
    description = RichTextUploadingField()
    featured = models.CharField(max_length=5, default = 'False', choices=FEATURED_OPTIONS)
    slug = models.SlugField(max_length=200, unique=True)
    image = CloudinaryField('blogpostImages')
    #image = models.ImageField(upload_to='blogPostImages/', blank=True, null=True)
    posted = models.DateTimeField(auto_now_add=True, verbose_name='Posted On')
    category = models.CharField(max_length= 20, choices=CATEGORY_OPTIONS)
    author = models.ForeignKey(Author, default=1, null=1, on_delete=models.SET_NULL)
    posted = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Posted On')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Updated On')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    class Meta:
        verbose_name_plural = "Blog Posts"
        ordering = ['-updated', '-posted']

    def __str__(self):
        return self.title

    def __save__(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)

    def get_absolute_url(self):
         return reverse('home:details', kwargs={'slug': self.slug})


class PostImages(models.Model):
    post = models.ForeignKey(BlogPost, default=None, on_delete=models.CASCADE)
    image = CloudinaryField('postImages')
    #image = models.ImageField(upload_to='postImages/')

    class Meta:
        verbose_name_plural = "Post Images"

    def __str__(self):
        return self.post.title


class Contact(models.Model):
    email = models.EmailField(max_length=50, verbose_name="Email Address")
    subject = models.CharField(max_length=100)
    message = models.TextField()
    sent = models.DateTimeField(auto_now_add=True, verbose_name="Sent On")

    class Meta:
        verbose_name_plural = "Reader's Message"
        ordering = ['-sent']
    
    def __str__(self):
        return self.subject + ' : ' + self.email 


class Search(models.Model):
    user = models.CharField(max_length=20, blank=True)
    search = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add = True, verbose_name="Searched On")

    class Meta:
        verbose_name_plural = "Searched Queries"
        ordering = ['-timestamp']

    def __str__(self):
        return self.search + ' : ' + self.user + ' : ' + str(self.timestamp.date()) 


class Advertisement(models.Model):
    name = models.CharField(max_length=200, verbose_name='Advertisement Name')
    company = models.CharField(max_length=50, verbose_name='Advertisement Company')
    type = models.CharField(max_length=10, choices=(('Main', 'Main'), ('Side', 'Side')))
    image = CloudinaryField('adImages')
    #image = models.ImageField(upload_to='adImages')
    posted = models.DateTimeField(auto_now_add=True, verbose_name='Posted On')

    class Meta:
        verbose_name_plural = "Advertisements"
        ordering = ['-posted']

    def __str__(self):
        return self.name + 'from ' + self.company


class Subscriber(models.Model):
    subscriber = models.EmailField(max_length=30, unique=True, blank=False, null=False, verbose_name="Subscriber Email")
    subscribed = models.DateTimeField(auto_now_add=True, verbose_name='Subscribed On')

    class Meta:
        verbose_name_plural = 'Subscription List'
        ordering = ['-subscribed']
    
    def __str__(self):
        return self.subscriber


