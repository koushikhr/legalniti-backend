import jwt
from django.conf import settings

def verify_access_token(access_token: object) -> object:
    try:
        decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        if decoded_token['email']:
            return [True, decoded_token]
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.DecodeError:
        return None  # Token is invalid