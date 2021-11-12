from django.urls import path, include
from .views import get_events , event_create , create_event_types

urlpatterns = [
    path('get_events/', get_events),
    path('event_create/', event_create),
    path('create_event_types/' , create_event_types)#admin restricted in v2
]