import json

from django.forms import model_to_dict
from django.http import JsonResponse
from .models import User
from logs import logger
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .serializers import RegisterSerializers, LoginSerializers
from rest_framework.response import Response
from rest_framework import status


class UserRegistration(APIView):

    # Create your views here.
    def post(self, request):
        try:
            serializer = RegisterSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "User Created", "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "login successful", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)
