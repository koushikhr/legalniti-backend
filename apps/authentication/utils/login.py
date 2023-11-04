import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from config import getUsersCollection
from ..functions import generate_tokens


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if "email" not in data and "phone_number" not in data:
                return JsonResponse({"message": "Invalid credentials"}, status=401)

            collection = getUsersCollection()

            # Check if the user exists in the collection
            user = collection.find_one({"email": data.get("email"), "phone_number": data.get("phone_number")})
            if user:
                tokens = generate_tokens(user)
                access_token = tokens ['access_token']
                refresh_token = tokens ['refresh_token']

                if access_token and refresh_token:
                    # Tokens were successfully created
                    return JsonResponse(
                        {"message": "Login successful", "x-users-tokens": {"access_token": access_token, "refresh_token": refresh_token}},
                        status=200)
                else:
                    # Authentication failed, handle the error
                    return JsonResponse({"message": "Authentication failed"}, status=401)
            else:
                return JsonResponse({"message": "Invalid credentials"}, status=401)

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=400)
