from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.db.models import Q
from django.http import JsonResponse
from django.template import RequestContext

from .models import User, Post, Comment
from .forms import UserRegisterForm, UserUpdateForm, CustomPasswordResetForm, PostCreateAndUpdateForm, CommentForm
from .utilities import signer


# Create your views here.

def error_403_view(request, exception):
    return render(request, 'http_error/403.html')


def error_404_view(request, exception):
    return render(request, 'http_error/404.html')


def error_500_view(request, exception):
    return render(request, 'http_error/500.html')





class HomePageView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'main/home.html'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.select_related('author').all()


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = 'main/user_profile.html'
    model = Post
    paginate_by = 3
    context_object_name = 'posts'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.user_id)
        context['user_post_count'] = user.post_set.count()
        return context

    def get_queryset(self):
        queryset = Post.objects.select_related('author').filter(author=self.user_id)
        return queryset


class UserRegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'main/user_register.html'

    def get_success_message(self, cleaned_data):
        return f'''You registered successfully, 
        we sent message to your email {cleaned_data['email']} with activation link, 
        click that link to activate your account
        ''' % cleaned_data

    def get_success_url(self):
        return reverse('main:user_login')

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            self.template_name = 'main/user_already_in_system.html'
        return super().get(request, *args, **kwargs)


class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'main/user_update.html'
    success_message = 'Your account updated successfully'
    success_url = reverse_lazy('main:user_profile')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'main/user_delete.html'
    success_message = 'Your account deleted successfully'

    def get_success_url(self):
        return reverse('main:user_login')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserLoginView(UserPassesTestMixin, SuccessMessageMixin, LoginView):
    template_name = 'main/user_login.html'
    success_message = 'You are login successfully'

    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return False
        return True


class UserLogoutView(SuccessMessageMixin, LogoutView):
    template_name = 'main/user_logout.html'
    success_message = 'You are logout successfully'


class UserPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'main/user_password_reset.html'
    subject_template_name = 'email/user_password_reset_subject.txt'
    email_template_name = 'email/user_password_reset_template.txt'
    success_url = reverse_lazy('main:user_password_reset_done')

    def get_initial(self):
        return {'email': self.request.user.email}


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'main/user_password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'main/user_password_reset_confirm.html'
    success_url = reverse_lazy('main:user_password_reset_complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'main/user_password_reset_complete.html'


# activation view -=-=-==-

def activation_view(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(User, username=username)
    if user.is_activated and user.is_active:
        template = 'main/user_already_activated.html'
    else:
        template = 'main/user_activation_complete.html'
        user.is_activated = True
        user.is_active = True
        user.save()
    context = {'user': user}
    return render(request, template, context)


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostCreateAndUpdateForm
    template_name = 'main/post_create.html'
    success_url = reverse_lazy('main:home')
    success_message = 'Post successfully created!'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostCreateAndUpdateForm
    template_name = 'main/post_update.html'
    success_url = reverse_lazy('main:home')
    success_message = 'Post updated'

    def test_func(self):
        if not self.request.user == self.get_object().author:
            return False
        return True


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'main/post_delete.html'
    success_url = reverse_lazy('main:home')
    success_message = 'Post updated'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        post = self.get_object()
        if post.author.first_name and post.author.last_name:
            context['first_name'] = post.author.first_name
            context['last_name'] = post.author.last_name
        return context

    def test_func(self):
        post = self.get_object()
        if not post.author == self.request.user:
            return False
        return True


def user_post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            Comment.objects.create(author=request.user, post=post, content=content)
            return redirect('main:post_detail', pk=post.pk)
    else:
        context = {
            'post': post,
            'form': form,
        }
        return render(request, 'main/post_detail.html', context)


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'main/user_posts.html'
    paginate_by = 3

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = Post.objects.select_related('author').filter(author__username=username)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs['username'])
        context['user'] = user
        return context


@require_POST
def post_like_view(request):
    if request.method == 'POST':
        post = Post.objects.get(pk=request.POST['post_id'])

        if post.likes.filter(pk=request.user.pk).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        data = {
            'like_count': post.likes.count(),
            'post_liked': True if post.likes.filter(pk=request.user.pk).exists() else False
        }
        return JsonResponse(data, safe=False)


@require_POST
def search_redirect_view(request):
    content = request.POST['content']
    return redirect('main:search', content=content)


class UserSearchListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'main/searched_users.html'
    paginate_by = 2

    def get_queryset(self, **kwargs):
        search = self.kwargs['content']
        q = (Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search)) & Q(is_staff=False)
        return User.objects.filter(q)
