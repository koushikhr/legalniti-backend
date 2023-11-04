# const responseJSON = {
# area: ["Gandinagar Tumkur",
# "Settihalli",
#  "Jayanagar Extn Tumkur",
#  "S G Extn Tumkur",
#  "Sit Campus",
#  "Someswarapuram",
# ],
#  country: "India",
#  city: "Tumkur",
#  district: "Tumkur",
#  state: "Karnataka",
#  error: "",
#  message: "Data fetched Successfully",
# };
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import requests
import json
from django.http import HttpResponseBadRequest

@csrf_exempt
def Pincode2(request, pincode):
            if request.method == 'GET':
                if not pincode:
                    return HttpResponseBadRequest("Missing 'pincode' parameter")

                print(f"Received pincode: {pincode}")

                url = (f"https://api.postalpincode.in/pincode/{pincode}")

                response = requests.get(url)
                print("response", response)

                # response_dict = json.loads(response.text)
                return JsonResponse({"response": response})
