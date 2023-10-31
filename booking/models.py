from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Table(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        return f"Table {self.number}"


class Booking(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings')
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"Booking by {self.user.username} on {self.date} at {self.time} for {self.guests} guests at {self.table}"


class MenuItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = CloudinaryField('image', default='placeholder')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
