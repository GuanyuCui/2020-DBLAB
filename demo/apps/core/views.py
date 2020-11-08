'''
Description: 
Author: rainym00d
Github: https://github.com/rainym00d
Date: 2020-11-08 15:06:05
LastEditors: rainym00d
LastEditTime: 2020-11-08 17:50:21
'''
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def frontpage(request):
    return render(request, 'core/frontpage.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('frontpage')
    else:
        form = UserCreationForm()

    return render(request, 'core/signup.html', {'form': form})
    