from .models import MenuItem
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})


def register(request):
    return render(request, 'register.html')


def signin(request):
    return render(request, 'signin.html')


def book(request):
    return render(request, 'book.html')
