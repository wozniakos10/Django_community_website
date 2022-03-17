from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .forms import SpotForm
from .models import Spot
from django.core.paginator import Paginator
# Create your views here.

def base(request):
    return render(request, 'base.html')

def spotted(request):
    # look only for approved posts and order them by publication date
    posts_list = Spot.objects.all().filter(admin_aproved=True).order_by('-pub_date')


    #Set up Paginator
    p = Paginator(posts_list,4)
    page = request.GET.get('page')
    posts = p.get_page(page)
    # number of last page to show ( ... ) in html of spotted in paginator
    last_page = p.get_page(-1).number

    return render(request, 'msagh_website/spotted.html',{'posts': posts,
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
            return redirect(reverse('msagh_website:spotted'))

        # if a GET (or any other method) we'll create a blank form
    else:
        form = SpotForm()
    return render(request, 'msagh_website/new_spot.html', context={'form':form})