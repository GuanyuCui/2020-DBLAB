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
    url(r'^errors/', views.errors),
    url(r'^index/', views.index),
    url(r'^logout/$', views.logout),
    url(r'^home/', views.home),
    url(r'^insert/', views.insert),
    url(r'^detail/(?P<paperid>[0-9]+)/', views.detail),
    url(r'^check/(?P<paperid>[0-9]+)/', views.check),
    url(r'^modify/(?P<paperid>[0-9]+)/', views.modify),
    url(r'^query/',views.query),
    url(r'^createuser/', views.createuser),


    # 测试上传论文
    url(r'process_q/',views.query_process),
    
    # 
    # API

    url(r'^get_code/',views.get_code),
    url(r'^download/(?P<paperid>[0-9]+)/',views.download, name="download"),
    url(r'^set_password/',views.set_password),
    url(r'delete_tmp_paper', views.delete_tmp_paper),
    url(r'export/(?P<paperids>[\w\D]*)/', views.export),
    url(r'bibtex/', views.bibtex),
    url(r'api_dropbox/', views.api_dropbox),
    #
    #

    url(r'^admin/', admin.site.urls),
]
