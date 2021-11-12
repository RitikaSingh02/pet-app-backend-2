from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.http.response import JsonResponse
from django.shortcuts import render

from .models import Message,ForumMessage
from Owner.models import UserForum

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
        msgs.append({ "message": msg['message'] , "receiver" : str(username) ,  "sender" : str(request.user) })
        # msgs.append(["message: " +  msg['message'] , "receiver :" + str(username) ,  "sender : "+ str(request.user) ]) #for template

    params["msgs"] = msgs
    # return render(request , "chat.html" , params )
    return JsonResponse(params["msgs"] , safe = False , status = 200)

def forum(request , forumid):
    #custom check for the user existing in the forum
    query = UserForum.objects.filter(forum_id = forumid , user_id = request.user.id).exists()
    if not query:
        res = {}        
        res['msg'] = "You are unauthorized to access this forum"
        return JsonResponse(res , safe=False , status = 401)
    params = {
        "forum" : forumid , 
        "sender" : request.user ,
        }
    msg_query = list(ForumMessage.objects.filter(forum_id = forumid).values('message' , 'author_id' , 'receiver_id'))
    msgs = []
    for msg in msg_query:
        receiver = User.objects.get(id = msg['receiver_id']).username
        sender = User.objects.get(id = msg['author_id']).username
        msgs.append({ "message": msg['message'] , "receiver" : str(receiver) ,  "sender" : str(sender) })
        # msgs.append(["message: " +  msg['message'] , "receiver :" + str(receiver) ,  "sender : "+ str(sender) ]) #for template
    params["msgs"] = msgs
    # print(msgs)
    # return render(request , "chat.html" , params )
    return JsonResponse(params["msgs"] , safe = False , status = 200)

# Create your views here.
