import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..functions import refresh_tokens, verify_access_token

@csrf_exempt
def refresh(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            refresh_token = data.get("refresh_token")

            is_token_verified = verify_access_token(refresh_token)

            if is_token_verified[0] == False:
                return JsonResponse({"message": is_token_verified}, status=409)

            new_tokens = refresh_tokens(refresh_token)
            new_access_token = new_tokens['access_token']
            new_refresh_oken = new_tokens['refresh_token']
            return JsonResponse({"message": "Refresh Successful", "x-users-tokens": {"access_token": new_access_token,"refresh_token": new_refresh_oken}},status=201)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

