from django.contrib import admin
from .models import Table, Booking, MenuItem
from django_summernote.admin import SummernoteModelAdmin


@admin.register(MenuItem)
class MenuItemAdmin(SummernoteModelAdmin):

    list_display = ('name', 'price')
    summernote_fields = ('description',)


admin.site.register(Table)
admin.site.register(Booking)
