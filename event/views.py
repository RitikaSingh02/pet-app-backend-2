from django.shortcuts import render
from django.http.response import JsonResponse
import json
from django.contrib.auth.decorators import login_required

from .models import Events , EventTypes
from .Scripts.event_script import create_event_type

from datetime import datetime

@login_required
def event_create(request):
    res = {}
    if(request.method == "POST"):
        data = json.loads(request.body)
        event_type = data['event_type']
        event_description = data['event_description']
        event_name = data['event_name']
        event_venue = data['event_venue']
        date_time = data['date_time']
        date_time = datetime.strptime(date_time, '%m %d %Y %H:%M')
        # print(date_time)
        # print(request.user)
        Events.objects.create(
            event_name = event_name,
            event_venue = event_venue,
            event_type_id =  event_type, 
            date_of_event = date_time,
            user_id = request.user.id ,
            event_description = event_description
        )
        res["msg"] = "Event Creation Success"
        return JsonResponse(res , safe = False , status = 200)
    res['msg'] = "Method not Allowed"
    return JsonResponse(res , safe=False , status = 405)

def get_events(request): #get all events
    res = {}
    if(request.method == "GET"):
        all_event_type = list(EventTypes.objects.all().values("id" ,"type_name" , "type_decription"))
        res['msg'] = "Success"
        res['all_event_types'] = all_event_type
        return JsonResponse(res , safe = False , status =200)
    res['msg'] = "Method not allowed"
    return JsonResponse(res , safe= False , status = 405)

def create_event_types(request):
    res = {}
    create_event_type()
    res['msg'] = "Event types created successfully"
    return JsonResponse(res , safe = False , status = 200)