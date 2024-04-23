from rest_framework import serializers
from .models import *


class PrivateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["password", "username", "first_name", "last_name", "email"]
        
class PublicUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
  