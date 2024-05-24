from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializer import *
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
# Create your views here.\
    



    
    

def makeTicket(event, place):
    for each in range(place):
        Ticket.objects.create(event_id = event, status="available")



@api_view(['POST'])
def createEvent(request):
    try:
        if request.method == 'POST' and request.user.is_authenticated:
            print(request.user.id)
            request.data['manager'] = request.user.id
            print(request.data)
            serializer=EventSerializerprivate(data=request.data)
            if serializer.is_valid():
                event = serializer.save()
                makeTicket(event,event.place)
                return HttpResponse("event created successfully")
            else:
                print(serializer, serializer.errors)
                return HttpResponse("echec operation failed")
        else:
            return HttpResponseRedirect(redirect_to='/')
    except Exception as e:
        return HttpResponseRedirect(redirect_to='/login/')
        
     

     
     
@api_view(['GET','DELETE'])
def deleteEvent(request, event_id):
    print(request)
    if request.user.is_authenticated:
        print("yes")
        try:
            if Event.objects.get(pk=event_id) in Event.objects.filter(manager=request.user.id):
                Event.objects.get(pk=event_id).delete()
                return HttpResponse("event has been deleted", status=200)
            else:
                return HttpResponse("Event matching query does not exist", status = 403)
        except Event.DoesNotExist as e:
            return HttpResponse(e.__str__(), status=403)



# @renderer_classes([TemplateHTMLRenderer])
# def createEventform(request):
#     return Response(template_name='index.html')


# @api_view(['GET'])
# def createEventform(request):
#     return HttpResponse({'event':  "serializer.data"})
#     # return JsonResponse(serializer.data, safe=False)