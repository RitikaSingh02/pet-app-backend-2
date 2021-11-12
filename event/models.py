from django.db import models
from Owner.models import UserInfo
from django.utils import timezone

class EventTypes(models.Model):
    type_name = models.CharField(max_length=200 , default="NULL" , unique=True)  
    type_decription = models.CharField(max_length=200 , default="NULL" , unique=False) 

class Events(models.Model):
    event_type =  models.ForeignKey(EventTypes, on_delete=models.CASCADE)
    date_of_creation = models.DateField(auto_now=False, auto_now_add=False , default= timezone.now)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    event_description = models.CharField(max_length=200 , default="NULL" , unique=False) 




# Create your models here.
