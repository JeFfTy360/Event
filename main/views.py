from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from event.models import Event, Ticket
from event.serializer import *
from rest_framework import status
from rest_framework.decorators import api_view
import Authentication.serializer

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def index(request):
    print(request.user)
    list_event = Event.objects.all()
    serializer = EventSerializer(list_event, many=True,)
    print(serializer.data)
    return Response({'event':  serializer.data }, template_name='index.html')
    # return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def showUserProfil(request, username):
    try:
        user = User.objects.get(username=username)
        serializer_user = Authentication.serializer.PublicUserSerializer(user)
    
    
        event_of_user = Event.objects.filter(manager=User.objects.get(username=username).id)
        serialize_event =EventSerializer(event_of_user, many=True)
        data = {
        "user": serializer_user.data,
        "event": serialize_event.data
        }
        print(data)
        return Response(data, template_name='public_profil.html')
    except Exception as error:
        return Response(error, status=status.HTTP_204_NO_CONTENT)
    
    
import random
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def buyTicket(request, eventId):
    try:
        event = Event.objects.get(pk=eventId)
    except Event.DoesNotExist:
        return HttpResponse("error the event dont exist")
    if(event.place > 0):
        try:
            ticket = random.choice((Ticket.objects.filter(status="available", event_id=eventId)))
            serializer = TicketSerializer(ticket, many=False)
            print(len(serializer.data))
            print(serializer.data)
            ticket.status = "not available"
            ticket.save()
            event.place = event.place - 1
            event.sold_place = event.sold_place+1
            event.revenus = event.revenus + event.price
            event.save()
        
            return Response({"ticket_code":ticket.id}, template_name='ticket_generator.html')
        except Exception as e:
            return HttpResponse("ticket dont available")
            
       
    else:
        return HttpResponse("place is not available")
    
   
        