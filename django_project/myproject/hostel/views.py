from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import Booking

from .models import Profile, ContactMessage, Booking



# LOGIN + SIGNUP

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



# HOME

@login_required(login_url='/')
def home(request):
    return render(request, 'home.html', {
        'gender': request.user.profile.gender
    })



# LOGOUT

def custom_logout(request):
    logout(request)
    return redirect('login_page')



# BOOKINGS (PERMANENT)

def check_usn(request):
    usn = request.GET.get('usn', None)
    # Returns True if USN exists, False otherwise
    is_taken = Booking.objects.filter(usn__iexact=usn).exists()
    return JsonResponse({'is_taken': is_taken})

@login_required
def bookings(request):
    user_email = request.user.email
    existing_booking = Booking.objects.filter(email=user_email).first()

    # 1. Mapping Dictionary: Converts technical values to the actual names you want shown
    HOSTEL_NAMES = {
        "Himalaya": "Himalaya Hostel",
        "International-Hostel": "International Hostel",
        "international-hostel": "International Hostel",
        "Nandi": "Nandi Hostel",
        "Sapthagiri": "Sapthagiri Hostel",
        "Vidyapeeth": "Vidyapeeth Hostel",
        "saraswati": "Saraswati Hostel",
        "sindhu": "Sindhu Hostel",
        "sbi": "Sbi Hostel",
        "yamuna": "Yamuna Hostel",
    }

    # 2. Display Logic for the Success Card
    booking_display = None
    if existing_booking:
        booking_display = {
            "name": existing_booking.name,
            "email": existing_booking.email,
            "usn": existing_booking.usn,
            "phone": existing_booking.phone,
            "hostel": existing_booking.hostel_type.capitalize() + " Hostel",
            "year": existing_booking.year,
            # This looks up the name in the dictionary. If it can't find it, it uses the raw ID.
            "pref_1": HOSTEL_NAMES.get(existing_booking.pref_1, existing_booking.pref_1),
            "pref_2": HOSTEL_NAMES.get(existing_booking.pref_2, existing_booking.pref_2),
            "pref_3": HOSTEL_NAMES.get(existing_booking.pref_3, existing_booking.pref_3),
        }

    # 3. Form Submission logic (POST)
    if request.method == "POST":
        if existing_booking:
            messages.error(request, "You have already submitted a booking.")
            return redirect("bookings")

        phone = request.POST.get("phone")
        usn = request.POST.get("usn")

        # Validation
        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect("bookings")

        if len(usn) != 10:
            messages.error(request, "USN must be exactly 10 characters.")
            return redirect("bookings")

        if Booking.objects.filter(usn=usn).exists():
            messages.error(request, "This USN is already registered.")
            return redirect("bookings")

        try:
            Booking.objects.create(
                name=request.POST.get("name"),
                email=user_email,
                usn=usn,
                phone=phone,
                hostel_type=request.POST.get("hostel_type"),
                year=int(request.POST.get("year")),
                pref_1=request.POST.get("pref_1"),
                pref_2=request.POST.get("pref_2"),
                pref_3=request.POST.get("pref_3"),
            )
            messages.success(request, "Booking submitted successfully!")
            return redirect("bookings")
        except Exception:
            messages.error(request, "Something went wrong. Please try again.")
            return redirect("bookings")

    # 4. GET logic (Dropdown lists)
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
        ("yamuna", "Yamuna Hostel"),
    ]

    if gender == "M":
        hostels = BOYS_HOSTELS
        hostel_type_display = "Boys Hostel"
        hostel_type = "boys"
    else:
        hostels = GIRLS_HOSTELS
        hostel_type_display = "Girls Hostel"
        hostel_type = "girls"

    return render(request, "bookings.html", {
        "existing_booking": existing_booking,
        "booking_display": booking_display,
        "hostels": hostels,
        "hostel_type_display": hostel_type_display,
        "hostel_type": hostel_type,
    })



# GENDER RESTRICTED HOSTELS

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



# CONTACT

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



# HOSTEL DETAILS

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
            "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d734.9035799974403!2d77.56373140879737!3d12.93875727578748!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae15005f98015f%3A0x7cb9fe1b8fade2ea!2sBhoomika!5e0!3m2!1sen!2sin!4v1766545419635!5m2!1sen!2sin"
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
            "map": "https://www.google.com/maps/embed?pb=!4v1766544943516!6m8!1m7!1sEqKplMRGDr0ngRS3IP1MOg!2m2!1d12.93976656536628!2d77.56552222397191!3f200.530635752027!4f24.023951524013086!5f0.7820865974627469"
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
                
            ],
            "map": "https://www.google.com/maps/embed?pb=!4v1766545044846!6m8!1m7!1sq9ZNtO9mslTcv2OoLNVDmQ!2m2!1d12.94075896208654!2d77.5643480260269!3f315.49415467126073!4f22.10950895199869!5f0.7820865974627469"
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
            "map": "https://www.google.com/maps/embed?pb=!4v1766544891705!6m8!1m7!1sCn0qGJciLBUoMkdPTf21WQ!2m2!1d12.93977622125206!2d77.56561720176323!3f47.44767376796364!4f16.801678076964677!5f0.7820865974627469"  
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
                "images/Hostels/Boys/Himalaya/MH3.jpeg",
                "images/Hostels/Boys/Himalaya/MH4.jpeg"
            ],
            "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3888.4720098413404!2d77.56423497454614!3d12.941620315535925!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae158b11e34d2f%3A0x5f4adbdbab8bd80f!2sBMS%20College%20of%20Engineering!5e0!3m2!1sen!2sin!4v1766545032514!5m2!1sen!2sin"
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
            "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3888.4720098413404!2d77.56423497454614!3d12.941620315535925!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae158b11e34d2f%3A0x5f4adbdbab8bd80f!2sBMS%20College%20of%20Engineering!5e0!3m2!1sen!2sin!4v1766545032514!5m2!1sen!2sin"
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
            "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3888.4158757818327!2d77.5656742745462!3d12.945219215457197!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae1533701ca961%3A0xba9753f5ed73144f!2sNandi%20Block%2C%20NBH-7%20BMSETH!5e0!3m2!1sen!2sin!4v1766544929659!5m2!1sen!2sin" 
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
                "images/Hostels/Boys/Sapthagiri/S2.jpeg",
                "images/Hostels/Boys/Sapthagiri/S3.jpeg"
            ],
            "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3888.538618027471!2d77.55994087454606!3d12.937348615629391!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae15002b74c61b%3A0x1460c06426f40124!2sSapthagiri%20Block%20BMSET%20Boys%20hostel!5e0!3m2!1sen!2sin!4v1766544867910!5m2!1sen!2sin"
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
                "images/Hostels/Boys/Vidyapeeth/V2.jpeg",
                "images/Hostels/Boys/Vidyapeeth/V3.jpeg",
                "images/Hostels/Boys/Vidyapeeth/V4.jpeg"
            ],
            "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3888.5892711188644!2d77.55760357454606!3d12.934099215700424!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae3f00775ccc21%3A0xb60ed9d1a4fd34eb!2sVidyapeeta%20Block(NBH-14)%20BMSETH!5e0!3m2!1sen!2sin!4v1766544614840!5m2!1sen!2sin"
        }

    }

    hostel = HOSTELS.get(slug)
    if not hostel:
        return redirect("boys_hostels")

    return render(request, "hostel_detail_boys.html", {"hostel": hostel})
