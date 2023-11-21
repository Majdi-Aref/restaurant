from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Table, Booking
from .forms import NewUserForm, BookingForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction


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
            messages.success(
                request, 'You have successfully registered, please sign in to be able to book a table.')
            return redirect('signin')
    return render(request, 'register.html', {'form': form})


class SignInView(LoginView):
    template_name = 'signin.html'
    success_url = 'book'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 'You have successfully signed in; you can now book a table! If you have already booked a table, please first check "My Bookings".')
        return response


def signout(request):
    logout(request)
    messages.success(request, 'You have successfully signed out!')
    return redirect('home')


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})


@login_required
def book(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'You have successfully booked a table!')
            return redirect('my_bookings')
    else:
        form = BookingForm()
    tables = Table.objects.all()
    return render(request, 'book.html', {'form': form, 'tables': tables})


@login_required
@transaction.atomic
def update_booking(request, booking_id):
    booking = Booking.objects.select_for_update().get(id=booking_id)
    if booking.user != request.user:
        return redirect('my_bookings')
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(
                request, 'You have successfully updated this booking!')
            return redirect('my_bookings')
        else:
            messages.error(
                request, 'The details you have just chosen are not available, please choose other booking details to be able to update this booking.')
    else:
        form = BookingForm(instance=booking)
    tables = Table.objects.all()
    return render(request, 'update_booking.html', {'form': form, 'tables': tables})


@login_required
def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if booking.user == request.user:
        booking.delete()
        messages.success(
            request, 'You have successfully cancelled the selected booking.')
    return redirect('my_bookings')
