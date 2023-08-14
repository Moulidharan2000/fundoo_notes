from django.contrib import admin
from .models import Notes, Label, Collaborators

# Register your models here.
admin.site.register(Notes)
admin.site.register(Label)
admin.site.register(Collaborators)