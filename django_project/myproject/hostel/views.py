from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile

from django.shortcuts import redirect
from django.contrib.auth import logout

def login_signup(request):
    if request.method == 'POST':
        # --- SIGNUP ---
        if 'signup' in request.POST:
            name = request.POST.get('fullname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            gender = request.POST.get('gender')  # NEW

            if User.objects.filter(username=email).exists():
                messages.error(request, "User already exists. Please log in.", extra_tags='signup')
            else:
                user = User.objects.create_user(
                    username=email, email=email, password=password, first_name=name
                )
                Profile.objects.create(
                user=user,
                gender=gender
                )
                user.save()
                messages.success(request, "Signup successful! Please log in.", extra_tags='signup')
                return redirect('login_page')

        # --- LOGIN ---
        elif 'login' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password. Please try again or sign up.", extra_tags='login')

    return render(request, 'login.html')



@login_required(login_url='/')
def home(request):
    gender = request.user.profile.gender  # get gender

    context = {
        'gender': gender
    }
    return render(request, 'home.html', context)



def custom_logout(request):
    logout(request)
    return redirect('login_page')

@login_required
def bookings(request):
    return render(request, "bookings.html")

@login_required
def girls_hostels(request):
    return render(request, "girls_hostels.html")

@login_required
def boys_hostels(request):
    return render(request, "boys_hostels.html")

@login_required
def contact(request):
    return render(request, "contact.html")
