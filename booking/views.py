from .models import MenuItem
from django.shortcuts import render


def home(request):
    return render(request, 'base.html')


def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})
