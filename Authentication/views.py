from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework import status
from .models import User
from .serializer import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from event.models import Event
from event.serializer import EventSerializer, EventSerializerprivate
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib import messages
import logging
from event.models import Ticket
# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login as auth_login

def total_revenus(user_id):
    Event_of_user = Event.objects.filter(manager = user_id)
    Total_vente=0
    revenu_total = 0
    for each in Event_of_user:

        Total_vente = Total_vente+len([each for each in Ticket.objects.filter(status="not available", event_id=each.id) ])
        revenu_total = revenu_total + each.revenus
        
    return [Total_vente,revenu_total]
    
        

@api_view(['GET','POST'])
@renderer_classes([TemplateHTMLRenderer])
def login(request):
    if request.user.is_authenticated:
        print(request.user)
        data_calcul = total_revenus(request.user.id)
        data = {
            "username": request.user.username,
            "email":request.user.email,
            "name":request.user.last_name + request.user.first_name,
            "total_event":len(Event.objects.filter(manager=request.user.id)),
            "total_revenus":data_calcul[1],
            "total_vente":data_calcul[0],
            "profil":User.objects.get(pk=request.user.id).profil.__str__(),
            "all_event": EventSerializerprivate(Event.objects.filter(manager=request.user.id),many=True).data
        }
        # event_data = {"event": Event.objects.filter(manager=request.user.id)}
        # print(EventSerializerprivate(event_data,many=True))
        return Response({"data": data,},template_name='dashboard.html' ) 

    if request.method == 'POST':
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                auth_login(request, user)  # Enregistre l'utilisateur dans la session
                return HttpResponseRedirect("/login/") 
            else:
                return Response({"message": "username or password is incorect",},template_name='login.html' )
        except Exception as e:
            print(e)
            return Response({"message": "username or password is incorect",},template_name='login.html' )
    else:
        return Response(template_name='login.html')            


@api_view(['GET','POST'])
@renderer_classes([TemplateHTMLRenderer])
def createAccount(request):
    if request.method == 'POST':
        print(request.data)
        serializer = PrivateUserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
            )
                print(user)
                return Response({"message":"account created successfully"},template_name='signup.html')
            else:
                error = serializer.errors
                return Response({"message":error},template_name='signup.html')
        except Exception as e:
            # logging.basicConfig(filename="logfilename.log", level=logging.ERROR)
            # logging.error(e)
            return Response({"message":e},template_name='signup.html')
    else:
        return Response({"a":34},template_name='signup.html')


@api_view(['GET','POST'])
def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return Response("no user logged in`")
        
        
        

        
@api_view(['GET'])
def viewPrivateProfil(request):
    try:
        if request.user.is_authenticated:
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            userseriliser = PublicUserSerializer(user, many=False)
            userdata=userseriliser.data
            event = Event.objects.filter(manager=user_id)
            eventserialiser = EventSerializerprivate(event, many=True)
            eventdata = eventserialiser.data
            print(userdata)
        
            return Response({"userdata":userdata, "ticket_sold":2,"eventdata":eventdata}, template_name='dashboard.html')
        else:
            return Response("Not authenticated", status=404)
    except Exception as e:
        return HttpResponseRedirect("/")
  
  
