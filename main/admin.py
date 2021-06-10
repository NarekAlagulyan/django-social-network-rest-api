from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User, Post, Comment

# Register your models here.


class UserAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'is_activated', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fields = (
        ('username', 'email'),
        ('first_name', 'last_name', 'slug'),
        ('about', 'get_img_html_tag', 'picture'),
        ('is_activated',),
        ('can_send_notification',),
        ('date_joined',)
    )
    readonly_fields = ('date_joined', 'slug', 'can_send_notification', 'is_activated', 'get_img_html_tag')


class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'get_likes_count', 'pub_date')
    search_fields = ('author', 'title', 'content', 'pub_date')
    fields = (
        ('title', 'author'),
        ('content', 'get_img_html_tag'),
        ('picture', 'likes'),
        ('pub_date',)
    )
    readonly_fields = ('pub_date', 'get_img_html_tag')

    @admin.display(description='Count of post likes')
    def get_likes_count(self, post):
        return post.likes.count()


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'pub_date')
    search_fields = ('author', 'content', 'pub_date')
    fields = (
        ('author',),
        ('post',),
        ('content',),
        ('pub_date',)
    )
    readonly_fields = ('pub_date', 'author', 'post',)


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
