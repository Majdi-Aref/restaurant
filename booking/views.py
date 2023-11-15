from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import MenuItem, Table, Booking
from .forms import NewUserForm, BookingForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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


class SignOutView(LogoutView):
    next_page = 'home'


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
def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if booking.user == request.user:
        booking.delete()
        messages.success(
            request, 'You have successfully cancelled the selected booking.')
    return redirect('my_bookings')
