from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from logs import logger
from .serializers import NotesSerializer
from .models import Notes


# Create your views here.
class NotesAPI(APIView):
    def post(self, request):
        try:
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Notes Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            notes = Notes.objects.filter(user=request.data.get("user"))
            serializer = NotesSerializer(notes, many=True)
            return Response({"message": "Notes Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            note = Notes.objects.get(id=request.data.get("id"), user=request.data.get("user"))
            serializer = NotesSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Note Updated", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            note = Notes.objects.get(id=request.data.get("id"), user=request.data.get("user"))
            note.delete()
            return Response({"message": "Note Deleted", "status": 200, "data": {}},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)
