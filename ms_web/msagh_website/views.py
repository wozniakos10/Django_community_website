from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .forms import SpotForm, MemeForm, CommentSpotForm,CommentMemeForm
from .models import Spot, Meme, CommentSpot,CommentMeme
from django.core.paginator import Paginator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages  # import messages
from ms_web.settings import EMAIL_FROM_ADDRESS


# Create your views here.

def base(request):
    posts_list = Spot.objects.all().filter(admin_aproved=True).order_by('-pub_date')[:3]
    first_post = posts_list[0]
    second_post = posts_list[1]
    third_post = posts_list[2]

    return render(request, 'base.html', {'first_post': first_post,
                                         'second_post': second_post,
                                         'third_post': third_post, })


def spotted(request):
    # look only for approved posts and order them by publication date
    posts_list = Spot.objects.all().filter(admin_aproved=True).order_by('-pub_date')

    # Set up Paginator
    p = Paginator(posts_list, 4)
    page = request.GET.get('page')
    posts = p.get_page(page)

    # list of numbers of comments for every spot:
    numbers = []
    for post in posts:
        comments = CommentSpot.objects.all().filter(spot=post)
        numbers.append(len(comments))
    # number of last page to show ( ... ) in html of spotted in paginator
    last_page = p.get_page(-1).number

    numbers_posts = zip(numbers, posts)  # zip to iterate into django template
    return render(request, 'msagh_website/spotted.html', {'posts': posts,
                                                          "numbers_posts": numbers_posts,
                                                          "last_page": last_page})


@login_required(login_url='/login')
def new_spot(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SpotForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            form = SpotForm()
            return render(request, 'msagh_website/success_post_spot.html')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = SpotForm()
    return render(request, 'msagh_website/new_spot.html', context={'form': form})


def memes(request):
    # look only for approved posts and order them by publication date
    memes_list = Meme.objects.all().filter(admin_aproved=True).order_by('-pub_date')

    # Set up Paginator
    p = Paginator(memes_list, 5)
    page = request.GET.get('page')
    memes = p.get_page(page)

    # list of numbers of comments for every spot:
    numbers = []
    for meme in memes:
        comments = CommentMeme.objects.all().filter(memes=meme)
        numbers.append(len(comments))
    # number of last page to show ( ... ) in html of spotted in paginator
    last_page = p.get_page(-1).number
    numbers_memes = zip(numbers, memes)  # zip to iterate into django template
    return render(request, 'msagh_website/memes.html', {'memes': memes,
                                                        "last_page": last_page,
                                                        "numbers_memes": numbers_memes
                                                        })


@login_required(login_url='/login')
def new_meme(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MemeForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            return render(request, 'msagh_website/success_post_spot.html')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = MemeForm()
    return render(request, 'msagh_website/new_meme.html', context={'form': form})


def contact(request):
    return render(request, 'msagh_website/contact.html')


def password_reset_request(request):
    if request.user.is_authenticated:
        return redirect(reverse('msagh_website:base'))  # Prevent logged user to reset password by type in browser

    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']  # Getting email from form
            associated_users = User.objects.filter(
                Q(email=data, is_active=True))  # Checking if user with that email exists
            if associated_users.exists():
                try:
                    # Trying send email with link to reset password by built function
                    password_reset_form.save(domain_override='127.0.0.1:8000',
                                             subject_template_name='password/password_reset_email.txt',
                                             html_email_template_name='password/password_reset_body.html',
                                             from_email=EMAIL_FROM_ADDRESS)
                    return render(request, 'msagh_website/success_reset_password_sent.html')
                except:
                    # Warning if something went wrong
                    messages.warning(request, 'Coś poszło nie tak... spróbuj jeszcze raz.')

            else:
                # Warning if user with that email do not exist
                messages.warning(request,
                                 "Nie znaleźliśmy żadnego konta powiązanego z tym adresem Email, sprawdź swoje dane i spróbuj jeszcze raz."
                                 " Jeśli jeszcze tego nie zrobiłeś, potwierdź swoje konto.")

    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def one_spot(request, pk):
    try:
        single_spot = Spot.objects.all().filter(admin_aproved=True).order_by('pub_date').get(pk=pk)
    except Spot.DoesNotExist:
        return redirect(reverse('msagh_website:spotted'))

    if request.method == 'POST':
        if request.user.is_authenticated:
            # create a form instance and populate it with data from the request:
            form = CommentSpotForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.spot = single_spot
                obj.save()
                return redirect(reverse('msagh_website:one_spot', args=(pk,)))
        else:
            messages.warning(request, 'Musisz się zalogować aby dodać komentarz!')
            return redirect(reverse('msagh_website:one_spot', args=(pk,)))
    else:

        form = CommentSpotForm()

    comments = CommentSpot.objects.all().filter(spot=single_spot)
    no_comments = len(comments)
    ctx = {
        'single_spot': single_spot,
        'form': form,
        'comments': comments,
        "no_comments": no_comments,
    }

    return render(request, 'msagh_website/one_spot.html', context=ctx)  # Write a new template to view your news.

def one_meme(request, pk):
    try:
        single_meme = Meme.objects.all().filter(admin_aproved=True).order_by('pub_date').get(pk=pk)
    except Meme.DoesNotExist:
        return redirect(reverse('msagh_website:memes'))

    if request.method == 'POST':
        if request.user.is_authenticated:
            # create a form instance and populate it with data from the request:
            form = CommentMemeForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.spot = single_meme
                obj.save()
                return redirect(reverse('msagh_website:one_meme', args=(pk,)))
        else:
            messages.warning(request, 'Musisz się zalogować aby dodać komentarz!')
            return redirect(reverse('msagh_website:one_meme', args=(pk,)))
    else:

        form = CommentMemeForm()

    comments = CommentMeme.objects.all().filter(memes=single_meme)
    ctx = {
        'single_meme': single_meme,
        'form': form,
        'comments': comments
    }

    return render(request, 'msagh_website/one_meme.html',ctx)  # Write a new template to view your news.
