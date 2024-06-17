from django.http import  HttpResponseRedirect
from rest_framework import status
from .models import User
from .serializer import *
from rest_framework.decorators import api_view
from event.models import Event
from event.serializer import EventSerializer, EventSerializerprivate
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib import messages
import logging
from event.models import Ticket
from Authentication.models import notification, odpCode
import random
from django.core.mail import send_mail
from django.conf import settings

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
        # print(notification.objects.filter(user=request.user.id).order_by("-timestamp"))
        data = {
            "username": request.user.username,
            "email":request.user.email,
            "name":request.user.last_name + request.user.first_name,
            "total_event":len(Event.objects.filter(manager=request.user.id)),
            "total_revenus":data_calcul[1],
            "total_vente":data_calcul[0],
            "profil":User.objects.get(pk=request.user.id).profil.__str__(),
            "all_event": EventSerializerprivate(Event.objects.filter(manager=request.user.id),many=True).data,
            "notification":notifiactionSerializer(notification.objects.filter(user=request.user.id).order_by("-timestamp"),many=True).data,
            "count_notification":(notification.objects.filter(user=request.user.id, is_read=False)).count(),
        }
        # event_data = {"event": Event.objects.filter(manager=request.user.id)}
        # print(EventSerializerprivate(event_data,many=True))
        return Response({"data": data,},template_name='dashboard.html' ) 

    if request.method == 'POST':
        try:
            username = (request.data.get('username')).lower()
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
def singup(request):
    if request.method == 'POST':
        print(request.data)
        serializer = PrivateUserSerializer(data=request.data)
        try:
            if len(User.objects.filter(email=request.data['email'])) > 0:
                return Response({"message":"user with this email already exists"},template_name='signup.html')
            if serializer.is_valid():
                user = User.objects.create_user(
                username=(serializer.validated_data['username']).lower(),
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
        
        
        

        
@api_view(['GET','POST'])
@renderer_classes([TemplateHTMLRenderer])
def updateProfil(request):
    try:
        if request.user.is_authenticated:
            data = {
            "username": request.user.username,
            "email":request.user.email,
            "name":request.user.last_name + request.user.first_name,            
            "profil":User.objects.get(pk=request.user.id).profil.__str__(),
            "notification":notifiactionSerializer(notification.objects.filter(user=request.user.id).order_by("-timestamp"),many=True).data,
            "count_notification":(notification.objects.filter(user=request.user.id, is_read=False)).count(),
       
                }
           
            if request.method == "GET":
                return Response({"data":data, }, template_name='profil.html')
            
            elif request.method == "POST":
                user = User.objects.get(id=request.user.id)
                data_ = request.POST.copy()
                if 'profil' in request.FILES:
                    data_['profil'] = request.FILES['profil']
                    user.profil = request.FILES['profil']
                    user.save()
                     
                print(data_)
                if len(User.objects.filter(email=request.data['email'])) >0 and request.data['email'] != user.email:
                    return Response({"message":"user with this email already exists","data":data},template_name='profil.html')
                serializer =  UpdateUserSerializer(user, data= data_ ,partial=True)
                if serializer.is_valid():
                    if 'password' in data_ and len(data_['password']) > 0:
                        user.set_password(data_['password'])
                        user.save()
                        
                    serializer.save()   
                    return HttpResponseRedirect("/login/")                    
                    
            
            return Response({"data":data, }, template_name='profil.html')
   
        else:
            return Response("Not authenticated", status=404)
    except Exception as e:
        # print("error: ",e)
        return HttpResponseRedirect("/")
    # if request.method == 'POST':
        
  

@api_view(['GET','POST'])
@renderer_classes([TemplateHTMLRenderer])
def readnotification(request, id):
    if request.user.is_authenticated:
        data = {
            "username": request.user.username,
            "email":request.user.email,
            "name":request.user.last_name + request.user.first_name,            
            "profil":User.objects.get(pk=request.user.id).profil.__str__(),
            "notification":notifiactionSerializer(notification.objects.filter(user=request.user.id).order_by("-timestamp"),many=True).data,
            "count_notification":(notification.objects.filter(user=request.user.id, is_read=False)).count(),
       
                }
        notif = notification.objects.get(pk=id)
        notif.is_read = True
        notif.save()
        return HttpResponseRedirect("/login/")
    else:
        return HttpResponseRedirect("/login/") 



@api_view(['GET','POST'])
@renderer_classes([TemplateHTMLRenderer])    
def recoverypassword(request):
    if request.method == "GET":
        return Response(template_name='forgetPassword.html')
    else:
        if 'email' in request.data:
            try:
                odpCode.objects.filter(user=User.objects.get(email=request.data['email'])).delete()
                user_ = User.objects.get(email=request.data['email'])
                odpCode.objects.create(user=user_, code=user_.id+random.randint(2649,999999))
                

                send_mail('Astrakahn Event Recovery Password', 'Your code for recovery your password is: ' + str(odpCode.objects.get(user=user_).code), settings.EMAIL_HOST_USER, [request.data['email']])
                return Response({"email":request.data['email'], }, template_name='forgetPassword.html')
            
            except User.DoesNotExist:
                return Response({"message":"user email matching dont found", }, template_name='forgetPassword.html')
        else:
            try:
                code = request.data['code']
                # print(code)
                print(odpCode.objects.get(user=User.objects.get(email=request.data['email_'])).code)
                if odpCode.objects.get(user=User.objects.get(email=request.data['email_'])).code == code:
                    # print("reset password")
                    return HttpResponseRedirect("/newpassword/"+str(code))
                else:
                    # print("code correct")
                    return Response({"email":request.data['email_'],"message":"code incorect" }, template_name='forgetPassword.html')
            except Exception as e:
                return HttpResponseRedirect("/recoverypassword/")

@api_view(['GET','POST'])
@renderer_classes([TemplateHTMLRenderer])         
def newpassword(request, code):
    odpcode = code
    user = odpCode.objects.get(code=odpcode).user
    email = odpCode.objects.get(code=odpcode).user.email
    if request.method == 'GET':
        return Response({"email":email, "code":code},template_name='changepassword.html')
    else:
        user = odpCode.objects.get(code=odpcode).user
        print("code change")
        print("new password", request.data['password'])
        user.set_password(request.data['password'])
        user.save()
        odpCode.objects.get(code=odpcode).delete()
        return HttpResponseRedirect("/login/")