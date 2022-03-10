from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .forms import SpotForm
# Create your views here.

def base(request):
    return render(request, 'base.html')

def spotted(request):
    return render(request, 'msagh_website/spotted.html')

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