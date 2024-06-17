from django.db import models
from django.contrib.auth.models import User as MainUser
import time
import os


# Create your models here.
def get_time():
    timestamp = time.time()
    current_date = time.ctime(timestamp)
    return current_date
    
    
def user_directory_path(instance, filename):
    # Get the username from the related User model
    # print(filename[-3:])
    extension = "."+filename[-3:]
    username = instance.user.username
    filename = get_time()+extension
    # Construct the subfolder path
    return os.path.join('data', username, 'profil', filename)

class User(MainUser, models.Model):
    profil = models.ImageField(upload_to=user_directory_path, null=True)
    
    
    def __str__(self):
        return self.username
    
    
class notification(models.Model):
    is_read = models.BooleanField(default=False)
    description = models.CharField(max_length=255,blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class odpCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False,)
    code = models.CharField(max_length=100, blank=True)
    timestamp = models.TimeField(auto_now_add=True)