from django.template.loader import render_to_string
from django.core.signing import Signer


from my_social_network.settings import ALLOWED_HOSTS

signer = Signer()


def send_account_activation_notification(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {
        'host': host,
        'user': user,
        'sign': signer.sign(user.username)
    }
    subject = render_to_string('email/send_account_activation_notification_subject.txt', context)
    body = render_to_string('email/send_account_activation_notification_body.txt', context)

    user.email_user(
        subject=subject, message=body
    )


def send_new_comment_notification(comment):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'

    post_author = comment.post.author
    context = {
        'host': host,
        'author': post_author,
        'comment': comment,
    }
    subject = render_to_string('email/send_new_comment_notification_subject.txt', context)
    body = render_to_string('email/send_new_comment_notification_body.txt', context)
    post_author.email_user(
        subject=subject,
        message=body,
    )






















