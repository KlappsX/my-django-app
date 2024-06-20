from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm

urlpatterns = [
    path('', views.home, name='news-home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='MyApp/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='MyApp/password_reset.html', form_class=CustomPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='MyApp/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='MyApp/password_reset_confirm.html', form_class=CustomSetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='MyApp/password_reset_complete.html'), name='password_reset_complete'),
    path('post/<int:post_id>/', views.post_detail, name='post-detail'),
    path('post/new/', views.create_post, name='post-create'),
    path('post/<int:post_id>/comment/', views.create_comment, name='comment-create'),
    path('post/<int:post_id>/react/<str:reaction_type>/', views.react_to_post, name='post-react'),
    path('comment/<int:comment_id>/react/<str:reaction_type>/', views.react_to_comment, name='comment-react'),
]
