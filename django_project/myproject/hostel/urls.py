from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
urlpatterns = [
    path('', views.login_signup, name='login_page'),
    path('home/', views.home, name='home'),
    path("logout/", views.custom_logout, name="logout"),


]
