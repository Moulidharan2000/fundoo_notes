import json

from django.forms import model_to_dict
from django.http import JsonResponse
from .models import User
from logs import logger


# Create your views here.
def create_user(request):
    try:
        if not request.method == 'POST':
            raise Exception("Method not allowed")
        data = json.loads(request.body)
        user = User.objects.create(**data)
        return JsonResponse(model_to_dict(user))
    except Exception as ex:
        logger.exception(ex)
        return JsonResponse({"message": str(ex)})


def login_user(request):
    try:
        if not request.method == 'POST':
            raise Exception("Method not allowed")
        data = json.loads(request.body)
        user = User.objects.filter(user_name=data.get("user_name"), password=data.get("password"))
        if not user.exists():
            raise Exception("Invalid Credentials")
        return JsonResponse({"message": "login successful"})
    except Exception as ex:
        logger.exception(ex)
        return JsonResponse({"message": str(ex)})
