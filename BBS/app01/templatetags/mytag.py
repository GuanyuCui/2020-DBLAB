from django.template import Library
from app01 import models
from django.db.models.functions import TruncMonth
from django.db.models import Count

register = Library()


@register.inclusion_tag('left_menu.html')
def index(username):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    blog = user_obj.blog
    # 1.查询当前用户所有的分类及分类下的文章数
    category_list = models.Category.objects.filter(blog=blog).annotate(count_num=Count('article__pk')).values_list(
        'name', 'count_num', 'pk')

    # 2.查询当前用户所有的标签及标签下的文章数
    tag_list = models.Tag.objects.filter(blog=blog).annotate(count_num=Count('article__pk')).values_list('name',
                                                                                                         'count_num',
                                                                                                         'pk')

    # 3.按照年月统计文章数
    date_list = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values(
        'month').annotate(count_num=Count('pk')).order_by('-month').values_list('month', 'count_num')
    return locals()
    # return {'username':username,'blog':blog}