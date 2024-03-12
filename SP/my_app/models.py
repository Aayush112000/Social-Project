from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=20)
    created_at=  models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500,null=True,blank=True)
    description = models.CharField(null=True,blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    created_at=  models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at=  models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)