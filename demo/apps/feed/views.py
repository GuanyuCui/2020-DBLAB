'''
Description: 
Author: rainym00d
Github: https://github.com/rainym00d
Date: 2020-11-08 18:10:29
LastEditors: rainym00d
LastEditTime: 2020-11-08 18:15:54
'''
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def feed(request):
    return render(request, 'feed/feed.html')