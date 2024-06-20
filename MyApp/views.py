from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm, CustomUserCreationForm, ProfileUpdateForm, PostForm, CommentForm
from .models import Post, Profile, Comment, Reaction

def home(request):
    posts = Post.objects.all()
    return render(request, 'MyApp/home.html', {'posts': posts})

class CustomLoginView(LoginView):
    template_name = 'MyApp/login.html'

def custom_login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('news-home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            if not User.objects.filter(username=request.POST['username']).exists():
                messages.error(request, "Account with this user doesn't exist, please register.")
            else:
                messages.error(request, "Incorrect password!")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'MyApp/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Your account has been created! You are now logged in as {username}.')
            return redirect('news-home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'MyApp/register.html', {'form': form})

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
    return render(request, 'MyApp/profile.html', {'p_form': p_form})

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
    return render(request, 'MyApp/create_post.html', {'form': form})

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
    return render(request, 'MyApp/create_comment.html', {'form': form})

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
    return render(request, 'MyApp/post_detail.html', {'post': post, 'comments': comments})
