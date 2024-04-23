from django.db import models
from datetime import date
import time
from Authentication.models import User

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField(auto_now_add=False)
    line_up = models.TextField(blank=False)
    place = models.IntegerField(blank=False)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def maketicket(self):
        for i in range(self.place):
            event_instance = Event.objects.get(pk=self.id)
            ticket = Ticket.objects.create(event_id=event_instance)
        
    
class Ticket(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    owner = models.CharField(null=True, max_length=20, blank=True)
    def __str__(self):
        return str(str(self.id)+" for "+str(self.event_id))
    

