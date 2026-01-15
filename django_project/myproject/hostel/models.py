from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator



# USER PROFILE

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.user.username



# CONTACT FORM

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"



# HOSTEL BOOKING

phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be exactly 10 digits"
)

class Booking(models.Model):

    HOSTEL_TYPE_CHOICES = [
        ('boys', 'Boys Hostel'),
        ('girls', 'Girls Hostel'),
    ]

    #ONE BOOKING PER USER / EMAIL
    email = models.EmailField(unique=True)

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10,validators=[phone_validator])

    usn = models.CharField(max_length=20, unique=True)


    hostel_type = models.CharField(
        max_length=10,
        choices=HOSTEL_TYPE_CHOICES
    )

    year = models.PositiveSmallIntegerField()

    pref_1 = models.CharField(max_length=100)
    pref_2 = models.CharField(max_length=100)
    pref_3 = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.hostel_type}"
