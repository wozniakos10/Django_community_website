from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import RegexValidator


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Delete profile when user is deleted
    name = models.CharField(max_length=40, blank=True, default="Brak informacji")
    surname = models.CharField(max_length=40, blank=True, default="Brak informacji")

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Numer telefonu musi być zapisany we formacie: +123456789 ")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    github_regex = RegexValidator(regex='^(http(s?):\/\/)?(www\.)?github\.([a-z])+\/([A-Za-z0-9]{1,})+\/?$',
                                  message="Podaj link do githuba!")
    github_url = models.CharField(validators=[github_regex], max_length=200, blank=True)
    contact_url = models.CharField(max_length=200, blank=True, default='Brak informacji')

    bio = models.TextField(max_length=500, blank=True, default="Brak informacji")
    country = CountryField(blank_label='Brak informacji', default='Brak informacji')

    def __str__(self):
        return f'{self.user.username} Profile'  # show how we want it to be displayed
