from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# import requests
# import hashlib
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
# import json
import requests
from bs4 import BeautifulSoup
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
import re
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import cryptography
import binascii
import datetime
from cryptography.hazmat.primitives import hashes
import urllib.parse
import hashlib
from anticaptchaofficial.recaptchav2proxyless import *

solver = recaptchaV2Proxyless()
solver.set_verbose(1)
solver.set_key("ca26cd3e970e7ca9809ff03c2bb771ab")
solver.set_website_url("https://www.startupindia.gov.in/")
solver.set_website_key("6Ld112UUAAAAAITPMregPN1avoXBSMtFeOfra0_r")

solver.set_is_invisible(True)
solver.set_soft_id(0)


def upload_image(image_file_path):
    url = 'https://api.startupindia.gov.in/sih/api/file/user/image/Startup'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Origin': 'https://www.startupindia.gov.in',
        'Referer': 'https://www.startupindia.gov.in/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Te': 'trailers',
    }

    response = requests.get(image_file_path)

    files = {'file': ('Stay Whizzy.png', response.content, 'image/png')}  # Update the filename

    response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        print("Image uploaded successfully!")
        data = json.loads(response.text)
        name = data['name']
        return name  # Return the 'name' variable
    else:
        print(f"Failed to upload the image. Status code: {response.status_code}")

@csrf_exempt
def stratup_login(request):
    data = json.loads(request.body)
    username = data["general"]["username"]
    password = data["general"]["password"]
    url = "https://api.startupindia.gov.in/sih/api/noauth/sihLogin/auth"

    headers = {
        "Host": "api.startupindia.gov.in",
        "Content-Length": "695",
        "Sec-Ch-Ua": "",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36",
        "Sec-Ch-Ua-Platform": "\"\"",
        "Origin": "https://www.startupindia.gov.in",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.startupindia.gov.in/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9"
    }
    g_response = solver.solve_and_return_solution()
    data = {
        "username": username,
        "password": password,
        "grantType": "PASSWORD",
        "captchaResponse": g_response
    }
    response = requests.post(url, headers=headers, json=data)
    # print(response.text)
    data = json.loads(response.text)
    # Extract the value of 'token' key
    print(data['token'])
    request.session['auth_token'] = data['token']
    return HttpResponse(data['token'])

def application_save(payload,auth_token):
    url = 'https://api.startupindia.gov.in/sih/api/auth/dpiit/services/application/save'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/json',
        'X-Auth-Token': f'{auth_token}'
    }
    response = requests.post(url, headers=headers, json=payload)

# Check the response
    if response.status_code == 200:
        print("Form submitted successfully!")
        return response.json()
    else:
        print(f"Failed to submit the form. Status code: {response.status_code}")
        return None


def automate_form_fill(payload):
    url = "https://api.startupindia.gov.in/sih/api/auth/user/update/startup"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/json",
        "X-Auth-Token": "eyJhbGciOiJIUzUxMiIsInppcCI6IkRFRiJ9.eNp8zjGOwjAQBdC7TI1WTuIYO9WegGbLFcXYmYCRgyN7jFZC3H0HiYKK8n-9Gf07XDjCBEaH3pBH0l4Fra0ha6VxsANss4BDLismibV5iae2MSqlbljqGb9PK8b0FfIqICLD1BmnrBq7Qe-A_rZXoe3wLFqlAtMdtuZTrGeS_1wayel1bpVLpArTL4yLtoHGpUfnvTJjmBfs9oOCo6ygwLl8YK5_spQDcsxXWfxi7o25xfdaFpecSMQPY-G2wePxDwAA__8.AZY5vbY9HQ1u0s7lee1eq-YUrIKmeAmpeADKFj1eA2soTAh3XUS8sqsRz3WHXv69jjXj2FFUfeHzc4jIglYBLQ",
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Check if the request was successful
        print("Form submitted successfully!")
        print("Response:")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to submit the form: {e}")


@csrf_exempt
def startup(request):
    if request.method == "POST":
        dt = request.body
        data = json.loads(dt)
        auth_token = request.session.get('auth_token')

        # print(auth_token)
        name = upload_image(data['image_path'])
        print(name)
        payload = {
            "incorporationNumber": data["general"]['incorporationNumber'],
            "startupEntity": {
                "startupNatureOfEntity": {"id": data["general"]['startupNatureOfEntity']},
                "startupIndustry": {"id": data["general"]['startupIndustry']},
                "startupSection": {"id": data["general"]['startupSection']},
                "startupServices": [{"id": data["general"]['startupServices']}],
                "name": data["general"]['name'],
                "incorporationDate": data["general"]['incorporationDate'],
                "panNumber": data["general"]['panNumber']
            },
            "recognitionDetailType": data["general"]['recognitionDetailType'],
            "status": data["general"]['status']
        }
        

        resp = application_save(payload,auth_token)
        payload = {
            "incorporationNumber": data["general"]['incorporationNumber'],
            "startupEntity": {
                "startupNatureOfEntity": {"id": data["general"]['startupNatureOfEntity']},
                "startupIndustry": {"id": data["general"]['startupIndustry']},
                "startupSection": {"id": data["general"]['startupSection']},
                "startupServices": [{"id": data["general"]['startupServices']}],
                "name": data["general"]['name'],
                "incorporationDate": data["general"]['incorporationDate'],
                "panNumber": data["general"]['panNumber']
            },
            "recognitionDetailType": data['recognitionDetailType_address']['type'],
            "status": data['recognitionDetailType_address']['status'],
            "address": {
                "address1": data['recognitionDetailType_address']['address1'],
                "address2": data['recognitionDetailType_address']['address2'],
                "address3": data['recognitionDetailType_address']['address3'],
                "city": data['recognitionDetailType_address']['city'],
                "stateId": data['recognitionDetailType_address']['stateId'],
                "stateName": data['recognitionDetailType_address']['stateName'],
                "pinCode": data['recognitionDetailType_address']['pinCode'],
                "districtId": data['recognitionDetailType_address']['districtId'],
                "districtName": data['recognitionDetailType_address']['districtName'],
                "subDistrictId": data['recognitionDetailType_address']['subDistrictId'],
                "subDistrictName": data['recognitionDetailType_address']['subDistrictName']
            }
        }




        resp = application_save(payload,auth_token)
        payload = {
            "incorporationNumber": data['general']['incorporationNumber'],
            "startupEntity": {
                "startupNatureOfEntity": {"id": data['general']['startupNatureOfEntity']},
                "startupIndustry": {"id": data['general']['startupIndustry']},
                "startupSection": {"id": data['general']['startupSection']},
                "startupServices": [{"id": data['general']['startupServices']}],
                "name": data['general']['name'],
                "incorporationDate": data['general']['incorporationDate'],
                "panNumber": data['general']['panNumber']
            },
            "recognitionDetailType": data['recognitionDetailType_address']['type2'],
            "status": data['recognitionDetailType_address']['status'],
            "address": {
                "address1": data['recognitionDetailType_address']['address1'],
                "address2": data['recognitionDetailType_address']['address2'],
                "address3": data['recognitionDetailType_address']['address3'],
                "city": data['recognitionDetailType_address']['city'],
                "stateId": data['recognitionDetailType_address']['stateId'],
                "stateName": data['recognitionDetailType_address']['stateName'],
                "pinCode": data['recognitionDetailType_address']['pinCode'],
                "districtId": data['recognitionDetailType_address']['districtId'],
                "districtName": data['recognitionDetailType_address']['districtName'],
                "subDistrictId": data['recognitionDetailType_address']['subDistrictId'],
                "subDistrictName": data['recognitionDetailType_address']['subDistrictName']
            },
            "representative": {
                "name": data['general']['name'],
                "designation": data['representative']['designation'],
                "mobile": data['representative']['mobile'],
                "email": data['representative']['email']
            },
            "directors": [
                {
                    "directorCin": data['director1']['directorCin'],
                    "name": data['director1']['name'],
                    "gender": data['director1']['gender'],
                    "mobilePrefix": data['director1']['mobilePrefix'],
                    "mobileNumber": data['director1']['mobileNumber'],
                    "address": data['director1']['address'],
                    "email": data['director1']['email']
                },
                {
                    "directorCin": data['director2']['directorCin'],
                    "name": data['director2']['name'],
                    "gender": data['director2']['gender'],
                    "mobilePrefix": data['director2']['mobilePrefix'],
                    "mobileNumber": data['director2']['mobileNumber'],
                    "address": data['director2']['address'],
                    "email": data['director2']['email']
                }
            ],
            "activities": {
                "problemStatement": data['activities']['problemStatement'],
                "problemSolution": data['activities']['problemSolution'],
                "solutionUniqueness":data['activities']['solutionUniqueness'] ,
                "generateRevenue": data['activities']['generateRevenue']
            },
            "additionalInformation": {
                "numberOfEmployees": data['additionalInformation']['numberOfEmployees'],
                "stage": data['additionalInformation']['stage'],
                "ipr": data['additionalInformation']['ipr'] ,
                "workCategory":data['additionalInformation']['workCategory'] ,
                "scalableBusinessModel": data['additionalInformation']['scalableBusinessModel'],
                "receiveFunding": data['additionalInformation']['receiveFunding'],
                "iprs": [
                    {
                        "applicationNumber": data['additionalInformation']['iprs']['applicationNumber1']['number'],
                        "iprTitle": data['additionalInformation']['iprs']['applicationNumber1']['iprTitle'],
                        "applied": data['additionalInformation']['iprs']['applicationNumber1']['applied'] ,
                        "registered": data['additionalInformation']['iprs']['applicationNumber1']['registered']
                    },
                    {
                        "applicationNumber": data['additionalInformation']['iprs']['applicationNumber2']['number'],
                        "iprTitle": data['additionalInformation']['iprs']['applicationNumber2']['iprTitle'],
                        "applied": data['additionalInformation']['iprs']['applicationNumber2']['applied'] ,
                        "registered": data['additionalInformation']['iprs']['applicationNumber2']['registered']
                    },
                    {
                    "applicationNumber": data['additionalInformation']['iprs']['applicationNumber3']['number'],
                        "iprTitle": data['additionalInformation']['iprs']['applicationNumber3']['iprTitle'],
                        "applied": data['additionalInformation']['iprs']['applicationNumber3']['applied'] ,
                        "registered": data['additionalInformation']['iprs']['applicationNumber3']['registered']
                    },
                    {
                        "applicationNumber": data['additionalInformation']['iprs']['applicationNumber4']['number'],
                        "iprTitle": data['additionalInformation']['iprs']['applicationNumber4']['iprTitle'],
                        "applied": data['additionalInformation']['iprs']['applicationNumber4']['applied'] ,
                        "registered": data['additionalInformation']['iprs']['applicationNumber4']['registered']
                },
                    {
                        "applicationNumber": data['additionalInformation']['iprs']['applicationNumber5']['number'],
                        "iprTitle": data['additionalInformation']['iprs']['applicationNumber5']['iprTitle'],
                        "applied": data['additionalInformation']['iprs']['applicationNumber5']['applied'] ,
                        "registered": data['additionalInformation']['iprs']['applicationNumber5']['registered']
                    }
                ],
                "workCategories": [],
                "fundingProof": {},
                "businessModel": {
                "wealthCreation": data['businessModel']['wealthCreation'],
                "note": data['businessModel']['note']
                }
            }
        }


        resp = application_save(payload,auth_token)

        request.session['image'] = name
        return HttpResponse(resp,name)
    
@csrf_exempt
def form_submit(request):
    if request.method == "POST":
        name_variable = request.session.get(['image'])

        data = json.loads(request.body)
        payload = {
            "name": data['finalpayload']['name'],
            "uid": data['finalpayload']['uid'],
            "email": data['finalpayload']['email'],
            "phone": data['finalpayload']['phone'],
            "image": f"{name_variable}",
            #"uniqueId": "64b51967e4b0c4486e86762e",
            "startup": {
                "name": data['finalpayload']['startup']['name'],
                "funded": data['finalpayload']['startup']['funded'],
                "stage": data['finalpayload']['startup']['stage'],
                "ideaBrief": data['finalpayload']['startup']['ideaBrief'],
                "state": get_country_id(data['finalpayload']['startup']['country']),  # Replace with the desired country name
                "phone": data['finalpayload']['startup']['phone'],
                "city": get_city_id(data['finalpayload']['startup']['city']),  # Replace with the desired city name
                "startupindustry": data['finalpayload']['startup']['startupindustry'],
                "services": [data['finalpayload']['startup']['services']],
                "sector": data['finalpayload']['startup']['sector'],
                "addAll":  data['finalpayload']['startup']['addAll'],
                "lookingToConnectTo": [data['finalpayload']['startup']['lookingToConnectTo']['name1'], data['finalpayload']['startup']['lookingToConnectTo']['name2'], data['finalpayload']['startup']['lookingToConnectTo']['name3'], data['finalpayload']['startup']['lookingToConnectTo']['name4'], data['finalpayload']['startup']['lookingToConnectTo']['name5']],
                "description": data['finalpayload']['startup']['description'],
                "location": {
                    "country": {"id": get_country_id(data['finalpayload']['startup']['country'])},  # Replace with the desired country name
                    "state": {"id": get_country_id(data['finalpayload']['startup']['country'])},  # Replace with the desired state name
                    "city": {"id": get_city_id(data['finalpayload']['startup']['city'])},  # Replace with the desired city name
                },
                "startupEntity": data['finalpayload']['startup']['startupEntity'],
                "dippCertified": data['finalpayload']['startup']['dippCertified'],        "members": [],
                "businessPlan": data['finalpayload']['startup']['businessPlan'],
                "mobileAppLink": data['finalpayload']['startup']['mobileAppLink'],
                "focusArea": {
                    "industry": {"id": data['finalpayload']['startup']['focusarea']['industry']},
                    "sectors": [{"id": data['finalpayload']['startup']['focusarea']['sectors']}],
                },
                "mentorshipParticipant":data['finalpayload']['startup']['mentorshipParticipant'],
                "mentorship": {"mentorMeans": []},
            },
            "oldEmail": data['finalpayload']['oldemail']
        }
        response = automate_form_fill(payload)
        return HttpResponse(response)



def get_country_id(country_name):
    countries = {
    "Argentina": "5f48d0c92a9bb065cdfc43f0",
    "Austria": "5f48d0c92a9bb065cdfc43fe",
    "Australia": "5f48d0c92a9bb065cdfc4402",
    "Brazil": "5f48d0c92a9bb065cdfc43ef",
    "Bhutan": "5f29a899f883f92b03227cd9",
    "Canada": "5f48d0c92a9bb065cdfc43ee",
    "China": "5f48d0c92a9bb065cdfc43f6",
    "Denmark": "5f48d0c92a9bb065cdfc43fd",
    "Finland": "5f02e38c6f3de87babe20cd9",
    "Bahrain": "5f48d0c92a9bb065cdfc4404",
    "Germany": "5f02e38c6f3de87babe20cd8",
    "Hong Kong": "5f48d0c92a9bb065cdfc43f2",
    "Indonesia": "5f48d0c92a9bb065cdfc43f4",
    "Ireland": "5f48d0c92a9bb065cdfc4400",
    "Italy": "5f48d0c92a9bb065cdfc43fc",
    "Japan": "5f02e38c6f3de87babe20cdc",
    "Netherlands": "5f02e38c6f3de87babe20cda",
    "Israel": "5f02e38c6f3de87babe20cd3",
    "Malaysia": "5f48d0c92a9bb065cdfc43f3",
    "India": "5f02e38c6f3de87babe20cd2",
    "France": "5f48d0c92a9bb065cdfc43fb",
    "Russia": "5f02e38c6f3de87babe20cdd",
    "Portugal": "5ef99f79e151c732272cad93",
    "Switzerland": "5f48d0c92a9bb065cdfc43ff",
    "South Korea": "5f02e38c6f3de87babe20cdb",
    "Thailand": "5f239fa322502845250dd426",
    "Sri Lanka": "5f48d0c92a9bb065cdfc43f7",
    "USA": "5f02e38c6f3de87babe20cd6",
    "UAE": "5f48d0c92a9bb065cdfc4403",
    "United Kingdom": "5f48d0c92a9bb065cdfc43fa",
    "Vietnam": "5f239e4722502845250dd423",
    "Taiwan": "5f48d0c92a9bb065cdfc43f1",
    "South Africa": "5f48d0c92a9bb065cdfc4405",
    "Singapore": "5f02e38c6f3de87babe20cd5",
    "Spain": "5f02e38c6f3de87babe20cd7",
    "Sweden": "5f02e38c6f3de87babe20cd4",
    "Norway": "5f48d0c92a9bb065cdfc4401",
    "Mexico": "60657cdb6804a9394f8fb67d",
    "Chile": "60657f04be15641e4cd35aa9",
    "Colombia": "60657f356804a9394f8fb692",
    "Bangladesh": "60657f68805fa03767541308",
    "Myanmar": "6065b56d805fa03767541606",
    "Kazakhstan": "6065b5ba805fa0376754160d",
    "Kyrgyzstan": "6065b5eb805fa03767541612",
    "Tajikistan": "6065b60dbe15641e4cd35dd6",
    "Uzbekistan": "6065b6266804a9394f8fb9b6",
    "Belgium": "6065b6446804a9394f8fb9b7",
    "Bulgaria": "6065b65e805fa0376754161d",
    "Croatia": "6065b675805fa0376754161e",
    "Cyprus": "6065b68dbe15641e4cd35ddd",
    "Czech Republic": "6065b6ad6804a9394f8fb9be",
    "Estonia": "6065b6d56804a9394f8fb9bf",
    "Greece": "6065b70f6804a9394f8fb9c2",
    "Hungary": "6065b72f6804a9394f8fb9c3",
    "Latvia": "6065b7546804a9394f8fb9c4",
    "Lithuania": "6065b76e805fa0376754162f",
    "Luxembourg": "6065b782be15641e4cd35de8",
    "Malta": "6065b7be6804a9394f8fb9c5",
    "Poland": "6065b7e5805fa03767541638",
    "Romania": "6065b804be15641e4cd35deb",
    "Slovakia": "6065b87c6804a9394f8fb9cb",
    "Slovenia": "6065b89b805fa0376754163d",
    "Republic of Korea": "6065ba736804a9394f8fb9e3",
    "Turkey": "6065bad0be15641e4cd35e06",
    "Republic of South Africa": "6065bb1e6804a9394f8fb9ec",
    "Saudi Arabia": "6065bb34805fa03767541650",
    "Others": "64b7bf8a5d4c4b6466edaf69"
    }
    return countries.get(country_name)

def get_city_id(city_name):
    cities = {
  "Adyar": "5f48d0c92a9bb065cdfc454c",
  "Afzalpur": "5f48d0c92a9bb065cdfc453b",
  "Arsikere": "5f48d0c92a9bb065cdfc4518",
  "Athni": "5f48d0c92a9bb065cdfc451d",
  "Bagalkot": "5f48ce5a2a9bb065cdf9fd4e",
  "Bagalkote": "5f89b9b161334048016290e0",
  "Ballari": "5f48ce5a2a9bb065cdf9fd52",
  "Belagavi": "5f48ce5a2a9bb065cdf9fd51",
  "Bengaluru": "5f48d0c92a9bb065cdfc4507",
  "Bengaluru Rural": "5f48ce5a2a9bb065cdf9fd50",
  "Bengaluru Urban": "5f48ce5a2a9bb065cdf9fd4f",
  "Bidar": "5f48ce5a2a9bb065cdf9fd53",
  "Chamarajanagar": "5f48ce5a2a9bb065cdf9fd55",
  "Chikballapur": "5f48ce5a2a9bb065cdf9fdb8",
  "Chikkaballapur": "5f89b9b161334048016290e1",
  "Chikkamagaluru": "5f48ce5a2a9bb065cdf9fd56",
  "Chitradurga": "5f48ce5a2a9bb065cdf9fd57",
  "Dakshina Kannada": "5f48ce5a2a9bb065cdf9fd58",
  "Davanagere": "5f48d0c92a9bb065cdfc450a",
  "Dharwad": "5f48ce5a2a9bb065cdf9fd5a",
  "Gadag": "5f48ce5a2a9bb065cdf9fd5b",
  "Gokak": "5f48d0c92a9bb065cdfc4512",
  "Gulbarga": "5f89b9b161334048016290e2",
  "Hassan": "5f48ce5a2a9bb065cdf9fd5d",
  "Haveri": "5f48ce5a2a9bb065cdf9fd5e",
  "Hubli-Dharwad": "5f48d0c92a9bb065cdfc4508",
  "Kalaburagi": "5f48ce5a2a9bb065cdf9fd5c",
  "Karwar": "5f48d0c92a9bb065cdfc450e",
  "Kodagu": "5f48ce5a2a9bb065cdf9fd5f",
  "Kolar": "5f48ce5a2a9bb065cdf9fd60",
  "Koppal": "5f48ce5a2a9bb065cdf9fd61",
  "Lakshmeshwar": "5f48d0c92a9bb065cdfc4528",
  "Lingsugur": "5f48d0c92a9bb065cdfc452e",
  "Maddur": "5f48d0c92a9bb065cdfc453c",
  "Madhugiri": "5f48d0c92a9bb065cdfc453d",
  "Madikeri": "5f48d0c92a9bb065cdfc4530",
  "Magadi": "5f48d0c92a9bb065cdfc4541",
  "Mahalingapura": "5f48d0c92a9bb065cdfc4534",
  "Malavalli": "5f48d0c92a9bb065cdfc452c",
  "Malur": "5f48d0c92a9bb065cdfc4538",
  "Mandya": "5f48ce5a2a9bb065cdf9fd62",
  "Mangaluru": "5f48d0c92a9bb065cdfc4509",
  "Manvi": "5f48d0c92a9bb065cdfc4526",
  "Mudabidri": "5f48d0c92a9bb065cdfc4540",
  "Mudalagi": "5f48d0c92a9bb065cdfc4535",
  "Muddebihal": "5f48d0c92a9bb065cdfc4536",
  "Mudhol": "5f48d0c92a9bb065cdfc4521",
  "Mulbagal": "5f48d0c92a9bb065cdfc451e",
  "Mundargi": "5f48d0c92a9bb065cdfc4549",
  "Mysuru": "5f48ce5a2a9bb065cdf9fd63",
  "Nanjangud": "5f48d0c92a9bb065cdfc4519",
  "Nargund": "5f48d0c92a9bb065cdfc452a",
  "Navalgund": "5f48d0c92a9bb065cdfc4542",
  "Nelamangala": "5f48d0c92a9bb065cdfc4527",
  "Pavagada": "5f48d0c92a9bb065cdfc4537",
  "Piriyapatna": "5f48d0c92a9bb065cdfc454b",
  "Puttur": "5f48d0c92a9bb065cdfc451c",
  "Raayachuru": "5f48d0c92a9bb065cdfc450c",
  "Rabkavi Banhatti": "5f48d0c92a9bb065cdfc4513",
  "Raichur": "5f48ce5a2a9bb065cdf9fd64",
  "Ramanagaram": "5f48d0c92a9bb065cdfc4511",
  "Ramdurg": "5f48d0c92a9bb065cdfc4529",
  "Ranebennur": "5f48d0c92a9bb065cdfc450f",
  "Ranebennuru": "5f89b9b161334048016290dc",
  "Ranibennur": "5f89b9b161334048016290dd",
  "Robertson Pet": "5f48d0c92a9bb065cdfc450d",
  "Ron": "5f48d0c92a9bb065cdfc4548",
  "Sadalagi": "5f48d0c92a9bb065cdfc454a",
  "Sagara": "5f48d0c92a9bb065cdfc451a",
  "Sakaleshapura": "5f48d0c92a9bb065cdfc4546",
  "Sanduru": "5f48d0c92a9bb065cdfc453a",
  "Sankeshwara": "5f48d0c92a9bb065cdfc452f",
  "Saundatti-Yellamma": "5f48d0c92a9bb065cdfc4524",
  "Savanur": "5f48d0c92a9bb065cdfc452d",
  "Sedam": "5f48d0c92a9bb065cdfc4532",
  "Shahabad": "5f48d0c92a9bb065cdfc4514",
  "Shahpur": "5f48d0c92a9bb065cdfc4523",
  "Shiggaon": "5f48d0c92a9bb065cdfc4543",
  "Shikaripur": "5f48d0c92a9bb065cdfc4533",
  "Shivamogga": "5f48ce5a2a9bb065cdf9fd65",
  "Shrirangapattana": "5f48d0c92a9bb065cdfc4544",
  "Sidlaghatta": "5f48d0c92a9bb065cdfc4522",
  "Sindagi": "5f48d0c92a9bb065cdfc4545",
  "Sindhnur": "5f48d0c92a9bb065cdfc4516",
  "Sira": "5f48d0c92a9bb065cdfc451b",
  "Sirsi": "5f48d0c92a9bb065cdfc4515",
  "Siruguppa": "5f48d0c92a9bb065cdfc4520",
  "Srinivaspur": "5f48d0c92a9bb065cdfc4547",
  "Surapura": "5f48d0c92a9bb065cdfc451f",
  "Talikota": "5f48d0c92a9bb065cdfc4531",
  "Tarikere": "5f48d0c92a9bb065cdfc452b",
  "Tekkalakote": "5f48d0c92a9bb065cdfc453e",
  "Terdal": "5f48d0c92a9bb065cdfc453f",
  "Tiptur": "5f48d0c92a9bb065cdfc4517",
  "Tumakuru": "5f48ce5a2a9bb065cdf9fd66",
  "Udupi": "5f48ce5a2a9bb065cdf9fd67",
  "Uttara Kannada": "5f48ce5a2a9bb065cdf9fd68",
  "Vijayapura": "5f48ce5a2a9bb065cdf9fd54",
  "Wadi": "5f48d0c92a9bb065cdfc4525",
  "Yadgir": "5f48ce5a2a9bb065cdf9fdbd"
}
    return cities.get(city_name)