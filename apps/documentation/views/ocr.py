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

class DetectObjectsAndTextView(View):


    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body)
            image_url = data.get('imageurl', '')

            if not image_url:
                return JsonResponse({'error': 'Image URL not provided'}, status=400)

            reader = Reader(['en'])
            model = YOLO('D:/office/spice backend/django backend/CompanyAvailabilityProject/companyavailabilityapp/best.pt')  # Update with the actual path to your YOLO model checkpoint

            t = model.predict(image_url, save=True, imgsz=640, conf=0.1, save_txt=True, save_conf=True, show_labels=False)

            img_paths = []
            label_paths = []
            img_name = image_url.split('/')[-1]

            for pred in t:
                labels = pred.names

                img_path = pred.save_dir + '/' + img_name
                label_path = pred.save_dir + '/labels/' + '.'.join(img_name.split('.')[:-1]) + '.txt'

                img_paths.append(img_path)
                label_paths.append(label_path)

            path = io.BytesIO(urllib.request.urlopen(image_url).read())
            detect_list = []

            for x in range(len(img_paths)):
                with open(label_paths[x], 'r') as file:
                    label = file.readlines()
                img = Image.open(path)

                height = img.height
                width = img.width
                detect_dict = {}

                for i in label:
                    value = [float(a) for a in i.split()]
                    sw = int(width * float(value[1] - value[3] / 2))
                    ew = int(width * float(value[1] + value[3] / 2))
                    sh = int(height * float(value[2] - value[4] / 2))
                    eh = int(height * float(value[2] + value[4] / 2))

                    if labels[int(value[0])] not in detect_dict:
                        detect_dict[labels[int(value[0])]] = [[img.crop((sw, sh, ew, eh)), value[5]]]
                    else:
                        detect_dict[labels[int(value[0])]].append([img.crop((sw, sh, ew, eh)), value[5]])

                detect_list.append(detect_dict)

            detect_list1 = [x.copy() for x in detect_list]

            for f, i in enumerate(detect_list):
                for x, y in i.items():
                    tl = []
                    highest_confidence = 0.0
                    best_result = ""

                    for t in y:
                        temp_image_path = tempfile.NamedTemporaryFile(suffix='.jpg').name
                        t[0].save(temp_image_path, format='JPEG')
                        results = reader.readtext(temp_image_path)

                        for detection in results:
                            text = detection[1]
                            confidence = t[1]

                            if confidence > highest_confidence:
                                highest_confidence = confidence
                                best_result = text

                        tl = [best_result, confidence]

                    detect_list1[f][x] = tl

            return JsonResponse(detect_list1, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        

