"""
URL configuration for aSimpleProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MyApp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='news-home'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('post/<int:post_id>/', views.post_detail, name='post-detail'),
    path('post/new/', views.create_post, name='post-create'),
    path('post/<int:post_id>/comment/', views.create_comment, name='comment-create'),
    path('post/<int:post_id>/react/<str:reaction_type>/', views.react_to_post, name='post-react'),
    path('comment/<int:comment_id>/react/<str:reaction_type>/', views.react_to_comment, name='comment-react'),
]
