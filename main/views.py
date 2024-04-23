from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Event, User, Ticket
from .serializer import *
from rest_framework import status
from rest_framework.decorators import api_view
import Authentication.serializer

# Create your views here.

@api_view(['GET',])
def index(request):
    
    list_event = Event.objects.all()
    print(list_event)
    serializer = EventSerializer(list_event, many=True,)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def showUserProfil(request, username):
    user = User.objects.get(username=username)
    serializer_user = Authentication.serializer.PublicUserSerializer(user)
    try:
        event_of_user = Event.objects.filter(manager=User.objects.get(username=username).id)
        serialize_event =EventSerializer(event_of_user, many=True)
    except Event.DoesNotExist:
        return JsonResponse("error")
    
    data = {
        "user": serializer_user.data,
        "event": serialize_event.data
    }
    return JsonResponse(data, safe=True)

