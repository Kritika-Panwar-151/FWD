from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Profile, ContactMessage, Booking


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

                Profile.objects.create(user=user, gender=gender)

                messages.success(
                    request,
                    "Signup successful! Please log in.",
                    extra_tags='signup'
                )
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
# HOME
# =========================
@login_required(login_url='/')
def home(request):
    return render(request, 'home.html', {
        'gender': request.user.profile.gender
    })


# =========================
# LOGOUT
# =========================
def custom_logout(request):
    logout(request)
    return redirect('login_page')


# =========================
# BOOKINGS (PERMANENT)
# =========================
@login_required
def bookings(request):

    user_email = request.user.email

    # 🔍 CHECK EXISTING BOOKING (KEY FIX)
    existing_booking = Booking.objects.filter(email=user_email).first()

    # ---------- POST ----------
    if request.method == "POST":

        # ❌ BLOCK DUPLICATE BOOKINGS
        if existing_booking:
            return JsonResponse(
                {"status": "error", "message": "Booking already exists"},
                status=400
            )

        try:
            Booking.objects.create(
                name=request.POST.get("name"),
                email=user_email,  # 🔒 TRUST SERVER
                phone=request.POST.get("phone"),
                hostel_type=request.POST.get("hostel_type"),
                year=int(request.POST.get("year")),
                pref_1=request.POST.get("pref_1"),
                pref_2=request.POST.get("pref_2"),
                pref_3=request.POST.get("pref_3"),
            )
            return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)},
                status=400
            )

    # ---------- GET ----------
    gender = request.user.profile.gender

    BOYS = [
        ("blue_haven", "Blue Haven PG"),
        ("skyline", "Skyline Men’s Hostel"),
        ("metro_pg", "Metro PG"),
    ]

    GIRLS = [
        ("pink_petals", "Pink Petals PG"),
        ("lotus_ladies", "Lotus Ladies Hostel"),
        ("rose_residency", "Rose Residency"),
    ]

    if gender == "M":
        hostels = BOYS
        hostel_type_display = "Boys Hostel"
        hostel_type = "boys"
    else:
        hostels = GIRLS
        hostel_type_display = "Girls Hostel"
        hostel_type = "girls"

    return render(request, "bookings.html", {
        "existing_booking": existing_booking,  # 🔥 PERMANENT FLAG
        "hostels": hostels,
        "hostel_type_display": hostel_type_display,
        "hostel_type": hostel_type,
    })


# =========================
# GENDER RESTRICTED HOSTELS
# =========================
@login_required
def girls_hostels(request):
    if request.user.profile.gender != 'F':
        return redirect('home')
    return render(request, "girls_hostels.html")


@login_required
def boys_hostels(request):
    if request.user.profile.gender != 'M':
        return redirect('home')
    return render(request, "boys_hostels.html")


# =========================
# CONTACT
# =========================
@login_required
def contact(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),
        )
        messages.success(request, "We’ll reach out to you soon!")
        return redirect("contact")

    return render(request, "contact.html")


# =========================
# HOSTEL DETAILS
# =========================
@login_required
def hostel_detail_girls(request, slug):

    HOSTELS = {
        "pink-petals": {
            "name": "Pink Petals PG",
            "images": [
                "images/girls_hostel1.jpeg",
                "images/girls_hostel2.jpeg",
                "images/girls_hostel3.jpeg",
            ],
            "map": "https://maps.google.com/maps?q=BMSCE&output=embed"
        },
        "lotus-ladies": {
            "name": "Lotus Ladies Hostel",
            "map": "https://maps.google.com/maps?q=BMSCE&output=embed"
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
            "images": [
                "images/boys_hostel1.jpeg",
                "images/boys_hostel2.jpeg",
                "images/boys_hostel3.jpeg",
            ],
            "map": "https://maps.google.com/maps?q=BMSCE&output=embed"
        }
    }

    hostel = HOSTELS.get(slug)
    if not hostel:
        return redirect("boys_hostels")

    return render(request, "hostel_detail_boys.html", {"hostel": hostel})
