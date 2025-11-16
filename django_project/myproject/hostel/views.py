from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout   # <-- IMPORTANT
from django.contrib.auth.decorators import login_required

def login_signup(request):
    if request.method == 'POST':
        # --- SIGNUP ---
        if 'signup' in request.POST:
            name = request.POST.get('fullname')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(username=email).exists():
                messages.error(request, "User already exists. Please log in.", extra_tags='signup')
            else:
                user = User.objects.create_user(
                    username=email, email=email, password=password, first_name=name
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


@login_required
def home(request):
    return render(request, 'home.html')


def custom_logout(request):
    logout(request)  # logs out user
    return render(request, "logged_out.html")  # show message + redirect in HTML
