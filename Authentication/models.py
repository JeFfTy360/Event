from django.db import models
from django.contrib.auth.models import User as MainUser
import time

# Create your models here.


class User(MainUser, models.Model):
    profil = models.ImageField(null=True, )
    
    def __str__(self):
        return self.username
    
    
    