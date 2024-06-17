from django.db import models
from datetime import date
import time
import os
from Authentication.models import User


def get_time():
    timestamp = time.time()
    current_date = time.ctime(timestamp)
    return current_date

def user_directory_path(instance, filename):
    # Get the username from the related User model
    # print(filename[-3:])
    extension = "."+filename[-3:]
    username = instance.manager.username
    print(username)
    eventname = instance.name
    filename = get_time()+extension
    # Construct the subfolder path
    return os.path.join('data', username, 'event',eventname, filename)


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField(auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    line_up = models.TextField(blank=False)
    price = models.FloatField(blank=True, default=0)
    place = models.IntegerField(blank=False)
    sold_place = models.IntegerField(blank=False, default=0)
    # remaining_place = models.IntegerField(blank=True, default=0)
    manager = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    flyers = models.ImageField(upload_to=user_directory_path, blank=True)
    revenus = models.FloatField(blank=False, default=0)
    adress = models.TextField(null=True, max_length=255)
  
    
    def __str__(self):
        return self.name + str(self.id)
    
    
        
    
class Ticket(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(default="available", max_length=50)
    owner = models.CharField(null=False, max_length=20, default="")
    def __str__(self):
        return str(str(self.id)+" for "+str(self.event_id))
    
