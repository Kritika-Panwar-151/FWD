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
        ("Himalaya", "Himalaya Hostel"),
        ("International-Hostel", "International Hostel"),
        ("Nandi", "Nandi Hostel"),
        ("Sapthagiri", "Sapthagiri Hostel"),
        ("Vidyapeeth", "Vidyapeeth Hostel")
    ]

    GIRLS_HOSTELS = [
        ("international-hostel", "International Hostel"),
        ("saraswati", "Saraswati Hostel"),
        ("sindhu", "Sindhu Hostel"),
        ("sbi", "Sbi Hostel"),
        ("yamuna", "Yamuna Hostel")
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
        "international-hostel": {
            "name": "International Hostel",
            "distance": "Incampus",
            "facilities": [
                "2 / 3 Sharing Rooms",
                "Common Washroom",
                "High-Speed WiFi",
                "Common Study Area",
                "CCTV Surveillance",
                "Lift Facility",
                "Washing Machine Facilty",
                "Special IH Mess",
                "Night Canteen",
                "24/7 Security",
                "No Gym facilty",
                "Open Terrace",
            ],
            "warden": {
                "name": "Mrs. Anitha Rao",
                "phone": "+91 91234 56789",
            },
            'images': [
                'images/Hostels/Girls/IH/1.jpeg', 
                'images/Hostels/Girls/IH/2.jpeg', 
                'images/Hostels/Girls/IH/3.jpeg', 
            ],
            "map": "https://maps.google.com/maps?q=Basavanagudi%20Bangalore&t=&z=14&ie=UTF8&iwloc=&output=embed"
        },

        "saraswati": {
            "name": "Saraswati Hostel",
            "distance": "400 m from BMSCE",
            "facilities": [
                "2 / 3 / 5 Sharing Rooms",
                "Attached Washroom",
                "High-Speed WiFi",
                "No Common Study Area",
                "CCTV Surveillance",
                "Lift Facility",
                "Washing Machine Facilty",
                "No Mess inside the hostel",
                "No Night Canteen",
                "24/7 Security",
                "No Gym Facility",
                "Open Terrace",
            ],
            "warden": {
                "name": "Ms. Kavya Nair",
                "phone": "+91 99887 66554",
            },
            'images': [
                'images/Hostels/Girls/Saraswati/1.jpeg', 
                'images/Hostels/Girls/Saraswati/2.jpeg',
                'images/Hostels/Girls/Saraswati/3.jpeg',
                'images/Hostels/Girls/Saraswati/4.jpeg',
            ],
            "map": "https://maps.google.com/maps?q=BMSCE&t=&z=14&ie=UTF8&iwloc=&output=embed"
        },

        "sindhu": {
            "name": "Sindhu Hostel",
            "distance": "100 m from BMSCE",
            "facilities": [
                "2 / 3 Sharing Rooms",
                "Attached Washroom",
                "High-Speed WiFi",
                "No Common Study Area",
                "CCTV Surveillance",
                "No Lift Facility",
                "Washing Machine Facilty",
                "No Mess inside the hostel",
                "No Night Canteen",
                "24/7 Security",
                "No Gym Facilty",
                "Open Terrace",
            ],
            "warden": {
                "name": "Mrs. Mona Sharma",
                "phone": "+91 91204 56789",
            },
            'images': [
                'images/Hostels/Girls/Sindhu/1.jpeg', 
                'images/Hostels/Girls/Sindhu/2.jpeg', 
                'images/Hostels/Girls/Sindhu/3.jpeg', 
            ],
            "map": "https://maps.google.com/maps?q=Basavanagudi%20Bangalore&t=&z=14&ie=UTF8&iwloc=&output=embed"
        },
        "sbi": {
            "name": "SBI Hostel",
            "distance": "400 m from BMSCE",
            "facilities": [
                "2 / 3 Sharing Rooms",
                "Attached Washroom",
                "High-Speed WiFi",
                "No Common Study Area",
                "CCTV Surveillance",
                "Lift Facility",
                "Washing Machine Facilty",
                "No Mess inside Hostel",
                "No Night Canteen",
                "24/7 Security",
                "No Gym facilty",
                "Open Terrace",
            ],
            "warden": {
                "name": "Mrs. Monica Patil",
                "phone": "+91 93345 56789",
            },
            'images': [
                'images/Hostels/Girls/Sbi/1.jpeg', 
                'images/Hostels/Girls/Sbi/2.jpeg', 
                'images/Hostels/Girls/Sbi/3.png', 
                'images/Hostels/Girls/Sbi/4.png', 
                'images/Hostels/Girls/Sbi/5.png', 
            ],
            "map": "https://maps.google.com/maps?q=Basavanagudi%20Bangalore&t=&z=14&ie=UTF8&iwloc=&output=embed"
        },
        "yamuna": {
            "name": "Yamuna Hostel",
            "distance": "50 m from BMSCE",
            "facilities": [
                "2 Sharing Rooms",
                "Attached Washroom",
                "High-Speed WiFi",
                "Common Study Area",
                "CCTV Surveillance",
                "Lift Facility",
                "Washing Machine Facilty",
                "No Mess inside Hostel",
                "No Night Canteen",
                "24/7 Security",
                "Gym facilty",
                "No Open Terrace",
            ],
            "warden": {
                "name": "Mrs. Jaya Teli",
                "phone": "+91 93345 52389",
            },
            'images': [
                'images/Hostels/Girls/Yamuna/1.jpeg', 
                'images/Hostels/Girls/Yamuna/2.jpeg', 
                'images/Hostels/Girls/Yamuna/3.jpeg', 
                'images/Hostels/Girls/Yamuna/4.jpeg', 
                'images/Hostels/Girls/Yamuna/5.png',  
                'images/Hostels/Girls/Yamuna/6.png', 
                'images/Hostels/Girls/Yamuna/7.png', 
            ],
            "map": "https://maps.google.com/maps?q=Basavanagudi%20Bangalore&t=&z=14&ie=UTF8&iwloc=&output=embed"
        }
    }

    hostel = HOSTELS.get(slug)

    if not hostel:
        return redirect("girls_hostels")

    return render(request, "hostel_detail_girls.html", {"hostel": hostel})


@login_required
def hostel_detail_boys(request, slug):

    HOSTELS = {
        "Himalaya": {
            "name": "Himalaya Hostel",
            "distance": "100 m from BMSCE",
            "facilities": [
                "Single Sharing Rooms",
                "Common Washroom",
                "High-Speed WiFi",
                "Common Study Area",
                "CCTV Surveillance",
                "Washing Machine Facilty",
                "No Mess inside the Hostel",
                "Night Canteen",
                "24/7 Security",
                "Gym facility",
                "Open Terrace"
            ],
            "warden": {
                "name": "Mr. Srinidhi",
                "phone": "+91 9986273000"
            },
            "images": [
                "images/Hostels/Boys/Himalaya/MH1.jpeg",
                "images/Hostels/Boys/Himalaya/MH2.jpeg",
                "images/Hostels/Boys/Himalaya/MH3.jpeg"
            ],
            "map": "https://maps.app.goo.gl/czjDh1i28RyVHhCx9"
        },

        "International-Hostel": {
            "name": "International Hostel",
            "distance": "Incampus",
            "facilities": [
                "2 / 3 Sharing Rooms",
                "Common Washroom",
                "High-Speed WiFi",
                "Common Study Area",
                "CCTV Surveillance",
                "Lift Facility",
                "Washing Machine Facilty",
                "Special IH Mess",
                "Night Canteen",
                "24/7 Security",
                "No Gym facilty",
                "Open Terrace"
            ],
            "warden": {
                "name": "Mrs. Anitha Rao",
                "phone": "+91 91234 56789"
            },
            'images': [
                'images/Hostels/Boys/IH/IH1.jpeg', 
                'images/Hostels/Boys/IH/IH2.jpeg', 
                'images/Hostels/Boys/IH/IH3.jpeg' 
            ],
            "map": "https://maps.google.com/maps?q=Basavanagudi%20Bangalore&t=&z=14&ie=UTF8&iwloc=&output=embed"
        },

        "Nandi": {
            "name": "Nandi Hostel",
            "distance": "700 m from BMSCE",
            "facilities": [
                "2 / 3 Sharing Rooms",
                "Attached Washroom",
                "High-Speed WiFi",
                "CCTV Surveillance",
                "Lift Facility",
                "Washing Machine Facilty",
                "Integrated Mess",
                "24/7 Security",
                "No Gym facility",
                "Open Terrace"
            ],
            "warden": {
                "name": "Mr. Raghavendra",
                "phone": "+91 98765 43210"
            },
            "images": [
                "images/Hostels/Boys/Nandi/N1.jpeg",
                "images/Hostels/Boys/Nandi/N2.jpeg",
                "images/Hostels/Boys/Nandi/N3.jpeg",
                "images/Hostels/Boys/Nandi/N4.jpeg"
            ],
            "map": "https://maps.google.com/maps?q=Basavanagudi%20Bangalore&output=embed"
        },

        "Sapthagiri": {
            "name": "Sapthagiri Hostel",
            "distance": "450 m from BMSCE",
            "facilities": [
                "2 / 3 Sharing Rooms",
                "Attached Washroom",
                "High-Speed WiFi",
                "CCTV Surveillance",
                "Lift Facility",
                "Washing Machine Facility",
                "No integrated Mess",
                "24/7 Security",
                "No Gym facility",
                "Open Terrace"
            ],
            "warden": {
                "name": "Mr. Kanishka Gupta",
                "phone": "+91 98765 43210"
            },
            "images": [
                "images/Hostels/Boys/Sapthagiri/S1.jpeg",
                "images/Hostels/Boys/Sapthagiri/S2.jpeg"
            ],
            "map": "https://maps.google.com/maps?q=Basavanagudi%20Bangalore&output=embed"
        },

        "Vidyapeeth": {
            "name": "Vidyapeeth Hostel",
            "distance": "900 m from BMSCE",
            "facilities": [
                "2 / 3 Sharing Rooms",
                "Attached Washroom",
                "High-Speed WiFi",
                "CCTV Surveillance",
                "Lift Facility",
                "Washing Machine Facility",
                "Integrated Mess",
                "24/7 Security",
                "No Gym facility",
                "Open Terrace"
            ],
            "warden": {
                "name": "Mr. Mandeep Singh",
                "phone": "+91 8252439516"
            },
            "images": [
                "images/Hostels/Boys/Vidyapeeth/V1.jpeg",
                "images/Hostels/Boys/Vidyapeeth/V2.jpeg"
            ],
            "map": "https://maps.google.com/maps?q=Basavanagudi%20Bangalore&output=embed"
        }

    }

    hostel = HOSTELS.get(slug)
    if not hostel:
        return redirect("boys_hostels")

    return render(request, "hostel_detail_boys.html", {"hostel": hostel})
