"""Research_Management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from apps import views

urlpatterns = [
    #
    # 页面
    
    url(r'^$', views.test), # 测试
    url(r'^login/', views.login),
    url(r'^logout/$', views.logout),
    url(r'^home/', views.home),
    url(r'^insert/', views.insert),
    url(r'^detail/(?P<paperid>[0-9]+)/', views.detail),
    url(r'^query/',views.query),
    url(r'^createuser/', views.createuser),

    
    # 
    # API

    url(r'^get_code/',views.get_code),


    #
    #

    url(r'^admin/', admin.site.urls),
]
