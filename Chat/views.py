from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.shortcuts import render
from .models import Message
from django.db.models import Q

def chat(request , username):
    receiver_id = User.objects.get(username = username).id
    params = {
        "receiver" : username , 
        "sender" : request.user ,
        }
    msg_query = list(Message.objects.filter(Q(author_id = request.user.id , receiver_id = receiver_id) | Q(receiver_id = request.user.id , author_id = receiver_id)).values('message'))
    msgs = []
    for msg in msg_query:
        msgs.append(msg['message'])
    params["msgs"] = msgs
    return render(request , "chat.html" , params )
# Create your views here.
