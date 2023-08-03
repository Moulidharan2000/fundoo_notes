from logs import logger
from rest_framework.views import APIView
from .serializers import RegisterSerializers, LoginSerializers
from rest_framework.response import Response
from rest_framework import status
from .utils import JWToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserRegistration(APIView):

    # Create your views here.
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
