from .views import register, SignInView, book, update_booking
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('register/', views.register, name='register'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', views.signout, name='signout'),
    path('book/', views.book, name='book'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('update_booking/<int:booking_id>/',
         views.update_booking, name='update_booking'),
    path('cancel_booking/<int:booking_id>/',
         views.cancel_booking, name='cancel_booking'),
]
