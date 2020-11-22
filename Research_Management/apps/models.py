'''
Description: 
Author: rainym00d
Github: https://github.com/rainym00d
Date: 2020-11-12 13:34:13
LastEditors: Please set LastEditors
LastEditTime: 2020-11-22 13:41:16
'''
from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserInfo(AbstractUser):

    create_time = models.DateField(auto_now_add=True)

    class Meta:
        '''元属性，非必要，但可以辅助阅读'''
        # 元属性快速参考文章：https://www.liujiangblog.com/course/django/99

        # admin页面显示的名字
        verbose_name = '用户表'
        verbose_name_plural = '用户表'

    def __str__(self):
        '''打印时会返回用户名，方便阅读'''
        return self.username

class Author(models.Model):
    authorid = models.CharField(db_column='AuthorID', primary_key=True, max_length=12)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Author'


class Conferjournal(models.Model):
    name = models.CharField(db_column='Name', primary_key=True, max_length=100)  # Field name made lowercase.
    conferorjournal = models.CharField(db_column='ConferOrJournal', max_length=1)  # Field name made lowercase.
    abbreviation = models.CharField(db_column='Abbreviation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ruclevel = models.CharField(db_column='RUCLevel', max_length=2)  # Field name made lowercase.
    ccflevel = models.CharField(db_column='CCFLevel', max_length=2)  # Field name made lowercase.
    ccfchinalevel = models.CharField(db_column='CCFChinaLevel', max_length=2)  # Field name made lowercase.
    issn = models.CharField(db_column='ISSN', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ConferJournal'


class Pa(models.Model):
    paid = models.IntegerField(db_column='PAID', primary_key=True)  # Field name made lowercase.
    papertitle = models.ForeignKey('Paper', models.DO_NOTHING, db_column='PaperTitle')  # Field name made lowercase.
    authorid = models.ForeignKey(Author, models.DO_NOTHING, db_column='AuthorID')  # Field name made lowercase.
    authorrank = models.IntegerField(db_column='AuthorRank')  # Field name made lowercase.
    authoridentity = models.CharField(db_column='AuthorIdentity', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PA'


class Paper(models.Model):
    title = models.CharField(db_column='Title', primary_key=True, max_length=100)  # Field name made lowercase.
    conferorjournal = models.CharField(db_column='ConferOrJournal', max_length=1)  # Field name made lowercase.
    conferjournalname = models.ForeignKey(Conferjournal, models.DO_NOTHING, db_column='ConferJournalName')  # Field name made lowercase.
    publishtime = models.DateField(db_column='PublishTime')  # Field name made lowercase.
    volume = models.IntegerField(db_column='Volume', blank=True, null=True)  # Field name made lowercase.
    issue = models.IntegerField(db_column='Issue', blank=True, null=True)  # Field name made lowercase.
    startpage = models.IntegerField(db_column='StartPage')  # Field name made lowercase.
    endpage = models.IntegerField(db_column='EndPage')  # Field name made lowercase.
    keywords = models.CharField(db_column='Keywords', max_length=100, blank=True, null=True)  # Field name made lowercase.
    conferencelocation = models.CharField(db_column='ConferenceLocation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    papertypeid = models.ForeignKey('Papertype', models.DO_NOTHING, db_column='PaperTypeID')  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Paper'


class Papertype(models.Model):
    typeid = models.IntegerField(db_column='TypeID', primary_key=True)  # Field name made lowercase.
    typename = models.CharField(db_column='TypeName', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PaperType'
        

