from django.db import models
from user.models import User


class Notes(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    image = models.ImageField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    remainder = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notes'


class Label(models.Model):
    name = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=200)
    font = models.CharField(max_length=200)

    class Meta:
        db_table = 'label'


