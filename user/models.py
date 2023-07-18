from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    phone = models.BigIntegerField(null=True)
    location = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = "user"

