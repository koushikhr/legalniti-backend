from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import requests
import json
import urllib.parse
from django.http import HttpResponseBadRequest
import io
import urllib.request
import tempfile
from PIL import Image
from easyocr import Reader
from ultralytics.models.yolo import YOLO
from django.shortcuts import render
from django.http import HttpResponse
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx import Document
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from docx import Document
from docx.shared import Pt
import openpyxl
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
import requests
from rest_framework import status
import boto3
from botocore.exceptions import NoCredentialsError
from io import BytesIO
from datetime import datetime
import pytz
import datetime
from docx2pdf import convert
from docx.shared import Inches
import os
import re




class Cindata(APIView):
    
    def get(self, request, cin, format=None):
        try:
            if not cin:
                return Response({"error": "CIN is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            url = f"https://api.finanvo.in/company/profile?CIN={cin}"
            headers = {
                "Host": "api.finanvo.in",
                "App-Origin": "https://web.compdata.in",
                "Origin": "https://web.compdata.in",
                "Referer": "https://web.compdata.in/",
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return JsonResponse(response.json(), status=status.HTTP_200_OK)
            else:
                return JsonResponse({"error": f"Request failed with status code: {response.status_code}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def Cindata(request, cin):
    if request.method == 'GET':
        try:
            if not cin:
                return Response({"error": "CIN is required"}, status=status.HTTP_400_BAD_REQUEST)

            url = f"https://api.finanvo.in/company/profile?CIN={cin}"
            headers = {
                "Host": "api.finanvo.in",
                "App-Origin": "https://web.compdata.in",
                "Origin": "https://web.compdata.in",
                "Referer": "https://web.compdata.in/",
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return JsonResponse(response.json(), status=status.HTTP_200_OK)
            else:
                return JsonResponse({"error": f"Request failed with status code: {response.status_code}"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=400)
