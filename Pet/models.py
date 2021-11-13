from django.db import models
from django.contrib.auth.models import User

class PetInfo(models.Model):
    pet_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, default="NULL")
    gender = models.CharField(max_length=200, default="NULL")
    description = models.CharField(max_length=200, default="NULL")
    category = models.CharField(max_length=200, default="NULL")
    breed = models.CharField(max_length=200, default="NULL")
    profile_pet = models.URLField(null=True)
    identifier = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Category(models.Model):
    category = models.CharField(max_length=200, default="NULL")

class Breed(models.Model):
    breed = models.CharField(max_length=200, default="NULL" )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
# Create your models here.
