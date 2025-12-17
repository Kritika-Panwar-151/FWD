from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_signup, name='login_page'),
    path('home/', views.home, name='home'),
    path('logout/', views.custom_logout, name='logout'),
    path('bookings/', views.bookings, name='bookings'),
    path('girls/', views.girls_hostels, name='girls_hostels'),
    path('boys/', views.boys_hostels, name='boys_hostels'),
    path('contact/', views.contact, name='contact'),

    path('hostel/<slug:slug>/', views.hostel_detail, name='hostel_detail'),
]
