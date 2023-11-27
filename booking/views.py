from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Table, Booking
from .forms import NewUserForm, BookingForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    """
    View function for the home page of the restaurant.
    """
    return render(request, 'home.html')


def menu(request):
    """
    View function for the restaurant menu.
    """
    menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})


def register(request):
    """
    View function for the restaurant registration page.
    A message will confirm a successful registration.
    """
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
    """
    Class-based view for the restaurant sign-in page.
    A message will confirm a successful sign-in.
    """
    template_name = 'signin.html'
    success_url = 'book'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 'You have successfully signed in; you can now book a table! If you have already booked a table, please first check "My Bookings".')
        return response


def signout(request):
    """
    View function for sign-out on the navigation bar.
    A message will confirm a successful sign-out.
    """
    logout(request)
    messages.success(request, 'You have successfully signed out!')
    return redirect('home')


@login_required
def my_bookings(request):
    """
    View function for displaying a customer's bookings.
    """
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})


@login_required
def book(request):
    """
    View function for the restaurant booking page.
    A message will confirm a successful booking.
    """
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
def update_booking(request, booking_id):
    """
    View function for updating a booking.
    A message will confirm a successful update.
    """
    booking = get_object_or_404(Booking, id=booking_id)
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
        form = BookingForm(instance=booking)
    tables = Table.objects.all()
    return render(request, 'update_booking.html', {'form': form, 'tables': tables})


@login_required
def cancel_booking(request, booking_id):
    """
    View function for cancelling a booking.
    A message will confirm a successful cancellation.
    """
    booking = Booking.objects.get(id=booking_id)
    if booking.user == request.user:
        booking.delete()
        messages.success(
            request, 'You have successfully cancelled the selected booking.')
    return redirect('my_bookings')
