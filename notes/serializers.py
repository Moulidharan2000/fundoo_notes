from rest_framework import serializers
from .models import Notes


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'image', 'user', 'remainder', 'created_at', 'updated_at']

    # def create(self, validated_data):
    #     note = Notes.objects.create(**validated_data)
    #     return note