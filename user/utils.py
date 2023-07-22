import jwt
from datetime import datetime, timedelta
from .models import User


class JWToken:
    @staticmethod
    def to_encode(payload):
        if "exp" not in payload.keys():
            payload["exp"] = datetime.utcnow() + timedelta(hours=1)
        return jwt.encode(payload, key="hidden", algorithm="HS256")

    @staticmethod
    def to_decode(token):
        try:
            return jwt.decode(token, key="hidden", algorithms=["HS256"])
        except jwt.PyJWTError as e:
            raise e


def verify_user(function):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get("Token")
        if not token:
            raise Exception("Token not Found")
        payload = JWToken.to_decode(token)
        if "user" not in payload.keys():
            raise Exception("User not Found")
        user = User.objects.filter(id=payload.get("user"))
        if not user.exists():
            raise Exception("User not Found")
        request.data.update({"user": user.first().id})
        return function(self, request, *args, **kwargs)
    return wrapper
