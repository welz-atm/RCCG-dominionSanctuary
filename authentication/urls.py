from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout_user/', views.logout_user, name='logout'),
    path('register_user/', views.register_user, name='register'),
    path('register_worker/', views.register_worker, name='register_worker'),
    path('users/', views.all_users, name='all_users'),
    path('edit_user/', views.edit_user, name='edit_user'),
]