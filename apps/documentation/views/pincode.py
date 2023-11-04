from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import requests
import json
import urllib.parse
from django.http import HttpResponseBadRequest
from django.conf import settings
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

@csrf_exempt
def PincodeinfoView(request, pincode):
            if request.method == 'GET':
              # Get the pincode from the URL parameter
                if not pincode:
                    return HttpResponseBadRequest("Missing 'pincode' parameter")

                print(f"Received pincode: {pincode}")

                url = "https://www.mca.gov.in/bin/mca/login"

                headers = {
                    "Origin": "www.mca.gov.in",
                    "Content-Length": "235",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Accept": "/",
                    "X-Requested-With": "XMLHttpRequest",
                    "Sec-Ch-Ua-Platform": "Windows"
                }

                data = "data=Ut8pBOc0RSM6iYqffqN1ovf7bobPRWJxrpoJRNCmK3GGtEoRKl3FZEf8xy36Iw3GHkoeOLH2Iw8tFFM6yB%2F6gZ4FgTyvicwoT%2FfDKJjUEuk9iiwbfqGT4bPey9LVPXwmJrnHl2AVXwPwjTY7BjtpUZ7CCRrYzb8G8Hs%2FTqLxp0oBRcfBtzGPnIVN9fMdkw%2Fj%2FSvMTL%2FNk05TbSN%2FPlQW%2FgdaTJRMuzmlIKp26ixHs8k%3D"
                response = requests.post(url, headers=headers, data=data)
                set_cookie_value = response.headers.get('Set-Cookie')
                start_index = set_cookie_value.find("session-token=") + len("session-token=")
                end_index = set_cookie_value.find(";", start_index)
                session_token = set_cookie_value[start_index:end_index]
                url = 'https://www.mca.gov.in/content/forms/af/mca-aem-forms/form-fillip/fillip-main-form/form-fillip/jcr:content/guideContainer.af.dermis'

                headers = {
                    'Host': 'www.mca.gov.in',
                    'Cookie': f'cookiesession1=678B2869144E6B476733B93A4104896E; deviceId=4d23ogqkdbe; alertPopup=true; session-token{session_token}',
                    'Content-Length': '544',
                    'Sec-Ch-Ua': '',
                    'Sec-Ch-Ua-Mobile': '?0',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Accept': 'text/plain, /; q=0.01',
                    'Csrf-Token': 'undefined',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Sec-Ch-Ua-Platform': "",
                    'Origin': 'https://www.mca.gov.in',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Referer': 'https://www.mca.gov.in/content/mca/global/en/mca/llp-e-filling/Fillip.html',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9'
                }

                payload = {
                    'functionToExecute': 'invokeFDMOperation',
                    'formDataModelId': '/content/dam/formsanddocuments-fdm/mca-aem-forms/common-service/common-pin-info',
                    "input": f'{{"Model0":{{"value":"{pincode}"}}}}',
                    'operationName': 'POST /bin/mca-gov/commonpincode',
                    'guideNodePath': '/content/forms/af/mca-aem-forms/form-fillip/fillip-main-form/block2/jcr:content/guideContainer/rootPanel/items/panel_1379931518_cop/items/panel/items/panel/items/panel_702814714/items/panel/items/guidetextbox_copy_11_1386963699'
                }

                response = requests.post(url, headers=headers, data=payload)

                response_dict = json.loads(response.text)
                return JsonResponse(response_dict)