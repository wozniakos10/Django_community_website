from django.shortcuts import render

def handle_not_found(request,exception):
    return render(request,'errors/not_found_error.html',status=404)