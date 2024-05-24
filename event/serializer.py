from rest_framework import serializers
from .models import *


class EventSerializer(serializers.ModelSerializer):
    manager = serializers.CharField(source="manager.username")

    class Meta:
        model = Event
        fields = ["id","name","description","date","line_up","place","manager", "flyers"]
    

class EventSerializerprivate(serializers.ModelSerializer):
    

    class Meta:
        model = Event
        fields = ["id","name","description","date","line_up","place","flyers","revenus", "sold_place"]

    
        
        
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"