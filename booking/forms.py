from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking
from django.core.exceptions import ValidationError


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ChoiceTimeField(forms.TimeField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.widget = forms.Select(
            choices=[('%02d:00' % i, '%02d:00' % i) for i in [10, 12, 14, 16, 18]])


class BookingForm(forms.ModelForm):
    time = ChoiceTimeField()

    class Meta:
        model = Booking
        fields = ['table', 'date', 'time', 'guests']

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        guests = cleaned_data.get('guests')

        if table and guests:
            if guests <= 0 or guests > table.capacity:
                raise ValidationError(
                    'You have entered an invalid number of guests; please enter a number of guests that is not zero, equal to, or less than the capacity of the table that you want to book!')

        return cleaned_data
