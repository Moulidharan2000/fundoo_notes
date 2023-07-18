import json

from django.forms import model_to_dict
from django.http import JsonResponse
from .models import User
from logs import logger
from django.contrib.auth import authenticate


# Create your views here.
def create_user(request):
    try:
        if not request.method == 'POST':
            raise Exception("Method not allowed")
        data = json.loads(request.body)
        user = User.objects.create_user(**data)
        return JsonResponse(model_to_dict(user))
    except Exception as ex:
        logger.exception(ex)
        return JsonResponse({"message": str(ex)})


def login_user(request):
    try:
        if not request.method == 'POST':
            raise Exception("Method not allowed")
        data = json.loads(request.body)
        user = authenticate(**data)
        if not user:
            raise Exception("Invalid Credentials")
        return JsonResponse({"message": "login successful"})
    except Exception as ex:
        logger.exception(ex)
        return JsonResponse({"message": str(ex)})
