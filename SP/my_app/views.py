from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *

import datetime

from sqlalchemy import create_engine, ForeignKey, Column,String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from rest_framework.exceptions import PermissionDenied

import pandas as pd

# Create your views here.

engine = create_engine('postgresql+psycopg2://postgres:admin@localhost:5432/sp', echo=True)

conn = engine.connect()

# Custom Login Required
def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Check if the request contains email and password
        data = pd.read_sql("SELECT * from  my_app_user",conn)
        print("\n\n\n data -> ",data)

        email = request.request.data.get('email')
        password = request.request.data.get('password')
    
        if email and password:
            users = data.loc[:,['email','password']]
            if email in list(data['email']):
                pass1 = users.loc[users["email"]==email]["password"]
                if pass1.iloc[0] == password:
                    return view_func(request, *args, **kwargs)
        raise PermissionDenied(detail='Authentication required')
    return wrapper


# user sign up
class UserSignUp(APIView):
    def post(self, request):
        name = request.data['name']
        email = request.data['email']
        password = request.data["password"]

        try:
            if User.objects.all().get(name=name):
                return Response({'message':'Username Not Available'})
        except:
            pass

        try:
            if User.objects.all().get(email=email):
                return Response({'message':'This email is already registered'})
        except:
            pass

        new_user = User.objects.create(name=name,email=email,password=password)
        new_user.is_validate = True
        new_user.save()
        return Response({'message':'registraion Successfull'})
        # messages.success(request,"registraion Successfull")


#post upload
class UploadPost(APIView):
    @custom_login_required
    def post(self, request):
        title1 = pd.read_sql("SELECT title from  my_app_post",conn)
        title1 = title1["title"]
        lst = []
        for t in title1:
            lst.append(t)

        email = request.data.get("email")
        user = User.objects.get(email=email)

        title = request.data.get('title')
        if title in lst:
            return Response({'message':'This title already used'})

        content = request.FILES.get('content')
        description = request.FILES.get('description')

        # new_post = Post.objects.create(user=user,title=title,image=image,likes=likes)
        new_post = Post.objects.create(user=user,title=title,content=content,description=description)
        new_post.save()

        return Response({'message':'Post Added Successfully'})
    
    @custom_login_required
    def patch(self, request):
        post_id = request.data.get('post')
        post = Post.objects.get(id=post_id)

        if request.data.get('title'):
            title1 = pd.read_sql("SELECT title from  my_app_post",conn)
            title1 = title1["title"]
            lst = []
            for t in title1:
                lst.append(t)
            title = request.data.get('title')
            if title in lst:
                return Response({'message':'This title already used'})
            else:
                post.title = title
        
        if request.data.get('description'):
            post.description = request.data.get('description')
        if request.data.get('content'):
            post.content = request.data.get('content')
        post.save()
        return Response({'message':'Post Updated...'})


class DoLike(APIView):
    @custom_login_required
    def post(slef, request):
        post_id = request.data.get("post")
        email = request.data.get("email")

        user = User.objects.get(email=email)
        post = Post.objects.get(id=post_id)

        try:
            if Like.objects.all().get(user=user,post=post):
                return Response({'message':'Already Liked...'})
        except:
            pass

        like = Like.objects.create(user=user,post=post)
        like.save()
        return Response({'message':'Like Added'})


class GetAllPost(APIView):
    def get(self, request):
        posts = Post.objects.all().values()
        post = []
        for p in posts:
            likes = Like.objects.filter(post_id=p["id"]).count()
            p["likes"] = likes
            post.append(p)
        return Response({'Posts':f'{post}'})