import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from ..functions import *

@csrf_exempt
def name_gen(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method. Use POST."})
    try:
        request_data = json.loads(request.body)
        suffix = request_data.get('company_type')
        desc = request_data.get('desc').strip().lower()
        av_names = []
        # print(suffix)
        # print(desc)
        session_token = fetch_session_token()
        
        # print(session_token)

        if suffix in ["1", "2"]:
            desired_total = 20  # Target number of available names
            while len(av_names) < desired_total:
                base_names = fetch_distinct_names(desc)
                print(base_names)

                with Pool(processes=settings.TOTAL_WORKER_THREAD) as pool:  # You can adjust the number of processes as needed
                    av_names_batch = pool.starmap(check_name_availability, [(name, suffix, session_token) for name in base_names])
                    av_names_batch = [name for name in av_names_batch if name is not None]

                av_names.extend(av_names_batch)
                av_names = list(set(av_names))  # Deduplicate the list

            av_names = av_names[:desired_total]  # Ensure you have 20 available names in the end
            return JsonResponse({"available_names": av_names})
        else:
            return JsonResponse({"error": "Invalid input. Please enter 'llp' or 'private limited'."})
    except Exception as e:
        return JsonResponse({"error": str(e)})
