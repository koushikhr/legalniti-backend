import json

import jwt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from config import getUsersCollection, getRelationsCollection
from django.conf import settings


@csrf_exempt
def FillipForm(request):
    if request.method == 'POST':
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            bearer_token = auth_header[len('Bearer '):]
            decoded_token = jwt.decode(bearer_token, settings.SECRET_KEY, algorithms=["HS256"])

            userCollection = getUsersCollection()
            relationCollection = getRelationsCollection()


            user = userCollection.find_one({"email": decoded_token['email'], "phone_number": decoded_token['phone_number']})
            # Convert ObjectId fields to strings
            relations = []
            if user:
                # user['_id'] = str(user['_id'])
                # Get the user's ObjectId
                user_id = str(user['_id'])

                # Find all related records in the relation collection using user_id
                relations = list(relationCollection.find({"client_id": user_id}))

                if len(relations) <= 0:
                    relations = list(relationCollection.find({"professional_id": user_id}))

                body = json.loads(request.body)
                formType = "fillip"
                formData = body.get("form_data")

                if "form_type" not in body and "form_data" not in body:
                    return JsonResponse({"message": "Invalid credentials"}, status=401)

                for relation in relations:
                    # relation['_id'] = str(relation['_id'])
                    if relation["services"] and len(relation["services"]) > 0:
                        for service in relation["services"]:
                            if service == formType:
                                print(relation)
                                # Assuming you want to update the 'form_data' field in the relation document
                                # Specify the filter criteria to identify the document to update
                                filter_criteria = {"_id": relation["_id"]}  # Use the appropriate identifier for your document
                                # Specify the updated data
                                updated_data = {"$set": {"fillip": formData}}

                                # Update the document in the MongoDB collection
                                # Update the document in the MongoDB collection and check if it was modified
                                result = relationCollection.update_one(filter_criteria, updated_data)

                                if result.modified_count > 0:
                                    return JsonResponse({"message": "Document updated successfully"})
                                else:
                                    return JsonResponse({"message": "Document not found or no update necessary"},
                                                        status=404)

                # return JsonResponse({"type": formType, "data": formData})

            # return JsonResponse({"user": user, "relations": relations})
        else:
            return JsonResponse({"error": "Invalid authorization header"}, status=401)

    if request.method == 'GET':
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            bearer_token = auth_header[len('Bearer '):]
            decoded_token = jwt.decode(bearer_token, settings.SECRET_KEY, algorithms=["HS256"])

            userCollection = getUsersCollection()
            relationCollection = getRelationsCollection()

            user = userCollection.find_one(
                {"email": decoded_token['email'], "phone_number": decoded_token['phone_number']})
            relations = []
            if user:
                user_id = str(user['_id'])
                relations = list(relationCollection.find({"client_id": user_id}))

                if len(relations) <= 0:
                    relations = list(relationCollection.find({"professional_id": user_id}))

                for relation in relations:
                    relation["_id"] = str(relation["_id"])
                return JsonResponse({"Data": relations})

        return JsonResponse({"Ne amma ": "sdasd"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)