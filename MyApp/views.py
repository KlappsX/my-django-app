from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm, ProfileUpdateForm, PostForm, CommentForm
from .models import Post, Profile, Comment, Reaction

class CustomLoginView(LoginView):
    template_name = 'myapp/login.html'

def home(request):
    posts = Post.objects.all()
    return render(request, 'myapp/home.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Your account has been created! You are now logged in as {username}.')
            return redirect('news-home')
    else:
        form = UserRegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'myapp/profile.html', {'p_form': p_form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('news-home')
    else:
        form = PostForm()
    return render(request, 'myapp/create_post.html', {'form': form})

@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'myapp/create_comment.html', {'form': form})

@login_required
def react_to_post(request, post_id, reaction_type):
    post = get_object_or_404(Post, id=post_id)
    reaction, created = Reaction.objects.get_or_create(user=request.user, post=post, reaction_type=reaction_type)
    if not created:
        reaction.delete()
    return redirect('post-detail', post_id=post.id)

@login_required
def react_to_comment(request, comment_id, reaction_type):
    comment = get_object_or_404(Comment, id=comment_id)
    reaction, created = Reaction.objects.get_or_create(user=request.user, comment=comment, reaction_type=reaction_type)
    if not created:
        reaction.delete()
    return redirect('post-detail', post_id=comment.post.id)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'myapp/post_detail.html', {'post': post, 'comments': comments})