from django.db import models

# Create your models here.

class Demo(models.Model):
    paperid = models.IntegerField(db_column='paperID', primary_key=True)  # Field name made lowercase.
    content = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'demo'