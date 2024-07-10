from django.shortcuts import render


# Create your views here.

def home(request):
    return render(request, 'Sign_in.html')

def register(request):
    return render(request, 'Sign_in.html')