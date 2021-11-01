from django.urls import path, include

from .views import forum_create

urlpatterns = [
    path('create/', forum_create),
]