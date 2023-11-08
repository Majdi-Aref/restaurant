from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import MenuItem, Table
from .forms import NewUserForm, BookingForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required


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


class SignOutView(LogoutView):
    next_page = 'home'


@login_required
def book(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('home')
    else:
        form = BookingForm()
    tables = Table.objects.all()
    return render(request, 'book.html', {'form': form, 'tables': tables})
