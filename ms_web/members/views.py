from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth import logout


from django.contrib.auth import get_user_model
from django_email_verification import send_email

from django.views.decorators.csrf import csrf_exempt

from datetime import timedelta
from ratelimit.decorators import ratelimit
from blacklist.ratelimit import blacklist_ratelimited

# Create your views here.

# if user or ip tried to send more 20 register request block him/it for 3 hour
@ratelimit(key='user_or_ip', rate='20/h', block=False)
@blacklist_ratelimited(timedelta(minutes=180))
@csrf_exempt
def register(response):
    # Prevent loged in user to go on register page
    if response.user.is_authenticated:
        return redirect(reverse('msagh_website:base'))
    else:
        if response.method == "POST":
            form = RegisterForm(response.POST)
            if form.is_valid():

                user = form.save(commit=False)  # no save in database yet
                user_in_database = get_user_model().objects.create(username=user.username, password=user.password,
                                                                   email=user.email)
                user_in_database.is_active = False  # default set false
                send_email(user_in_database)  # send email with link to confirmation account

                return render(response, 'registration/success_register.html')
        else:
            form = RegisterForm()

        return render(response, 'members/register.html', {"form": form})


def logoutUser(request):
    logout(request)
    return render(request, 'members/logout.html')
