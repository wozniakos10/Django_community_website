from django.shortcuts import render

# Create your views here.

def base(request):
    return render(request, 'base.html')

def spotted(request):
    return render(request, 'msagh_website/spotted.html')

