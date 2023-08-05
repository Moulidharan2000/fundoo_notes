from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'phone', 'location']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=200, write_only=True)
    password = serializers.CharField(max_length=200, write_only=True)
    id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        user = authenticate(**validated_data)
        if not user:
            raise Exception("Invalid Credentials")
        return user
