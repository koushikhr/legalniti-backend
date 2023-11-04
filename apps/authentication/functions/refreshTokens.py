from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .generateTokens import generate_tokens
import jwt
from django.conf import settings


def refresh_tokens(refresh_token_value):
    try:
        decoded_token = jwt.decode(refresh_token_value, settings.SECRET_KEY, algorithms=["HS256"])
        # Check if the token is expired
        if datetime.utcnow() > datetime.fromtimestamp(decoded_token["exp"]):
            return None  # Token has expired
        # Generate a new access token
        return generate_tokens(decoded_token)
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.DecodeError:
        return None  # Token is invalid
