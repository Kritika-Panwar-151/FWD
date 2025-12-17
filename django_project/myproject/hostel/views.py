from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_signup(request):
    if request.method == 'POST':

        if 'signup' in request.POST:
            name = request.POST.get('fullname')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(username=email).exists():
                messages.error(request, "User already exists.", extra_tags='signup')
            else:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=name
                )
                user.save()
                messages.success(request, "Signup successful!", extra_tags='signup')
                return redirect('login_page')

        elif 'login' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)

            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid credentials", extra_tags='login')

    return render(request, 'login.html')


@login_required(login_url='/')
def home(request):
    return render(request, 'home.html')


def custom_logout(request):
    logout(request)
    return render(request, "logged_out.html")


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



@login_required
def hostel_detail(request, slug):

    HOSTELS = {
        "pink-petals": {
            "name": "Pink Petals PG",
            "image": "images/girls_hostel1.jpeg",
            "distance": "0.4 km from BMSCE",
            "facilities": [
                "Home-style Food",
                "2 / 3 Sharing Rooms",
                "High-Speed WiFi",
                "Common Study Area",
                "CCTV Surveillance",
                "Laundry Facility"
            ],
            "warden": {
                "name": "Mrs. Anitha Rao",
                "phone": "+91 91234 56789"
            },
            "map": "https://maps.google.com/maps?q=Basavanagudi%20Bangalore&t=&z=14&ie=UTF8&iwloc=&output=embed"
        },

        "lotus-ladies": {
            "name": "Lotus Ladies Hostel",
            "image": "images/girls_hostel2.jpeg",
            "distance": "0.8 km from BMSCE",
            "facilities": [
                "Vegetarian Meals",
                "Twin Sharing Rooms",
                "Lift Facility",
                "Terrace Garden",
                "24x7 Security"
            ],
            "warden": {
                "name": "Ms. Kavya Nair",
                "phone": "+91 99887 66554"
            },
            "map": "https://maps.google.com/maps?q=BMSCE&t=&z=14&ie=UTF8&iwloc=&output=embed"
        }
    }

    hostel = HOSTELS.get(slug)

    if not hostel:
        return redirect("girls_hostels")

    return render(request, "hostel_detail.html", {"hostel": hostel})