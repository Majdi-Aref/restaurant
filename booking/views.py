from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import MenuItem
from .forms import NewUserForm
from django.contrib.auth.views import LoginView


def home(request):
    return render(request, 'home.html')


def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})


def register(request):
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    return render(request, 'register.html', {'form': form})


class SignInView(LoginView):
    template_name = 'signin.html'
    success_url = 'book'


def book(request):
    return render(request, 'book.html')
