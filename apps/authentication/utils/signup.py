import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from config import getUsersCollection
from bson.json_util import dumps
from ..functions import generate_tokens

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get("email")
            phone_number = data.get("phone_number")
            data["role"] = "Client"

            if not email and not phone_number:
                return JsonResponse({"message": "Invalid credentials"}, status=401)

            collection = getUsersCollection()

            # Check if email already exists in the database
            existing_email = collection.find_one({"email": email})

            # Check if phNum already exists in the database
            existing_phNum = collection.find_one({"phone_number": phone_number})

            if existing_email and existing_phNum:
                return JsonResponse({"message": "Email and Phone number both already exist"}, status=409)
            elif existing_email:
                return JsonResponse({"message": "Email already exists"}, status=409)
            elif existing_phNum:
                return JsonResponse({"message": "Phone number already exists"}, status=409)

            # Insert the user data into the collection
            result = collection.insert_one(data)

            # Check if the insertion was successful
            if result.acknowledged:
                inserted_id = result.inserted_id
                serialized_id = dumps({"_id": inserted_id})

                user = collection.find_one({"email": email})
                if user:
                    tokens = generate_tokens(data)
                    access_token = tokens['access_token']
                    refresh_token = tokens['refresh_token']
                    if access_token and refresh_token:
                        # Tokens were successfully created
                        return JsonResponse({"message": "Signup successful", "x-users-tokens": {"access_token": access_token,
                                             "refresh_token": refresh_token}}, status=201)
                    else:
                        # Authentication failed, handle the error
                        return JsonResponse({"message": "Authentication failed"}, status=401)
            else:
                return JsonResponse({"message": "Signup failed"}, status=500)

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=400)

