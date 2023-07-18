from django.db import models


# Create your models here.
# attributes - first_name, lastname, username - unique, password, email, phone, location
# APIs - create or register user, login user.

class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_num = models.BigIntegerField()
    location = models.CharField(max_length=200)

