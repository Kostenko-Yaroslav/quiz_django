from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'
urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', next_page='core:index'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:index'), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]