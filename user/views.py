from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from logs import logger
from rest_framework.views import APIView
from .models import User
from .serializers import RegisterSerializers, LoginSerializers
from rest_framework.response import Response
from rest_framework import status
from .utils import JWToken
from drf_yasg.utils import swagger_auto_schema
from django.views.generic import View
from django.contrib import messages


class UserRegistration(APIView):
    @swagger_auto_schema(request_body=RegisterSerializers)
    def post(self, request):
        try:
            serializer = RegisterSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "User Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    @swagger_auto_schema(request_body=LoginSerializers)
    def post(self, request):
        try:
            serializer = LoginSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = JWToken.to_encode({"user": serializer.data.get("id")})
            return Response({"message": "login successful", "status": 200, "token": token},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class JinjaRegistration(View):
    def get(self, request):
        return render(request, 'UserRegister.html')

    def post(self, request):
        try:
            data = {x: y for x, y in request.POST.items()}
            data.pop('csrfmiddlewaretoken')
            User.objects.create_user(**data)
            messages.info(request, "User Registered Successfully")
            return redirect('login')
        except Exception as ex:
            messages.error(request, str(ex))
            return render(request, 'UserRegister.html')


class JinjaLogin(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'UserLogin.html')

    def post(self, request):
        try:
            data = {x: y for x, y in request.POST.items()}
            data.pop('csrfmiddlewaretoken')
            user = authenticate(**data)
            if not user:
                raise Exception("Invalid Credentials")
            login(request, user)
            return redirect('index')
        except Exception as ex:
            messages.error(request, str(ex))
            return render(request, 'UserLogin.html')


def home_page(request):
    return render(request, 'index.html', context={"user": request.user})


def user_logout(request):
    logout(request)
    return redirect('login')
