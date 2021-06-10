import django.contrib.auth.models
from django.db import models
from django.db.models.signals import post_save
from django.db.models.aggregates import Count
from django.contrib.auth.models import AbstractUser
from django.db.models import Q, F
from django.utils.safestring import mark_safe
from django.utils.html import escape


from .utilities import send_new_comment_notification

# Create your models here.


PROFILE_PIC_LOCATION = 'user_picture'
DEFAULT_PROFILE_PIC = 'user_picture/def_pic.jpg'
POST_PIC_LOCATION = 'post_picture'


# implement user profile image =-=-============-=
class User(AbstractUser):
    is_activated = models.BooleanField(default=False, verbose_name='Does account activated?')
    can_send_notification = models.BooleanField(default=True, verbose_name='Allow to send notifications')
    picture = models.ImageField(
        upload_to=PROFILE_PIC_LOCATION,
        blank=True,
        default=DEFAULT_PROFILE_PIC,
        verbose_name='Profile picture'
    )
    about = models.TextField(null=True, blank=True, verbose_name='About me')
    slug = models.SlugField(verbose_name='Slug')

    def save(self, *args, **kwargs):
        self.slug = self.username
        return super().save(*args, **kwargs)

    @property
    def get_picture_url(self):
        return self.picture.url

    def get_img_html_tag(self):
        tag = f'<img src="{self.get_picture_url}" width="300px" class="rounded">'
        return mark_safe(tag)

    class Meta(AbstractUser.Meta):
        pass

    get_img_html_tag.short_description = 'User picture'
    get_img_html_tags = True


class MostPostUserManager(models.Manager):
    def get_queryset(self):
        q = Q(post_count__gt=0) & Q(is_active=True)
        return User.objects.annotate(post_count=Count('post')).filter(q).order_by('-post_count')[:5]


class MostPostUserProxy(User):
    objects = MostPostUserManager()

    class Meta:
        proxy = True
        verbose_name_plural = 'User with biggest amount of posts'
        verbose_name = 'user'


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Author')
    title = models.CharField(max_length=30, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    picture = models.ImageField(upload_to=POST_PIC_LOCATION, verbose_name='Post picture')
    likes = models.ManyToManyField(User, related_name='blog_posts', verbose_name='Likes')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Published date')
    slug = models.SlugField(verbose_name='Slug')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self.title
        return super().save(*args, **kwargs)

    @property
    def get_picture_url(self):
        return self.picture.url

    def get_img_html_tag(self):
        tag = f'<img src="{self.get_picture_url}" width="300px" class="rounded">'
        return mark_safe(tag)

    class Meta:
        verbose_name_plural = 'Posts'
        verbose_name = 'Post'
        ordering = ['-pub_date']

    get_img_html_tag.short_description = 'Image'
    get_img_html_tag.allow_tags = True


class MostLikedPostManager(models.Manager):
    def get_queryset(self):
        return Post.objects.annotate(like_count=Count('likes')).filter(like_count__gt=0).order_by('-like_count')[:3]


class MostLikedPostProxy(Post):
    objects = MostLikedPostManager()

    class Meta:
        proxy = True
        verbose_name_plural = 'Most liked posts'
        verbose_name = 'post'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post')
    content = models.TextField(verbose_name='Comment')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Published date')

    def __str__(self):
        return f'Comment to post "{self.post.title}" by user "{self.author.username}"'

    class Meta:
        verbose_name_plural = 'Comments'
        verbose_name = 'Comment'


def new_comment_dispatcher(sender, **kwargs):
    comment = kwargs['instance']
    post_author = comment.post.author

    if kwargs['created']:
        if post_author.can_send_notification:
            send_new_comment_notification(comment)


post_save.connect(new_comment_dispatcher, sender=Comment)