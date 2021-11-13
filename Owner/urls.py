from django.urls import path, include

from .views import connections_add, forum_add, forum_create

urlpatterns = [
    path('forum_create/', forum_create),
    path('forum_add/', forum_add),
    path('connections_add/' , connections_add)
]