from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path("",views.index),
    path("profil/<str:username>", views.showUserProfil),
    path("buyticket/<int:eventId>", views.buyTicket),
    path("find/", views.findEvent)
]
