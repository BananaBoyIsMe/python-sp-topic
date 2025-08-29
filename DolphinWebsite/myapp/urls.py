from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name="home-page"),
    path('home2', home2),
    path('about/', aboutUs, name="about-page"),
]