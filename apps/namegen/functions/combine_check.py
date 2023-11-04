import requests
import json
import urllib.parse
from requests_toolbelt.multipart.encoder import MultipartEncoder
from django.conf import settings
# Session token extraction from response headers
def get_session_token(response):
    set_cookie_value = response.headers.get('Set-Cookie')
    start_index = set_cookie_value.find("session-token=") + len("session-token=")
    end_index = set_cookie_value.find(";", start_index)
    session_token = set_cookie_value[start_index:end_index]
    return session_token

def fetch_session_token():
    url = "https://www.mca.gov.in/bin/mca/login"
    headers = {
        "Origin": "www.mca.gov.in",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" }
    data=settings.MCA_LOGIN_PASS_HASH
    response = requests.post(url, headers=headers, data=data)
    return get_session_token(response)

def check_llp_name(c_name, session_token):
    # Construct the payload for LLP
    payload_llp = r'''{"requestBody":{"formData":{"purpose":"New Incorporation","proposedname1":"ZIZZAGGGGG LLP","formIntegrationId":"1686922988308_FOUSER","NICcode1":"98200","NICCode1Desc":"Undifferentiated service-producing activities of private households for own use","NICcode2":"98100","NICCode2Desc":"Undifferentiated goods-producing activities of private households for own use","NICcode3":"","NICCode3Desc":"","formAttachment":[]},"formDescription":"RUN LLP","formName":"RUN LLP","formVersion":"1.1","userId":"BIPULKUMARSINGH6690@GMAIL.COM","integrationId":"1686922988308_FOUSER","status":"Draft/Pending Submission"}}'''
    payload_llp_json = json.loads(payload_llp)
    payload_llp_json['requestBody']['formData']['proposedname1'] = c_name
    payload_llp_json = json.dumps(payload_llp_json)
    url_llp = "https://www.mca.gov.in/bin/mca-gov/RunLLPSaveSubmit"

    headers_llp = {
        "Host": "www.mca.gov.in",
        "Cookie": f"cookiesession1=678B28695C218253C321286001478935; alertPopup=true; session-token={session_token}",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary0AN6dHNNjREqqUBN",
        "Origin": "https://www.mca.gov.in",
        "Referer": "https://www.mca.gov.in/content/mca/global/en/mca/llp-e-filling/run-llp.html",
    }

    multipart_data_llp = MultipartEncoder(fields={
        'data': (None, payload_llp_json),
        'action': (None, 'savesubmit'),
        'operation': (None, 'Submit'),
        'serveAction': (None, 'validateform')
    })

    headers_llp['Content-Type'] = multipart_data_llp.content_type

    response_llp = requests.post(url_llp, headers=headers_llp, data=multipart_data_llp)
    result_llp = response_llp.json()
    alert_list_llp = result_llp['validationResponse']['validationresposeBody']
    all_empty_llp = all(not item['alertDescription'] for item in alert_list_llp)
    return all_empty_llp

def check_private_limited_name(c_name, session_token):
    formData = "%7B%22formData%22%3A%7B%22companyType%22%3A%22New+Company+(Others)%22%2C%22companyClass%22%3A%22Private%22%2C%22companyCategory%22%3A%22Company+limited+by+shares%22%2C%22companySubCategory%22%3A%22Non-government+company%22%2C%22proposedName1%22%3A%22DUMBMET+PRIVATE+LIMITED%22%2C%22NICCode1%22%3A%2298200%22%2C%22Description1%22%3A%22Undifferentiated+service-producing+activities+of+private+households+for+own+use%22%2C%22NICCode2%22%3A%2298100%22%2C%22Description2%22%3A%22Undifferentiated+goods-producing+activities+of+private+households+for+own+use%22%2C%22formIntegrationId%22%3A%221%22%2C%22continueFlag%22%3A%22N%22%2C%22LLPIN%22%3A%22%22%2C%22NICCode3%22%3A%22%22%2C%22Description3%22%3A%22%22%2C%22proposedName2%22%3A%22%22%7D%2C%22formDescription%22%3A%22SPICE+PART+A%22%2C%22formName%22%3A%22Spice%2B+Part+A%22%2C%22formVersion%22%3A%221%22%2C%22userId%22%3A%22BIPULKUMARSINGH6690%40GMAIL.COM%22%2C%22integrationId%22%3A%221%22%2C%22prefill%22%3A%22false%22%2C%22status%22%3A%22Draft%2FPending+Submission%22%2C%22operation%22%3A%22Save%22%2C%22referenceNumber%22%3A%22%22%2C%22srn%22%3A%22%22%2C%22formId%22%3A%22%22%2C%22Approvedname%22%3A%22%22%2C%22serveAction%22%3A%22autocheck%22%7D"

    # Manually parse the data
    decoded_data = urllib.parse.unquote_plus(formData,encoding='utf-8')
    data_start = decoded_data.find('{')
    data_end = decoded_data.rfind('}') + 1
    data_str = decoded_data[data_start:data_end]
    data = eval(data_str)
    data['formData']['proposedName1'] = c_name
    encoded_data = urllib.parse.quote_plus(json.dumps(data), encoding='utf-8').replace('%20', '').replace('%28','(').replace('%29',')').replace('+%','%')
    url = "https://www.mca.gov.in/bin/mca-gov/newSpiceA"

    headers = {
        "Host": "www.mca.gov.in",
        "Cookie": f"cookiesession1=678B28695C218253C321286001478935; alertPopup=true; session-token={session_token}; deviceId=1uytaas0tlbi",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.mca.gov.in",
        "Referer": "https://www.mca.gov.in/content/mca/global/en/mca/e-filing/incorporation/spice.html",
    }

    payload = f"formData={encoded_data}"
    response = requests.post(url, headers=headers, data=payload)
    result = response.json()
    alert_list = result['validationResponse']['validationresposeBody']
    all_empty = all(not item['alertDescription'] for item in alert_list)
    return all_empty
def check_name_availability(name, suffix, session_token):
    if suffix == "1":
        full_name = f"{name} LLP"
        if check_llp_name(full_name, session_token):
            return full_name
    elif suffix == "2":
        full_name = f"{name} PRIVATE LIMITED"
        if check_private_limited_name(full_name, session_token):
            return full_name

    return None
