'''
Description: 
Author: rainym00d
Github: https://github.com/rainym00d
Date: 2020-11-08 16:39:36
LastEditors: rainym00d
LastEditTime: 2020-11-08 16:47:11
'''
from django.db import models

from django.contrib.auth.models import User

class MyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
User.myprofile = property(lambda  u: MyProfile.objects.get_or_create(user=u)[0])

