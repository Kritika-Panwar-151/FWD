from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Profile, ContactMessage   # ContactMessage added


# =========================
# LOGIN + SIGNUP
# =========================
def login_signup(request):
    if request.method == 'POST':

        # ---------- SIGNUP ----------
        if 'signup' in request.POST:
            name = request.POST.get('fullname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            gender = request.POST.get('gender')

            if User.objects.filter(username=email).exists():
                messages.error(request, "User already exists.", extra_tags='signup')
            else:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=name
                )

                # Create profile with gender
                Profile.objects.create(
                    user=user,
                    gender=gender
                )

                messages.success(request, "Signup successful! Please log in.", extra_tags='signup')
                return redirect('login_page')

        # ---------- LOGIN ----------
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


# =========================
# HOME (Gender Based)
# =========================
@login_required(login_url='/')
def home(request):
    gender = request.user.profile.gender
    return render(request, 'home.html', {'gender': gender})


# =========================
# LOGOUT (Instant)
# =========================
def custom_logout(request):
    logout(request)
    return redirect('login_page')


# =========================
# STATIC PAGES
# =========================
@login_required
def bookings(request):
    gender = request.user.profile.gender

    BOYS_HOSTELS = [
        ("blue_haven", "Blue Haven PG"),
        ("skyline", "Skyline Men’s Hostel"),
        ("metro_pg", "Metro PG"),
    ]

    GIRLS_HOSTELS = [
        ("pink_petals", "Pink Petals PG"),
        ("lotus_ladies", "Lotus Ladies Hostel"),
        ("rose_residency", "Rose Residency"),
    ]

    # Select hostel list based on gender
    if gender == "M":
        hostels = BOYS_HOSTELS
        hostel_type_display = "Boys Hostel"
    else:
        hostels = GIRLS_HOSTELS
        hostel_type_display = "Girls Hostel"

    context = {
        "hostels": hostels,
        "hostel_type_display": hostel_type_display,
        "hostel_type": "boys" if gender == "M" else "girls",
    }

    return render(request, "bookings.html", context)



@login_required
def girls_hostels(request):
    # Optional safety check
    if request.user.profile.gender != 'F':
        return redirect('home')
    return render(request, "girls_hostels.html")


@login_required
def boys_hostels(request):
    # Optional safety check
    if request.user.profile.gender != 'M':
        return redirect('home')
    return render(request, "boys_hostels.html")


# =========================
# CONTACT (BACKEND ADDED)
# =========================
@login_required
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # Save message to DB
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")

    return render(request, "contact.html")


# =========================
# HOSTEL DETAIL PAGE
# =========================
@login_required
def hostel_detail_girls(request, slug):

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
            'images': [
                'images/girls_hostel1.jpeg', 
                'images/girls_hostel2.jpeg', 
                'images/girls_hostel3.jpeg', 
            ],
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

    return render(request, "hostel_detail_girls.html", {"hostel": hostel})


@login_required
def hostel_detail_boys(request, slug):

    HOSTELS = {
        "blue-haven": {
            "name": "Blue Haven PG",
            "distance": "0.4 km from BMSCE",
            "facilities": [
                "North & South Indian Meals",
                "2 / 3 Sharing Rooms",
                "High-Speed WiFi",
                "Gym Facility",
                "CCTV Security",
                "Laundry"
            ],
            "warden": {
                "name": "Mr. Raghavendra",
                "phone": "+91 98765 43210"
            },
            "images": [
                "images/boys_hostel1.jpeg",
                "images/boys_hostel2.jpeg",
                "images/boys_hostel3.jpeg"
            ],
            "map": "https://maps.google.com/maps?q=Basavanagudi%20Bangalore&output=embed"
        }
    }

    hostel = HOSTELS.get(slug)
    if not hostel:
        return redirect("boys_hostels")

    return render(request, "hostel_detail_boys.html", {"hostel": hostel})
