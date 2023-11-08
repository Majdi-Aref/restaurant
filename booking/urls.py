from django.urls import path
from . import views
from .views import SignInView


urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('register/', views.register, name='register'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('book/', views.book, name='book'),
]
