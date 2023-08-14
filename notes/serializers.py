from rest_framework import serializers
from .models import Notes, Label


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'image', 'user', 'remainder', 'created_at', 'updated_at', 'is_archive',
                  'is_trash']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'user', 'color', 'font']


class UpdateNoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    remainder = serializers.DateTimeField(required=False)


class UpdateLabelSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(max_length=200)
    color = serializers.CharField(max_length=200)
    font = serializers.CharField(max_length=200)


class CollaboratorSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    collaborators = serializers.ListField(child=serializers.IntegerField())
    access_type = serializers.CharField(max_length=200, default="read_only")


class LabelCollaboratorSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    labels = serializers.ListField(child=serializers.IntegerField())
