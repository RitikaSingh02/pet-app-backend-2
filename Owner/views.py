from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http.response import JsonResponse
import json

from .models import UserForum , ForumInfo

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
    



