from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
class EventSerializer(serializers.ModelSerializer):
    manager = serializers.CharField(source="manager.username")

    class Meta:
        model = Event
        fields = ["name","description","date","line_up","place","manager"]
    
    
        
        
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"