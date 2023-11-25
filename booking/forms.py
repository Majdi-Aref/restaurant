from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking
from django.core.exceptions import ValidationError


class NewUserForm(UserCreationForm):
    """
    Class for creating a new user form.
    It inherits from Django's built-in UserCreationForm.
    It includes an email field.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        """
        Validation of the email field.
        Ensures a user cannot register with an email that is already registered.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "The email you just entered is already registered, please enter another email.")
        return email

    def save(self, commit=True):
        """
        Overrides the save method to include the email field.
        """
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ChoiceTimeField(forms.TimeField):
    """
    Provides pre-defined times for booking to choose from.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.widget = forms.Select(
            choices=[('%02d:00' % i, '%02d:00' % i) for i in [10, 12, 14, 16, 18]])


class BookingForm(forms.ModelForm):
    """
    Form for creating a new booking.
    """
    time = ChoiceTimeField()

    class Meta:
        model = Booking
        fields = ['table', 'date', 'time', 'guests']

    def clean(self):
        """
        Custom validation for the form.
        Ensures a user enters a valid number of guests.
        Prevents double bookings.
        """
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        guests = cleaned_data.get('guests')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if table and guests:
            if guests <= 0 or guests > table.capacity:
                raise ValidationError(
                    'You have entered an invalid number of guests; please enter a number of guests that is not zero, equal to, or less than the capacity of the table that you want to book!')

        if table and date and time:
            if Booking.objects.filter(table=table, date=date, time=time).exists():
                raise ValidationError(
                    'The table you want to book for the date and time you have chosen has already been booked by another customer; please choose another table, date, or time for your booking!')

        return cleaned_data
