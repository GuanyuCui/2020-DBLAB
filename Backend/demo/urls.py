from django.urls import path
from . import views

app_name = 'demo'

urlpatterns = [
    path('',views.default,name='default'),
    path('<int:paperID>/',views.demo, name='demo'),
    path('interact/',views.interact,name='interact')
]