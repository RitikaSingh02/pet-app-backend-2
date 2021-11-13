from django.urls import path, include

from .views import forum_add, forum_create

urlpatterns = [
    path('create/', forum_create),
    path('add/', forum_add),

]