from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

def base(request):
    return render(request, 'base.html')

def spotted(request):
    return render(request, 'msagh_website/spotted.html')

@login_required(login_url='/login')
def new_spot(request):
    return render(request, 'msagh_website/new_spot.html')