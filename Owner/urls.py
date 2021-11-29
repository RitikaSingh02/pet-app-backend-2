from django.urls import path, include

from .views import connections_add, forum_add, forum_create , feed_img_upload , feed_create , get_all_feed

urlpatterns = [
    path('forum_create/', forum_create),
    path('forum_add/', forum_add),
    path('connections_add/' , connections_add),
    path('feed_img_upload/' , feed_img_upload),
    path('feed_create/' , feed_create),
    path('get_all_feed/' , get_all_feed)
]