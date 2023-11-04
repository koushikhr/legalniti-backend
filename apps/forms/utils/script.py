from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def Script(request):
    if request.method == 'GET':
        return JsonResponse({"Script": "Output"})