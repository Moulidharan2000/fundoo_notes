import jwt


class JWToken:
    @staticmethod
    def to_encode(payload):
        return jwt.encode(payload, key="hidden", algorithm="HS256")

    @staticmethod
    def to_decode(token):
        try:
            return jwt.decode(token, key="hidden", algorithms=["HS256"])
        except jwt.PyJWTError as e:
            raise e








    #claims, decorators and custom decorators, expiry
