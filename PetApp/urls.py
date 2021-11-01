from django.contrib import admin
from django.urls import path
from django.urls.conf import include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('Login.urls')),
    path('chat/', include('Chat.urls')),
    path('pet/', include('Pet.urls')),
    path('forum/', include('Owner.urls')),


    # path('accounts/', include('Login.urls')),

]
