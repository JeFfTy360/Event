from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path("login/",views.login),
    path("signup/", views.createAccount),
    path("logout/", views.log_out),
    path("myprofil/", views.viewPrivateProfil),
]
