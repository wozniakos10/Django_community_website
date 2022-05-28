from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, UpdateProfileForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
from django_email_verification import send_email

from django.views.decorators.csrf import csrf_exempt

from datetime import timedelta
from ratelimit.decorators import ratelimit
from blacklist.ratelimit import blacklist_ratelimited
from .models import Profile
from msagh_website.models import Spot, CommentSpot
from .utils import compute_user_points
from django.contrib.auth.models import User
from django.contrib import messages  # import messages


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


@login_required(login_url='/login')
def profile(request, pk):
    user_profile = User.objects.get(pk=pk)

    no_comments = len(CommentSpot.objects.all().filter(user=user_profile))
    no_spots = len(Spot.objects.all().filter(user=user_profile, admin_aproved=True))
    points = compute_user_points(no_comments, no_spots, user_profile.date_joined)

    context = {
        'user_profile': user_profile,
        'points': points,
        'no_comments': no_comments,
        'no_spots': no_spots,

    }

    return render(request, 'members/profile.html', context)


# View to edit profile
@login_required(login_url='/login')
def edit_profile(request):
    if request.method == 'POST':
        # Getting form
        profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Twój profil został zaaktualizowany!')
            return redirect(reverse('members:profile', args=(request.user.pk,)))


    else:
        profile_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        'profile_form': profile_form
    }
    return render(request, 'members/edit_profile.html', context)
