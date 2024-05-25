from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path("event/create/",views.createEvent),
    # path("event/create/form/",views.createEventform),
    path("event/delete/<int:event_id>", views.deleteEvent),
    path("event/verify/<int:event_id>/<int:code_ticket>", views.scanTicket)
    # path("test/", views.profile_list),
    
]
