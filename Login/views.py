from django.db.models.expressions import F
from django.http.response import JsonResponse
from django.shortcuts import render
import json
from django.contrib.auth.models import User
from Owner.models import UserInfo 
from Pet.models import PetInfo
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login , logout 
from django.core.files.storage import FileSystemStorage
import os
import cloudinary
import cloudinary.uploader

def fun(request):
    return JsonResponse("yes" , safe = False)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload(request , pet_id):
    # print(request.FILES)
    res = {}
    cloudinary.config( 
    cloud_name = os.environ.get("cloud_name"),
    api_key = os.environ.get("api_key"), 
    api_secret = os.environ.get('api_secret')
    )
    if request.FILES:
        files = request.FILES
        for f in files:
            # print(files[f])
            if allowed_file(files[f].name):
                upload_result = cloudinary.uploader.upload(files[f])    
                url = upload_result['url']
                PetInfo.objects.filter(identifier=pet_id).update(profile_pet =  url)
                pet = PetInfo.objects.filter(identifier =pet_id).values('owner_id')
                # print(pet)
                res['msg'] = "file upload success"
                return JsonResponse(res , safe=False , status = 200)
            else:
                res['msg'] = "only .png , .jpg , .jpeg allowed"
                return JsonResponse(res , safe= False , status = 401)
            # fs = FileSystemStorage()
            # filename = fs.save(files[f].name , files[f])
            # url = fs.url('/pet/' + str(pet_id) + '/'+ filename)
            # # print(url)#/projectmedia/pet/7/yes_f1nqIJl.png
            # PetInfo.objects.filter(id = pet_id ).update(profile_pet =  url)
            # pet = PetInfo.objects.filter(id = pet_id).values('owner_id')
            # print(pet)
            # res['msg'] = "file upload success"
            # return JsonResponse(res , safe=False , status = 200)
    res['msg'] = "file upload failed"
    return JsonResponse(res , safe=False , status = 400)

def register(request):
    res = {}
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        name = data['name']
        email = data['email'] 
        password = data['password']
        owner = User.objects.filter(username = username).exists()
        if owner:
            res['msg'] = 'User already exists!'
            return JsonResponse(res ,safe=False, status = 400)
        user = UserInfo.objects.create(
            username = username,
            name = name,
            email = email,
            password=password
        )
        user = User.objects.create_user(username = username  , email = email , password = password)
        user.save()
        res['user'] = list(User.objects.filter(username = username).values('id' , 'username' ,  'email'))
        pet_name = data['pet_name']
        gender = data['gender']
        breed = data['breed']
        description = data['description']
        category = data['category']
        profile_pic = ""
        identifier = len(list(PetInfo.objects.all())) + 1
        pet = PetInfo.objects.create(
            name = pet_name,
            gender = gender,
            breed = breed,
            description = description,
            category = category,
            profile_pet = profile_pic,
            owner_id = user.id,
            identifier = identifier
        )
        res['msg'] = "registration success"
        res['pet'] = identifier
        # print(res)
        return JsonResponse(res , safe=False , status = 200)
    else:
        res['msg'] = "method not allowed"
        return JsonResponse(res ,safe = False ,  status = 405 )

def my_login(request):
    res = {}
    if request.method == 'POST':
        # print(request.META)
        if 'HTTP_AUTHORIZATION' in request.META:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            user = User.objects.filter(username = username).exists()
            if user:
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        owner = User.objects.get(username = username)
                        request.session['user_id'] =  owner.id
                        request.session['user_name'] = owner.username
                    else:
                        res['msg'] = "not an active user"
                        return JsonResponse(res , safe= False , status = 401)
                else:
                    res['msg'] = "Wrong Credentials!"
                    return JsonResponse(res , safe=False , status = 401)
            else:
                res['msg'] = "user does not exists unauthorized!"
                return JsonResponse(res , safe=False , status = 401)
            res['msg'] = "login success"
            # res['sessionid'] = request.session.session_key
            return JsonResponse(res , safe=False , status = 200)
        else:
            res['msg'] = "Bad request"
            return JsonResponse(res , safe= False , status = 400)
    else:
        res['msg'] = "Bad Request"
        return JsonResponse(res , safe= False , status = 401)

@login_required
def my_logout(request):
    # print(request.user)
    res = {}
    if('HTTP_COOKIE' in request.META):
        logout(request)
        res['msg'] = "logout success"
        return JsonResponse(res, safe=False)
    else:
        res['msg'] = "return to signup page/ unauthorized" 
        return JsonResponse(res, safe=False , status = 401)


