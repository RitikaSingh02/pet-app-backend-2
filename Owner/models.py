from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User

class UserInfo(models.Model):
    username = models.CharField(max_length=200, default="NULL" , unique= True )
    name = models.CharField(max_length=200, default="NULL")
    email = models.EmailField(max_length=200, default="NULL" , unique= True)
    password = models.CharField(max_length=200, default="NULL")

class ForumInfo(models.Model):
    forumname = models.CharField(max_length=200, default="Forum1" , unique= False)
    description = models.CharField(max_length=200 , default="NULL" , unique=False)    
    visibility = models.CharField(max_length=20 , default="PUBLIC" )

class UserForum(models.Model):
    forum = models.ForeignKey(ForumInfo, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)    

class UserConnections(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='user') 
    connection =models.ForeignKey(User, on_delete=models.CASCADE , related_name='connections') 