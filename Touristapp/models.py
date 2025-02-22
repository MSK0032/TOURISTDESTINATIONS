from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class TouristDestination(models.Model):
    place_name = models.CharField(max_length=255)
    tourist_img = models.ImageField(upload_to='places/', blank=True, null=True)
    weather = models.CharField(max_length=100)
    location_state = models.CharField(max_length=100)
    location_district = models.CharField(max_length=100)
    google_map_link = models.URLField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.place_name



class TouristImage(models.Model):
    destination = models.ForeignKey(TouristDestination, related_name='images', on_delete=models.CASCADE)
    place_name = models.CharField(max_length=255)
    Tourist_img = models.ImageField(upload_to='more_images/')

class CustomUser(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    confirm_password = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.username)

class Request(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    destination = models.ForeignKey(TouristDestination, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.destination.place_name} ({self.status})"
