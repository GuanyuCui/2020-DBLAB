from django.contrib import admin
from apps import models


# 将models加入到这个列表，才能在后台显示出来

register_list = [
    models.UserInfo,
    models.Author,
    models.Conferjournal,
    models.Pa,
    models.Paper,
    models.Tmppa,
    models.Tmppaper
]

admin.site.register(register_list)