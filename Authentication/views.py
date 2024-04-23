from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import status
from .models import User
from .serializer import *
from rest_framework.decorators import api_view
from main.models import Event
from main.serializer import EventSerializer
from django.contrib.auth import authenticate
# Create your views here.


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.data['username'], password=request.data['password'])
        try:
            status = user.is_authenticated
            return HttpResponse(user)
        except Exception as e:
            return HttpResponse("Invalid username or password")
        

@api_view(['POST'])
def createAccount(request):
    if request.method == 'POST':
        print(request.data)
        serializer = PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
            )
            print(user)
            return JsonResponse({"message":"account created successfully"})
        else:
            error = serializer.errors
            return JsonResponse({"message":"Data validation failed", "error": error})


