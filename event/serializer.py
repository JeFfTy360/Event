from rest_framework import serializers
from .models import *


class EventSerializer(serializers.ModelSerializer):
    manager = serializers.CharField(source="manager.username")

    class Meta:
        model = Event
        fields = ["id","name","description","adress","price","date","line_up","place","manager", "flyers"]
    


class EventWriteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = ["name","description","date","time","line_up","adress","price","place","manager", "flyers"]
            
    # def create(self, validated_data):
    #     manager_id = validated_data.pop('manager')
    #     validated_data['manager'] = User.objects.get(id=manager_id).id
    #     return super().create(validated_data)
    
    
class EventSerializerprivate(serializers.ModelSerializer):
    

    class Meta:
        model = Event
        fields = ["id","name","description","date","line_up","place","flyers","revenus", "sold_place"]

    
        
        
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"