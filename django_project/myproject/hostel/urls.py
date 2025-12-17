from django.contrib.auth import views as auth_views
from django.urls import include,path #include added
from . import views
urlpatterns = [
    path('', views.login_signup, name='login_page'),
    path('home/', views.home, name='home'),
    path("logout/", views.custom_logout, name="logout"),
    path("bookings/", views.bookings, name="bookings"), # New bookings page
    path('girls/', views.girls_hostels, name='girls_hostels'),
    path('boys/', views.boys_hostels, name='boys_hostels'),
    path("contact/", views.contact, name="contact"),



]
