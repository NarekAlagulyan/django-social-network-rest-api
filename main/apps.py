from django.apps import AppConfig
from django.dispatch import Signal

from .utilities import send_account_activation_notification


user_is_registered = Signal(providing_args=['instance'])


def user_is_registered_dispatch(sender, **kwargs):
    send_account_activation_notification(kwargs['instance'])


user_is_registered.connect(user_is_registered_dispatch)


class MainConfig(AppConfig):
    name = 'main'
