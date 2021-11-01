import asyncio
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.checks import messages
from django.http import request
from django.shortcuts import render
from Chat.views import forum
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Message , ForumMessage
from Owner.models import UserForum

class ChatConsumer(AsyncConsumer ):
    def __init__(self):
        self.sender = ""
        self.receiver = ""
        self.chat_room = ""
    async def websocket_connect(self , event):
        print("connected" , event)

        await self.send({
                "type":"websocket.accept"
            })
        await self.send({
            "type":"websocket.send",
            "text":"heya welcome to individual chats!!"
        })
        self.receiver = self.scope['url_route']['kwargs']['username']
        self.sender = self.scope['user']
        chatroom = "static1" 
        self.chat_room  = chatroom
        print(self.chat_room)

        await self.channel_layer.group_add(
            self.chat_room ,
            self.channel_name
        )
        print("receiver:",  self.receiver , "sender:" ,self.sender)

    async def websocket_receive(self , event ):
        print(event)
        # if self.chat_room!="":
        receiver = User.objects.get(username = self.receiver)
        sender = User.objects.get(username = self.sender)
        Message.objects.create(
        author_id = sender.id,
        receiver_id = receiver.id,
        message = event['text']
        )
        print("created with sender=" , sender.username , "receiver=" , receiver.username )
        new_event = {
        "type":"chat_message",
        "msg" : "this is a instant message",
        "text" : event['text'],
        "sender":sender.username
        }
        # a sort of broadcasting the msg into the group
        await self.channel_layer.group_send(
            self.chat_room,
            new_event
        )

        print("received" , event)

    async def chat_message(self, event):
        # sending the actual msg
        # print(event)
        front_response = event.get('text', None)
        # print("front_res" , front_response)
        if front_response is not None:
            compiled_response_data = front_response
        final_response = dict(text = front_response , sender = event.get('sender', None))

        # Send message to WebSocket
        await self.send({
            'type':'websocket.send',
            'text': json.dumps(final_response)
        })

    async def websocket_disconnect(self , event):
        print("disconnected" , event)

    @database_sync_to_async
    def chat(self , msg , sender , receiver):
        receiver = User.objects.get(username = receiver)
        sender = User.objects.get(username = sender)
        new_msg =  Message.objects.create(
            author_id = sender.id,
            receiver_id = receiver.id,
            message = msg
        )
        print("msgs created")
        return new_msg

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
class ForumConsumer(AsyncConsumer):
    def __init__(self):
        self.sender = ""
        self.receiver = []
        self.chat_room = ""
        self.forumId = 0

    async def websocket_connect(self , event):
        print("connected to forum" , event)

        await self.send({
                "type":"websocket.accept"
            })
        await self.send({
            "type":"websocket.send",
            "text":"heya welcome to forums!!"
        })

        self.sender = self.scope['user']
        self.forumId = int(self.scope['url_route']['kwargs']["forumid"])
        self.chat_room  = "ForumChat_" + str(self.forumId)
        self.receiver = []
        print("forumid" , self.forumId)
        forum_members = list(UserForum.objects.filter(forum_id = self.forumId).values('user_id'))
        print(forum_members)

        for member in forum_members:
            self.receiver.append(member['user_id'])
        #extracted from the db

        await self.channel_layer.group_add(
            self.chat_room ,
            self.channel_name
        )
        print("receiver:",  self.receiver , "sender:" ,self.sender , "forum:" , self.chat_room)

    async def websocket_receive(self , event ):
        print(event)

        sender = User.objects.get(username = self.sender)
        for i in self.receiver:
            ForumMessage.objects.create(
            author_id = sender.id,
            receiver_id = i,
            message = event['text'],
            forum_id = self.forumId
            )
        print("created with sender=" , sender.username , "receiver:",  self.receiver )

        new_event = {
        "type":"chat_message",
        "msg" : "this is a instant message",
        "text" : event['text'],
        "sender":sender.username
        }
        # a sort of broadcasting the msg into the group
        await self.channel_layer.group_send(
            self.chat_room,
            new_event
        )
        print("received" , event)

    async def chat_message(self, event):
        front_response = event.get('text', None)

        if front_response is not None:
            compiled_response_data = front_response
        final_response = dict(text = front_response , sender = event.get('sender', None))
        # Send message to WebSocket
        await self.send({
            'type':'websocket.send',
            'text': json.dumps(final_response)
        })

    async def websocket_disconnect(self , event):
        print("disconnected" , event)

    @database_sync_to_async
    def chat(self , msg , sender , receiver):
        receiver = User.objects.get(username = receiver)
        sender = User.objects.get(username = sender)
        new_msg =  Message.objects.create(
            author_id = sender.id,
            receiver_id = receiver.id,
            message = msg
        )
        print("msgs created")
        return new_msg
