from rest_framework import serializers
from .models import *


def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')

class PrivateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[required])
    username = serializers.CharField(validators=[required])
    last_name = serializers.CharField(validators=[required])
    first_name = serializers.CharField(validators=[required])
    email = serializers.EmailField(validators=[required])
    class Meta:
        model = User
        fields = ["password", "username", "first_name", "last_name", "email"]
        
class PublicUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
  