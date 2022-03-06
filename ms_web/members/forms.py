from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'style': 'max-width: 18em'}),
        error_messages={'unique': "A user with that username address already exists."}
    )
    email = forms.EmailField(
        max_length=64,
        widget=forms.TextInput(attrs={'style': 'max-width: 18em'}),
        error_messages={'unique': "A user with that email address already exists."}
    )
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={'style': 'max-width: 18em'}),
                                error_messages={
                                    'password_mismatch': "The two password fields didn't match.",
                                },
                                help_text="Password must contain at least 8 characters.",
                                help_text_color = "white"

                                )
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput(attrs={'style': 'max-width: 18em'}),
                                error_messages={
                                    'password_mismatch': "The two password fields didn't match.",
                                },
                                help_text="Enter the same password as above, for verification."
                                )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]