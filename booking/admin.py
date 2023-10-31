from django.contrib import admin
from .models import Table, Booking, MenuItem
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(Table)
admin.site.register(Booking)
admin.site.register(MenuItem)