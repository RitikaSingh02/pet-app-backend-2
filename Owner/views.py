from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required

import json

from .models import UserForum , ForumInfo , UserConnections , UserFeeds

import os
import cloudinary
import cloudinary.uploader

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

@login_required
def connections_add(request):
    res = {}
    if request.method == "POST":
        data = json.loads(request.body)
        connection_req_id = data['connection_id']
        UserConnections.objects.create(
            user_id = request.user.id,
            connection_id = connection_req_id
        )
        res['msg'] = "User added to connections"
        return JsonResponse(res , safe = False , status = 200)
    res['msg'] = "Method not allowed"
    return JsonResponse(res , safe = False , status = 405)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def feed_img_upload(request):
    res = {}
    cloudinary.config( 
    cloud_name = os.environ.get("cloud_name"),
    api_key = os.environ.get("api_key"), 
    api_secret = os.environ.get('api_secret')
    )
    if request.FILES:
        files = request.FILES
        for f in files:
            if allowed_file(files[f].name):
                upload_result = cloudinary.uploader.upload(files[f])    
                url = upload_result['url']
                curr_feed = UserFeeds.objects.get_or_create(
                    user_id = request.user.id,
                    feed_img = url
                )
                # print(curr_feed[0].id)
                res['msg'] = "file upload success"
                res['curr_feed_id'] = curr_feed[0].id
                return JsonResponse(res , safe=False , status = 200)
            else:
                res['msg'] = "only .png , .jpg , .jpeg allowed"
                return JsonResponse(res , safe= False , status = 401)
    res['msg'] = "file upload failed"
    return JsonResponse(res , safe=False , status = 400)

@login_required
def feed_create(request):
    res = {}
    if request.method == "POST":
        data = json.loads(request.body)
        curr_feed = data['curr_feed_id']
        feed_title = data['feed_title']
        feed_caption = data['feed_caption']
        UserFeeds.objects.filter(id = curr_feed).update(
            feed_title = feed_title,
            feed_caption = feed_caption,
            feed_status = "success"
        )
        res['msg'] = 'Feed upload sucess'
        return JsonResponse(res , safe = False , status = 200)
    res['msg'] = "Method not allowed"
    return JsonResponse(res , safe = False , status = 405)

@login_required
def get_all_feed(request):
    res = {}
    q = list(UserFeeds.objects.filter(user_id = request.user.id , feed_status = "success").values())
    res['feeds'] = q
    return JsonResponse(res , safe = False , status = 200)
    
