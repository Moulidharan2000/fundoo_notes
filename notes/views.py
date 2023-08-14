import json

from django.db import connection
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from logs import logger
from .serializers import NotesSerializer, LabelSerializer, UpdateNoteSerializer, \
    UpdateLabelSerializer, CollaboratorSerializer, LabelCollaboratorSerializer
from .models import Notes, Label, Collaborators
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
            notes = Notes.objects.filter(
                Q(user=request.data.get("user")) | Q(collaborators__id=request.data.get("user")),
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
            note = Notes.objects.filter(id=request.data.get("id"), user=request.data.get("user"))
            if not note.exists():
                note = Notes.objects.filter(note__note_id=request.data.get("id"), note__user_id=request.data.get("user"),
                                            note__access_type="writable")
            if not note.exists():
                raise Exception("Not Authorized to perform update")
            note = note.first()
            request.data["user"] = note.user_id
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
            # note.collaborators.remove(*request.data.get("collaborators"))
            # note.collaborators.add(*request.data.get("collaborators"),
            #                        through_defaults={"access_type": request.data.get("access_type")})
            # note.save()
            for i in request.data.get("collaborators"):
                Collaborators.objects.update_or_create(note_id=note.id, user_id=i,
                                                       defaults={"access_type": request.data.get("access_type")})
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
            return Response({"message": "Labels Retrieved", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
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


class LabelRaw(APIView):
    @swagger_auto_schema(request_body=LabelSerializer, operation_summary="Create Label")
    @verify_user
    def post(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT into label (name, user_id, color, font) VALUES(%s, %s, %s, %s)",
                               [request.data.get("name"), request.data.get("user"),
                                request.data.get("color"), request.data.get("font")])
                cursor.execute("SELECT * from label order by id desc limit 1")
                row = cursor.fetchone()
                column = [x[0] for x in cursor.description]
                result = dict(zip(column, row))
                return Response({"message": "Notes Created", "status": 201, "data": result},
                                status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @verify_user
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * from label where user_id=%s", [request.data.get("user")])
                row = cursor.fetchall()
                column = [x[0] for x in cursor.description]
                result = [dict(zip(column, x)) for x in row]
                return Response({"message": "Labels Retrieved", "status": 201, "data": result},
                                status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UpdateLabelSerializer, operation_summary="Update Label")
    @verify_user
    def put(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE label SET  name=%s, color=%s, font=%s where id=%s and user_id=%s",
                               [request.data.get("name"), request.data.get("color"),
                                request.data.get("font"), request.data.get("id"), request.data.get("user")])
                cursor.execute("SELECT * from label where id=%s", [request.data.get("id")])
                row = cursor.fetchone()
                column = [x[0] for x in cursor.description]
                result = dict(zip(column, row))
                return Response({"message": "Label Updated", "status": 200, "data": result},
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
            with connection.cursor() as cursor:
                cursor.execute("DELETE from label where id=%s", [request.data.get("id")])
                return Response({"message": "Label Deleted", "status": 200, "data": {}},
                                status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class LabelCollaborators(GenericAPIView, CreateModelMixin, DestroyModelMixin):
    queryset = Notes.objects.all()
    serializer_class = LabelCollaboratorSerializer

    @swagger_auto_schema(request_body=LabelCollaboratorSerializer,
                         operation_summary=" Create Label Collaborator")
    @verify_user
    def post(self, request, *args, **kwargs):
        try:
            notes = Notes.objects.get(id=request.data.get("id"), user_id=request.data.get("user"))
            notes.label.add(*request.data.get("labels"))
            notes.save()
            return Response({"message": "Label Added to Note", "status": 200, "data": {}},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=LabelCollaboratorSerializer,
                         operation_summary=" Delete Label Collaborator")
    @verify_user
    def delete(self, request, *args, **kwargs):
        try:
            note = Notes.objects.get(id=request.data.get("id"), user_id=request.data.get("user"))
            note.label.remove(*request.data.get("labels"))
            return Response({"message": "Note Label Deleted", "status": 200, "data": {}},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.exception(ex)
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)
