from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # Choices for gender
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    # One profile per user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Gender field
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.user.username

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
