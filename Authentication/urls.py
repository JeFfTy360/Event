from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path("login/",views.login),
    path("signup/", views.singup),
    path("logout/", views.log_out),
    path("profil/", views.updateProfil),
    path("readnotification/<int:id>", views.readnotification),
    path("recoverypassword/", views.recoverypassword),
    path("newpassword/<int:code>", views.newpassword),
]
