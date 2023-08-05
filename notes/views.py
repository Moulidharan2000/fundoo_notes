from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from logs import logger
from .serializers import NotesSerializer, LabelSerializer, UpdateNoteSerializer, UpdateLabelSerializer, CollaboratorSerializer
from .models import Notes, Label
from user.utils import verify_user
from .utils import RedisNote
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from django.db.models import Q


class NotesAPI(APIView):
    @swagger_auto_schema(request_body=NotesSerializer, operation_summary="Create Note")
    @verify_user
    def post(self, request):
        try:
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisNote.save(request.data.get("user"), serializer.data)
            return Response({"message": "Notes Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def get(self, request):
        try:
            # cache = RedisNote.retrive(request.data.get("user"))
            # if cache:
            #     return Response({"message": "Cache Note Retrieved", "status": 200, "data": cache},
            #                     status=status.HTTP_200_OK)
            notes = Notes.objects.filter(Q(user=request.data.get("user")) | Q(collaborators__id=request.data.get("user")),
                                         is_archive=False, is_trash=False).distinct("id")
            serializer = NotesSerializer(notes, many=True)
            return Response({"message": "Notes Retrieved", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UpdateNoteSerializer, operation_summary="Update Note")
    @verify_user
    def put(self, request):
        try:
            note = Notes.objects.get(id=request.data.get("id"), user=request.data.get("user"))
            serializer = NotesSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisNote.save(request.data.get("user"), serializer.data)
            return Response({"message": "Note Updated", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={"id": openapi.Schema(type=openapi.TYPE_INTEGER)},
                                                     required=["id"]),
                         operation_summary="Delete Notes")
    @verify_user
    def delete(self, request):
        try:
            note = Notes.objects.get(id=request.data.get("id"), user=request.data.get("user"))
            note.delete()
            RedisNote.delete(request.data.get("user"), request.data.get("id"))
            return Response({"message": "Note Deleted", "status": 200, "data": {}},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class LabelAPI(APIView):
    @swagger_auto_schema(request_body=LabelSerializer, operation_summary="Create Label")
    @verify_user
    def post(self, request):
        try:
            serializer = LabelSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Label Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def get(self, request):
        try:
            labels = Label.objects.filter(id=request.data.get("id"), user=request.data.get("user"))
            serializer = LabelSerializer(labels, many=True)
            return Response({"message": "Labels Retrieved", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UpdateLabelSerializer, operation_summary="Update Label")
    @verify_user
    def put(self, request):
        try:
            label = Label.objects.get(id=request.data.get("id"), user=request.data.get("user"))
            serializer = LabelSerializer(label, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Label Updated", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={"id": openapi.Schema(type=openapi.TYPE_INTEGER)},
                                                     required=["id"]),
                         operation_summary="Delete Label")
    @verify_user
    def delete(self, request):
        try:
            label = Label.objects.get(id=request.data.get("id"), user=request.data.get("user"))
            label.delete()
            return Response({"message": "Label Deleted", "status": 200, "data": {}},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class IsArchiveTrash(viewsets.ViewSet):
    @verify_user
    def list(self, request, *args, **kwargs):
        try:
            notes = Notes.objects.filter(user=request.data.get("user"), is_archive=True)
            serializer = NotesSerializer(notes, many=True)
            return Response({"message": "Archive Notes Retrived", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={"id": openapi.Schema(type=openapi.TYPE_INTEGER)}),
                         operation_summary="Create Trash")
    @verify_user
    def create(self, request, *args, **kwargs):
        try:
            note = Notes.objects.get(id=request.data.get("id"), user=request.data.get("user"))
            note.is_archive = True if not note.is_archive else False
            note.save()
            return Response({"message": "Success", "status": 200, "data": {}},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={"id": openapi.Schema(type=openapi.TYPE_INTEGER)}),
                         operation_summary="Create Trash")
    @action(methods=["post"], detail=True)
    @verify_user
    def set_trash(self, request, *args, **kwargs):
        try:
            note = Notes.objects.get(id=request.data.get("id"), user=request.data.get("user"))
            note.is_trash = True if not note.is_trash else False
            note.save()
            return Response({"message": "Success", "status": 200, "data": {}},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=True)
    @verify_user
    def get_trash(self, request, *args, **kwargs):
        try:
            notes = Notes.objects.filter(user=request.data.get("user"), is_trash=True)
            serializer = NotesSerializer(notes, many=True)
            return Response({"message": "Trash Note", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class NotesCollaborators(GenericAPIView, CreateModelMixin, DestroyModelMixin):
    queryset = Notes.objects.all()
    serializer_class = CollaboratorSerializer

    @swagger_auto_schema(request_body=CollaboratorSerializer,
                         operation_summary=" Create Notes Collaborator")
    @verify_user
    def post(self, request, *args, **kwargs):
        try:
            note = Notes.objects.get(id=request.data.get("id"), user_id=request.data.get("user"))
            note.collaborators.add(*request.data.get("collaborators"))
            note.save()
            return Response({"message": "Collaborators Added", "status": 200, "data": {}},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=CollaboratorSerializer,
                         operation_summary=" Delete Notes Collaborator")
    @verify_user
    def delete(self, request, *args, **kwargs):
        try:
            note = Notes.objects.get(id=request.data.get("id"), user_id=request.data.get("user"))
            note.collaborators.remove(*request.data.get("collaborators"))
            return Response({"message": "Collaborator Note Deleted", "status": 200, "data": {}},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

