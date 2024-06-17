from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializer import *
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from Authentication.models import notification
from Authentication.serializer import *

from django.http import JsonResponse

# Create your views here.\
    



    
    

def makeTicket(event, place):
    for each in range(place):
        Ticket.objects.create(event_id = event, status="available")

@api_view(['GET','POST'])
@renderer_classes([TemplateHTMLRenderer])
def scanTicket(request, event_id):
    if request.user.is_authenticated:
        data = {
                "username": request.user.username,
                "email":request.user.email,
                "name":request.user.last_name + request.user.first_name,
                "profil":User.objects.get(pk=request.user.id).profil.__str__(),
                "notification":notifiactionSerializer(notification.objects.filter(user=request.user.id).order_by("-timestamp"),many=True).data,
                "count_notification":(notification.objects.filter(user=request.user.id, is_read=False)).count(),
       

            }
        all_ticket_for_this_event = Ticket.objects.filter(event_id=event_id, status='not available')
        # ticket = Ticket.objects.get(pk= code_ticket)
        return Response({"ticket":TicketSerializer(all_ticket_for_this_event,many=True).data, "data": data}, template_name='scanner.html')
    else:
        return HttpResponseRedirect("/login/")

    
    


@api_view(['GET','POST'])
@renderer_classes([TemplateHTMLRenderer])
def createEvent(request):
    if request.user.is_authenticated:
        data = {
                    "username": request.user.username,
                    "email":request.user.email,
                    "name":request.user.last_name + request.user.first_name,
                    "profil":User.objects.get(pk=request.user.id).profil.__str__(),
                    "notification":notifiactionSerializer(notification.objects.filter(user=request.user.id).order_by("-timestamp"),many=True).data,
                    "count_notification":(notification.objects.filter(user=request.user.id, is_read=False)).count(),
       

                }
        try:
            if request.method == 'POST' and request.user.is_authenticated:
                print("files",request.FILES)
                data_ = request.POST.copy()
                data_['manager'] = request.user.id
                data_['flyers'] = request.FILES['flyers']
                print(data_)
                serializer=EventWriteSerializer(data=data_)
                print("kk")

                if serializer.is_valid():
                    
                    event = serializer.save()
                    event.manager = User.objects.get(pk=request.user.id)
                    makeTicket(event,event.place)
                    return Response({"response":"event created successfully", "data": data}, template_name='createE.html')
                    
                else:
                    print(serializer, serializer.errors)
                    print("ll")
                    return Response({"response":serializer.errors, "data": data}, template_name='createE.html')
            
            if request.method == "GET" and request.user.is_authenticated:
                return Response({"data": data},template_name='createE.html',)
        except Exception as e:
            print(e)
            print("kmk")
            return Response({"response":e.__str__(), "data": data}, template_name='createE.html')
    else:
        return HttpResponseRedirect("/login/")
        
     

     
     
@api_view(['GET','DELETE'])
def deleteEvent(request, event_id):
    if request.user.is_authenticated:
        print(request)
        if request.user.is_authenticated:
            print("yes")
            try:
                if Event.objects.get(pk=event_id) in Event.objects.filter(manager=request.user.id):
                    Event.objects.get(pk=event_id).delete()
                    return HttpResponseRedirect("/login/")
                else:
                    return HttpResponse("Event matching query does not exist", status = 403)
            except Event.DoesNotExist as e:
                return HttpResponse(e.__str__(), status=403)
    else:
        return HttpResponseRedirect("/login/")



