from django.template import Library

register = Library()


@register.filter(name='liked_by')
def post_liked_by_user_or_not(post, user):
    if user in post.likes.filter(username=user.username):
        return True
    return False

