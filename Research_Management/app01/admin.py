from django.contrib import admin
from app01 import models
# Register your models here.


admin.site.register(models.UserInfo)
admin.site.register(models.Blog)
admin.site.register(models.Category)
admin.site.register(models.Tag)
class ArticleConfig(admin.ModelAdmin):
    list_display = ['title','create_time']  # 配置展示字段
    list_display_links = ['title','create_time']  # 指定多个跳转标签
    search_fields = ['title']  # 指定查询  多个字段默认是or的关系

    def patch_init(self,queryset):
        pass
    patch_init.short_description = '批量更新'
    actions = [patch_init,]  # 自定义批量处理函数


    list_filter = ['tags','category']  # 定义外键字段的过滤





admin.site.register(models.Article,ArticleConfig)
admin.site.register(models.Article2Tag)
admin.site.register(models.Comment)
admin.site.register(models.UpAndDown)
