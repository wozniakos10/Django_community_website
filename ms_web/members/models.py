from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Delete profile when user is deleted
    name = models.CharField(max_length=40, blank=True, default="Brak informacji")
    surname = models.CharField(max_length=40, blank=True, default="Brak informacji")
    phone = models.CharField(max_length=40, blank=True, default="Brak informacji")
    bio = models.TextField(max_length=500, blank=True, default="Brak informacji")

    def __str__(self):
        return f'{self.user.username} Profile'  # show how we want it to be displayed
