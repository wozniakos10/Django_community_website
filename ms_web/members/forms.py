from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
#from captcha.fields import  CaptchaField
from .models import Profile
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django_countries import countries


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Nazwa użytkownika',
        max_length=64,
        widget=forms.TextInput(attrs={'style': 'max-width: 18em'}),
        error_messages={'unique': "A user with that username address already exists."}
    )
    email = forms.EmailField(
        max_length=64,
        widget=forms.TextInput(attrs={'style': 'max-width: 18em'}),
        error_messages={'Email already exists': "Konto z podanym adresem email już istnieje."}
    )
    password1 = forms.CharField(label="Hasło",
                                widget=forms.PasswordInput(attrs={'style': 'max-width: 18em'}),
                                error_messages={
                                    'password_mismatch': "The two password fields didn't match.",
                                },
                                help_text="Hasło musi zawierać co najmniej 8 znaków",

                                )
    password2 = forms.CharField(label="Powtórz hasło",
                                widget=forms.PasswordInput(attrs={'style': 'max-width: 18em'}),
                                error_messages={
                                    'password_mismatch': "The two password fields didn't match.",
                                }

                                )

    #=git captcha =  CaptchaField()


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Konto z podanym adresem email już istnieje.")
        return email

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name','surname','phone','bio','github_url','contact_url','country']

        labels = {
            'name': 'Imię',
            'surname': 'Nazwisko',
            'phone': 'Numer telefonu',
            'bio': 'Biogram',
            'github_url': 'Github',
            'contact_url': 'Kontakt',
            'country':'Kraj pochodzenia'
        }

        widgets = {'country' : CountrySelectWidget(attrs={'class': 'form-select',
                                                          'style': 'width:auto',
                                                          'blank_label': ''},
        layout='{widget}<img alt="" class="country-select-flag"  id="{flag_id}" style="margin: 10px 4px 0" src="{country.flag}">' ),
                   'name': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
                   'surname': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
                   'phone': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
                   'bio':   forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
                   'github_url': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
                   'contact_url': forms.Textarea(attrs={'class': 'form-control', 'rows': 5})





                   }