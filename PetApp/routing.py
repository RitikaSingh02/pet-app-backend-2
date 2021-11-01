from channels.routing import ProtocolTypeRouter , URLRouter
from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from Chat.consumers import ChatConsumer , ForumConsumer
from .settings import ALLOWED_HOSTS
application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    # r'^index/$', views.index, name='index
                    re_path(r"^chat/chat/(?P<username>\w+)/$" , ChatConsumer().as_asgi() , name="chatconsumer"),
                    re_path(r"^chat/chat/forum/(?P<forumid>\w+)/$" , ForumConsumer().as_asgi() , name="groupconsumer"),

                ]
            )
        )
    )
})

# ws://domain/<username>