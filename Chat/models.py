from django.db import models
from django.contrib.auth.models import User
from Owner.models import ForumInfo

class Message(models.Model):
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateField(auto_now_add=True, blank=True , null=True)

class ForumMessage(models.Model):
    author = models.ForeignKey(User, related_name='forummessages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateField(auto_now_add=True, blank=True , null=True)
    forum = models.ForeignKey(ForumInfo, related_name='messages', on_delete=models.CASCADE)
# Create your models here.
