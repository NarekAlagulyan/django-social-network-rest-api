from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm

from PIL import Image
from captcha import fields as captcha_fields

from .apps import user_is_registered
from .models import User, Post, Comment
from .validators import cannot_starts_with_lower_validator, cannot_contain_digits_validator, \
    cannot_contain_punctuation_validator


class UserRegisterForm(forms.ModelForm):

    email = forms.EmailField(required=True, label='Email:')
    first_name = forms.CharField(
        required=False,
        validators=[
            cannot_starts_with_lower_validator,
            cannot_contain_digits_validator,
            cannot_contain_punctuation_validator
        ], help_text='First name cannot starts with lower case, contain any digit and contain any punctuation sign')

    last_name = forms.CharField(
        required=False,
        validators=[
            cannot_starts_with_lower_validator,
            cannot_contain_digits_validator,
            cannot_contain_punctuation_validator
        ], help_text='Last name cannot starts with lower case, contain any digit and contain any punctuation sign')

    captcha = captcha_fields.CaptchaField(required=True, label='Pass this CAPTCHA test')

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        label='Password:',
        help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        label='Confirm password:',
        help_text='Repeat the password'
    )

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        errors = {}
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            errors['password2'] = ValidationError('Password did not match to each other', 'invalid')

    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password1'])
        user.is_activated = False
        user.is_active = False
        if commit:
            user.save()
        user_is_registered.send(UserRegisterForm, instance=user)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'picture',
            'can_send_notification',
        )


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        label='Email:'
    )
    first_name = forms.CharField(
        validators=[
            cannot_starts_with_lower_validator,
            cannot_contain_digits_validator,
            cannot_contain_punctuation_validator
        ],
        required=False,
        help_text='First name cannot starts with lower case, contain any digit and contain any punctuation sign')

    last_name = forms.CharField(
        validators=[
            cannot_starts_with_lower_validator,
            cannot_contain_digits_validator,
            cannot_contain_punctuation_validator
        ],
        required=False,
        help_text='Last name cannot starts with lower case, contain any digit and contain any punctuation sign')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'about',
            'picture',
            'can_send_notification',
        )


class CustomPasswordResetForm(PasswordResetForm):
    captcha = captcha_fields.CaptchaField(required=True)


class PostCreateAndUpdateForm(forms.ModelForm):
    title = forms.CharField(
        max_length=30,
        required=True,
        validators=[cannot_starts_with_lower_validator],
        label='Title'
    )
    content = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label='Description'
    )

    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'picture',
        )

    def clean(self):
        errors = {}
        title = self.cleaned_data.get('title')
        content = self.cleaned_data.get('content')

        if title == content:
            errors['content'] = ValidationError(
                message='Post title and content cannot be the same',
                code='invalid'
            )
        if errors:
            raise ValidationError(errors)


class CommentForm(forms.Form):
    content = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label='Comment'
    )


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = ''

    content = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'search user'}),
    )
