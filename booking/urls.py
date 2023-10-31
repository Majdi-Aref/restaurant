from django.urls import path
from . import views  # make sure to import your views

urlpatterns = [
    path('', views.home, name='home'),  # new
]
