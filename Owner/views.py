from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required

import json

from .models import UserForum , ForumInfo

@login_required
def forum_create(request):
    res = {}
    if request.method == "POST":
        # create forum
        data = json.loads(request.body)
        forumname = data['forumname']
        description = data['description']
        visibility = data['visibility']
        users = data['users'] #id of users req min users = 2 check at Frontend
        users_id = list(User.objects.filter(username__in = users).values('id'))#{'id': 72}
        users_id.append({'id' : request.user.id})#adding the user too into the forum

        forum = ForumInfo.objects.create(
            forumname = forumname,
            description = description,
            visibility = visibility
        )
        for user in users_id:
            UserForum.objects.create(
                forum_id = forum.id,
                user_id = user['id']
            )
    else:
        res['msg'] = "Method not allowed"
        return JsonResponse(res , safe=False , status = 405)
    res['msg'] = "Forum Created Successfully"
    return JsonResponse(res , safe=False , status = 200)

@login_required
def forum_add(request):
    res = {}
    if request.method == "POST":
        data = json.loads(request.body)
        user_id_list = data['user_id_list']
        forum_id = data['forum_id']
        for user_id in user_id_list:
            UserForum.objects.create(
                forum_id = forum_id,
                user_id = user_id
            )
    else:
        res['msg'] = "Method not allowed"
        return JsonResponse(res , safe=False , status = 405)
    res['msg'] = "User/s added to the forum Successfully"
    return JsonResponse(res , safe=False , status = 200)    

