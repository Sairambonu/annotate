from django.urls import path
from . import views

urlpatterns = [
	path('', views.index_page, name='index_page'),
    path('login/', views.user_login, name='login'), # Use Django's built-in authentication views
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('change_password/', views.change_password, name='change_password'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('endpoint/', views.endpoint, name='endpoint'),
]