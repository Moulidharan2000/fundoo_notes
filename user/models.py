from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    phone = models.BigIntegerField(null=True)
    location = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = "user"


# user log model, attr- method, url, count(default=1)
class LogModel(models.Model):
    method = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    count = models.IntegerField(default=1)

    class Meta:
        db_table = "user_log"

