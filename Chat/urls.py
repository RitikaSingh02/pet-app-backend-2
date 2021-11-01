from django.urls import path , re_path

from .views import chat , forum

urlpatterns = [
    re_path(r"^chat/(?P<username>\w+)/$" , chat),
    re_path(r"^chat/forum/(?P<forumid>\w+)/$" , forum),
    # path('accounts/', include('Login.urls')),

]
