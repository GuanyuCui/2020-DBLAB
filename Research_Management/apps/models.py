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
        return str(self.username)

class Author(models.Model):
    authorid = models.CharField(db_column='AuthorID', primary_key=True, max_length=12)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'author'

    def __str__(self):
        '''打印时会返回用户名，方便阅读'''
        return "(authorID:{}, authorName:{})".format(self.authorid, self.name)

class Conferjournal(models.Model):
    name = models.CharField(db_column='Name', primary_key=True, max_length=512)  # Field name made lowercase.
    conferorjournal = models.CharField(db_column='ConferOrJournal', max_length=1)  # Field name made lowercase.
    abbreviation = models.CharField(db_column='Abbreviation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ruclevel = models.CharField(db_column='RUCLevel', max_length=2)  # Field name made lowercase.
    ccflevel = models.CharField(db_column='CCFLevel', max_length=2)  # Field name made lowercase.
    ccfchinalevel = models.CharField(db_column='CCFChinaLevel', max_length=2)  # Field name made lowercase.
    issn = models.CharField(db_column='ISSN', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'conferjournal'

    def __str__(self):
        '''打印时会返回Conferjournal的name，方便阅读'''
        return self.name


class Pa(models.Model):
    paid = models.BigAutoField(db_column='PAID', primary_key=True)  # Field name made lowercase.
    paperid = models.ForeignKey('Paper', models.DO_NOTHING, db_column='PaperID')  # Field name made lowercase.
    authorname = models.CharField(db_column='AuthorName', max_length=20)  # Field name made lowercase.
    authorrank = models.IntegerField(db_column='AuthorRank')  # Field name made lowercase.
    authoridentity = models.CharField(db_column='AuthorIdentity', max_length=20)  # Field name made lowercase.
    authortype = models.CharField(db_column='AuthorType', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'pa'


class Paper(models.Model):
    paperid = models.BigAutoField(db_column='PaperID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=1024)  # Field name made lowercase.
    conferorjournal = models.CharField(db_column='ConferOrJournal', max_length=1)  # Field name made lowercase.
    conferjournalname = models.ForeignKey(Conferjournal, models.DO_NOTHING, db_column='ConferJournalName')  # Field name made lowercase.
    publishtime = models.DateField(db_column='PublishTime')  # Field name made lowercase.
    volume = models.IntegerField(db_column='Volume', blank=True, null=True)  # Field name made lowercase.
    issue = models.IntegerField(db_column='Issue', blank=True, null=True)  # Field name made lowercase.
    startpage = models.IntegerField(db_column='StartPage')  # Field name made lowercase.
    endpage = models.IntegerField(db_column='EndPage')  # Field name made lowercase.
    keywords = models.CharField(db_column='Keywords', max_length=100, blank=True, null=True)  # Field name made lowercase.
    conferencecountry = models.CharField(db_column='ConferenceCountry', max_length=50, blank=True, null=True)  # Field name made lowercase.
    conferencecity = models.CharField(db_column='ConferenceCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    papertype = models.CharField(db_column='PaperType', max_length=20)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'paper'

    def __str__(self):
        '''打印时会返回Paper的title，方便阅读'''
        return self.title

class Tmppa(models.Model):
    paid = models.BigAutoField(db_column='PAID', primary_key=True)  # Field name made lowercase.
    paperid = models.ForeignKey('Tmppaper', models.CASCADE, db_column='PaperID')  # Field name made lowercase.
    authorname = models.CharField(db_column='AuthorName', max_length=20)  # Field name made lowercase.
    authorrank = models.IntegerField(db_column='AuthorRank')  # Field name made lowercase.
    authoridentity = models.CharField(db_column='AuthorIdentity', max_length=20)  # Field name made lowercase.
    authortype = models.CharField(db_column='AuthorType', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tmppa'

class Tmppaper(models.Model):
    paperid = models.BigAutoField(db_column='PaperID', primary_key=True)  # Field name made lowercase.
    commitauthorid = models.ForeignKey(Author, models.DO_NOTHING, db_column='CommitAuthorID')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=1024)  # Field name made lowercase.
    conferorjournal = models.CharField(db_column='ConferOrJournal', max_length=1)  # Field name made lowercase.
    conferjournalname = models.ForeignKey(Conferjournal, models.DO_NOTHING, db_column='ConferJournalName')  # Field name made lowercase.
    publishtime = models.DateField(db_column='PublishTime')  # Field name made lowercase.
    volume = models.IntegerField(db_column='Volume', blank=True, null=True)  # Field name made lowercase.
    issue = models.IntegerField(db_column='Issue', blank=True, null=True)  # Field name made lowercase.
    startpage = models.IntegerField(db_column='StartPage')  # Field name made lowercase.
    endpage = models.IntegerField(db_column='EndPage')  # Field name made lowercase.
    keywords = models.CharField(db_column='Keywords', max_length=100, blank=True, null=True)  # Field name made lowercase.
    conferencecountry = models.CharField(db_column='ConferenceCountry', max_length=50, blank=True, null=True)  # Field name made lowercase.
    conferencecity = models.CharField(db_column='ConferenceCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    papertype = models.CharField(db_column='PaperType', max_length=20)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tmppaper'