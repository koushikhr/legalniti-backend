import json

import jwt
import datetime
from django.conf import settings

# Secret key for token encoding and decoding (You should use a strong, secret key in a production environment)
# SECRET_KEY = "your_secret_key_here"

# Function to generate both access and refresh tokens
def generate_tokens(data):
    # Calculate the expiration time for access and refresh tokens (example: 15 minutes for access, 7 days for refresh)
    access_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    refresh_exp = datetime.datetime.utcnow() + datetime.timedelta(days=7)

    # Create the access token
    access_payload = {
        "email": data["email"],
        "phone_number": data["phone_number"],
        "role": data["role"],
        "exp": access_exp
    }
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")

    # Create the refresh token
    refresh_payload = {
        "email": data["email"],
        "phone_number": data["phone_number"],
        "exp": refresh_exp
    }
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

    # Create a dictionary to hold the tokens
    tokens_dict = {
        "access_token": access_token.decode('utf-8'),
        "refresh_token": refresh_token.decode('utf-8')
    }

    return tokens_dict