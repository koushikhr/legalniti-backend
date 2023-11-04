from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
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
import os
import tempfile

def str2rstr_utf8(s):
    return s.encode('utf-8')

def rstr_sha1(s):
    sha1 = hashlib.sha1()
    sha1.update(s)
    return sha1.digest()

def rstr2hex(input_bytes):
    return ''.join(format(byte, '02x') for byte in input_bytes)

def hex_sha1(s):
    return rstr2hex(rstr_sha1(str2rstr_utf8(s)))

def get_view(respon:str):
    soup = BeautifulSoup(respon, 'html.parser')
    viewstate = soup.find('input', {'id': '__VIEWSTATE'})['value']
    viewstategenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
    previouspage = soup.find('input', {'id': '__PREVIOUSPAGE'})['value']
    eventvalidation = soup.find('input', {'id': '__EVENTVALIDATION'})['value']
    return viewstate,viewstategenerator,previouspage,eventvalidation

def request_url(data:dict,cookie=None):
    url="https://ipindiaonline.gov.in//trademarkefiling/user/frmNewRegistration.aspx"
    if cookie is None:
        response=requests.post(url)
        cookies=response.headers['set-cookie'].split(';')[0]+";"+response.headers['set-cookie'].split(';')[-4].split(', ')[1]
        
        return cookies,get_view(response.text)
    else:
        headers = {
                    "Cookie": cookie,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.141 Safari/537.36",
                    "Content-Type": "multipart/form-data",
                    "Sec-Fetch-Dest": "document",
                    "Accept-Encoding": "gzip, deflate",
                }
        multipart_data=MultipartEncoder(fields=data)
        headers["Content-Type"]= multipart_data.content_type
        response=requests.post(url,headers=headers,data=multipart_data)
        return get_view(response.text)
def request_txtcode(data:dict,cookie:str):
    url="https://ipindiaonline.gov.in//trademarkefiling/user/frmNewRegistration.aspx"
    headers = {
                    "Cookie": cookie,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.141 Safari/537.36",
                    "Content-Type": "multipart/form-data",
                    "Sec-Fetch-Dest": "document",
                    "Accept-Encoding": "gzip, deflate",
                }
    multipart_data=MultipartEncoder(fields=data)
    headers["Content-Type"]= multipart_data.content_type
    response=requests.post(url,headers=headers,data=multipart_data)
    soup = BeautifulSoup(response.text, 'html.parser')
    txt_code= soup.find('input', {'id': 'ctl00_ContentPlaceHolder1_txtCode'})['value']
    return txt_code,get_view(response.text)


def cert_data(cert_path:str):

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Get the file name from the URL
    file_name = os.path.join(temp_dir, os.path.basename(cert_path))

    # Send a GET request to the URL
    response = requests.get(cert_path)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the file to the temporary directory
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded and saved as {file_name}")
    else:
        return None
    # Load the X.509 certificate from a .cer file
    with open(file_name, 'rb') as cert_file:
        cert_data = cert_file.read()

    # Parse the certificate using the default backend
    certificate = x509.load_der_x509_certificate(cert_data, default_backend())

    # Extract the RSA public key from the certificate
    public_key = certificate.public_key()

    # If it's an RSA public key, serialize it in DER format
    if isinstance(public_key, cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey):
        rsa_public_key_der = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Convert the DER-encoded public key to a hex string
        hexstring = rsa_public_key_der.hex()

        # Insert a space after every 2 characters in the hex string
        spaced_hexstring = ' '.join(hexstring[i:i+2] for i in range(0, len(hexstring), 2))

        print("Hexstring of RSA Public Key found")
        # print(spaced_hexstring)
    else:
        print("The public key is not an RSA key.")


    


    # Extract the certificate serial number
    serial_number = certificate.serial_number

    # Create an instance of the SHA-1 hash algorithm
    sha1 = hashes.SHA1()

    # Compute the thumbprint (SHA-1 hash) of the certificate
    thumbprint = certificate.fingerprint(sha1)
    thumbprint = binascii.hexlify(thumbprint).decode('utf-8')

    # Extract the certificate expiry date
    expiry_date = certificate.not_valid_after

    # Format the expiry date as "dd/mm/yyyy"
    expiry_date = expiry_date.strftime("%d/%m/%Y")

    # Extract the holder name (subject name)
    holder_name = certificate.subject.rfc4514_string()

    # Extract the issuer name
    issuer_name = certificate.issuer.rfc4514_string()

    return str(serial_number),thumbprint,expiry_date,holder_name,issuer_name, spaced_hexstring

def check_name(data:dict,cookie:str):
    url="https://ipindiaonline.gov.in//trademarkefiling/user/frmNewRegistration.aspx"
    headers = {
                    "Cookie": cookie,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.141 Safari/537.36",
                    "Content-Type": "multipart/form-data",
                    "Sec-Fetch-Dest": "document",
                    "Accept-Encoding": "gzip, deflate",
                }
    multipart_data=MultipartEncoder(fields=data)
    headers["Content-Type"]= multipart_data.content_type
    response=requests.post(url,headers=headers,data=multipart_data)
    soup = BeautifulSoup(response.text, 'html.parser')
    element = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_lblCaptcha', 'class': 'FieldLabel'})

    # Extract the text content from the element
    if element:
        result = element.get_text()
        if not 'exist' in result:
            return result,get_view(response.text)
        else:
            return 'Error'
def submit(data:dict,cookie:str):
    url="https://ipindiaonline.gov.in//trademarkefiling/user/frmNewRegistration.aspx"
    headers = {
                    "Cookie": cookie,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.141 Safari/537.36",
                    "Content-Type": "multipart/form-data",
                    "Sec-Fetch-Dest": "document",
                    "Accept-Encoding": "gzip, deflate",
                }
    multipart_data=MultipartEncoder(fields=data)
    headers["Content-Type"]= multipart_data.content_type
    response=requests.post(url,headers=headers,data=multipart_data)
    return response.text
    # soup = BeautifulSoup(response.text, 'html.parser')
    # element = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_lblCaptcha', 'class': 'FieldLabel'})


@csrf_exempt
def trade(request):
    if request.method == "POST":
        request_data=json.loads(request.body)
        certificate = request_data['certificate']
        legal_status = request_data['legal_status']
        trad_disc = request_data['trad_disc']
        email=request_data['email']
        telephone=request_data['telephone']
        service_address=request_data['service_address']
        propritor_address=request_data['propritor_address']
        propritor_name=request_data['propritor_name']
        name=request_data['name']
        username = name.split(' ')[0] + telephone[-3:]
        password = hex_sha1(request_data['password'])
        cookie,view = request_url({})
        viewstate,viewstategenerator,previouspage,eventvalidation = view
        data1={
            "ctl00_ToolkitScriptManager1_HiddenField":";;AjaxControlToolkit, Version=3.5.40412.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:1547e793-5b7e-48fe-8490-03a375b13a33:475a4ef5:5546a2b:d2e10b12:effe2a26:37e2e5c9:5a682656:bfe70f69:3ac3e789:1d3ed089:497ef277:a43b07eb:751cdd15:dfad98a5:3cf12cf1",
            "__EVENTTARGET":"ctl00$ContentPlaceHolder1$ddlApplicantType",
            "__EVENTARGUMENT":"",
            "__LASTFOCUS":"",
            "__VIEWSTATE":viewstate,
            "__VIEWSTATEGENERATOR":viewstategenerator,
            "__VIEWSTATEENCRYPTED":"",
            "__PREVIOUSPAGE":previouspage,
            "__EVENTVALIDATION":eventvalidation,
            "ctl00$ContentPlaceHolder1$hdnSetPassword":"",
            "ctl00$ContentPlaceHolder1$hdnSetConfirmPassword":"",
            "ctl00$ContentPlaceHolder1$ddlApplicantType":"P",
            "ctl00$ContentPlaceHolder1$txtCode":"",
            "ctl00$ContentPlaceHolder1$RequiredFieldValidator3_ValidatorCalloutExtender_ClientState":"",
            "ctl00$ContentPlaceHolder1$DDLDocType":"BCR"
        }
        viewstate,viewstategenerator,previouspage,eventvalidation =request_url(data1,cookie)
        data1['__EVENTTARGET']="ctl00$ContentPlaceHolder1$lbtnPropSearch"
        data1['__VIEWSTATE']=viewstate
        data1['__EVENTVALIDATION']=eventvalidation
        viewstate,viewstategenerator,previouspage,eventvalidation =request_url(data1,cookie)
        del data1['__LASTFOCUS']
        del data1['ctl00$ContentPlaceHolder1$ddlApplicantType']
        del data1['ctl00$ContentPlaceHolder1$txtCode']
        del data1['ctl00$ContentPlaceHolder1$RequiredFieldValidator3_ValidatorCalloutExtender_ClientState']
        data1['__EVENTTARGET']=""
        data1['__VIEWSTATE']=viewstate
        data1['__EVENTVALIDATION']=eventvalidation
        data1['ctl00$ContentPlaceHolder1$tbsearchtext']=name
        data1['ctl00$ContentPlaceHolder1$btnsubmit']="Submit"
        viewstate,viewstategenerator,previouspage,eventvalidation =request_url(data1,cookie)
        del data1['ctl00$ContentPlaceHolder1$tbsearchtext']
        del data1['ctl00$ContentPlaceHolder1$btnsubmit']
        data1['__LASTFOCUS']=""
        data1['__VIEWSTATE']=viewstate
        data1['__EVENTVALIDATION']=eventvalidation
        data1['ctl00$ContentPlaceHolder1$btnAdd']="Add New"
        viewstate,viewstategenerator,previouspage,eventvalidation =request_url(data1,cookie)
        del data1['__LASTFOCUS']
        del data1['ctl00$ContentPlaceHolder1$btnAdd']
        data1['__EVENTTARGET']="ctl00$ContentPlaceHolder1$chkpropCategory$0"
        data1['__VIEWSTATE']=viewstate
        data1['__EVENTVALIDATION']=eventvalidation
        data1['ctl00$ContentPlaceHolder1$chkpropCategory$0']="on"
        viewstate,viewstategenerator,previouspage,eventvalidation =request_url(data1,cookie)
        del data1["ctl00$ContentPlaceHolder1$chkpropCategory$0"]
        data1['__EVENTTARGET']=""
        data1['__VIEWSTATE']=viewstate
        data1['__EVENTVALIDATION']=eventvalidation
        data1['ctl00$ContentPlaceHolder1$tbpropriatorname']=propritor_name
        data1['ctl00$ContentPlaceHolder1$tbpropriatorAddress']=propritor_address
        data1['ctl00$ContentPlaceHolder1$proprietorNation']="IN"
        data1['ctl00$ContentPlaceHolder1$txtpropserviceadd']=service_address
        data1['ctl00$ContentPlaceHolder1$txtproptelephone']=telephone
        data1['ctl00$ContentPlaceHolder1$txtfax']=""
        data1['ctl00$ContentPlaceHolder1$proprietorEmail']=email
        data1['ctl00$ContentPlaceHolder1$proprietorTradedesc']=trad_disc
        data1['ctl00$ContentPlaceHolder1$proprietorRegdesc']=legal_status
        data1['ctl00$ContentPlaceHolder1$btnpanelButtonSubmit']="Submit"
        txt_code,view = request_txtcode(data1,cookie)
        viewstate,viewstategenerator,previouspage,eventvalidation = view
        data1={
            'ctl00_ToolkitScriptManager1_HiddenField': ';;AjaxControlToolkit, Version=3.5.40412.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:1547e793-5b7e-48fe-8490-03a375b13a33:475a4ef5:5546a2b:d2e10b12:effe2a26:37e2e5c9:5a682656:bfe70f69:3ac3e789:1d3ed089:497ef277:a43b07eb:751cdd15:dfad98a5:3cf12cf1',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            "__VIEWSTATE":viewstate,
            '__VIEWSTATEGENERATOR':viewstategenerator,
            '__VIEWSTATEENCRYPTED':"",
            "__PREVIOUSPAGE":previouspage,
            "__EVENTVALIDATION":eventvalidation,
            'ctl00$ContentPlaceHolder1$hdnSetPassword': '',
            'ctl00$ContentPlaceHolder1$hdnSetConfirmPassword':'',
            'ctl00$ContentPlaceHolder1$ddlApplicantType': 'P',
            'ctl00$ContentPlaceHolder1$RequiredFieldValidator3_ValidatorCalloutExtender_ClientState': '',
            'ctl00$ContentPlaceHolder1$DDLDocType': 'BCR',
            'ctl00$ContentPlaceHolder1$txtCode': str(txt_code),
            'ctl00$ContentPlaceHolder1$btnGetDetails': 'Process',
            'ctl00$ContentPlaceHolder1$AFUAttachments': ''
            }
        viewstate,viewstategenerator,previouspage,eventvalidation =request_url(data1,cookie)
        data1["__EVENTTARGET"] = 'ctl00$ContentPlaceHolder1$rdoregmode$0'
        data1["__VIEWSTATE"]=viewstate
        data1["__VIEWSTATEGENERATOR"] = viewstategenerator
        data1['__PREVIOUSPAGE']=previouspage
        data1["__EVENTVALIDATION"]=eventvalidation
        data1["ctl00$ContentPlaceHolder1$rdoregmode"] = "D"
        data1["ctl00$ContentPlaceHolder1$txtUserID"]=''
        data1["ctl00$ContentPlaceHolder1$txtPassword"] = ''
        data1["ctl00$ContentPlaceHolder1$Hidden1"]=''
        data1["ctl00$ContentPlaceHolder1$Hidden2"]=''
        data1["ctl00$ContentPlaceHolder1$txtPasswordCheck"]=''
        data1["ctl00$ContentPlaceHolder1$CompareValidator1_ValidatorCalloutExtender_ClientState"] = ''
        data1["ctl00$ContentPlaceHolder1$RequiredFieldValidator2_ValidatorCalloutExtender_ClientState"]=''
        data1["ctl00$ContentPlaceHolder1$ValidatorCalloutExtender1_ClientState"]=''
        data1["ctl00$ContentPlaceHolder1$txtEmailId"]=''
        data1["ctl00$ContentPlaceHolder1$ValidatorCalloutExtender2_ClientState"]=''
        data1["ctl00$ContentPlaceHolder1$txtMobile"]=''
        data1["Hidden10"]= '34034'
        data1["ctl00$ContentPlaceHolder1$txtCaptcha"] = ''
        data1["ctl00$ContentPlaceHolder1$HFCertSrNo"]=''
        data1["ctl00$ContentPlaceHolder1$HFThumbPrint"]=''
        data1["ctl00$ContentPlaceHolder1$ExpiryDate"]=''
        data1["ctl00$ContentPlaceHolder1$HFIssuerName"]=''
        data1["ctl00$ContentPlaceHolder1$HFPublicKey"]=''
        data1["ctl00$ContentPlaceHolder1$HFdscHolderName"]=''
        viewstate,viewstategenerator,previouspage,eventvalidation =request_url(data1,cookie)
        
        certificate_data= cert_data(certificate)
        if certificate_data is None:
            return HttpResponse('Could not collect the certificate')
        serial_number,thumbprint,expiry_date,holder_name,issuer_name, spaced_hexstring = certificate_data
        data1["__EVENTTARGET"] = 'ctl00$ContentPlaceHolder1$rdoregmode$0'
        data1["__VIEWSTATE"]=viewstate
        data1["__VIEWSTATEGENERATOR"] = viewstategenerator
        data1['__PREVIOUSPAGE']=previouspage
        data1["__EVENTVALIDATION"]=eventvalidation
        data1["__EVENTTARGET"]='ctl00$ContentPlaceHolder1$lnkSignature'
        data1["ctl00$ContentPlaceHolder1$HFCertSrNo"]=serial_number
        data1["ctl00$ContentPlaceHolder1$HFThumbPrint"]=thumbprint
        data1["ctl00$ContentPlaceHolder1$ExpiryDate"]=expiry_date
        data1["ctl00$ContentPlaceHolder1$HFdscHolderName"]=holder_name
        data1["ctl00$ContentPlaceHolder1$HFPublicKey"]=spaced_hexstring
        data1["ctl00$ContentPlaceHolder1$HFIssuerName"]=issuer_name
        viewstate,viewstategenerator,previouspage,eventvalidation =request_url(data1,cookie)
        data1["__EVENTTARGET"] = 'ctl00$ContentPlaceHolder1$rdoregmode$0'
        data1["__VIEWSTATE"]=viewstate
        data1["__VIEWSTATEGENERATOR"] = viewstategenerator
        data1['__PREVIOUSPAGE']=previouspage
        data1["__EVENTVALIDATION"]=eventvalidation
        data1["__EVENTTARGET"]=''
        data1["ctl00$ContentPlaceHolder1$btncheckID"]='Check availability'
        data1["ctl00$ContentPlaceHolder1$txtUserID"]=username
        dt = check_name(data1,cookie)
        if len(dt)< 2:
            print(dt)
            return HttpResponse('Error  please check the username')
        result,view = dt
        viewstate,viewstategenerator,previouspage,eventvalidation = view
        
        request.session['viewstate'] = viewstate
        request.session['viewstategenerator'] = viewstategenerator
        request.session['previouspage'] = previouspage
        request.session['eventvalidation'] = eventvalidation
        request.session['data1']= data1
        request.session['data2']= telephone,email,password
        request.session['cookie']= cookie
        return HttpResponse(result)
    
@csrf_exempt
def submit_form(request):
    viewstate= request.session['viewstate']
    viewstategenerator=request.session['viewstategenerator']
    previouspage=request.session['previouspage']
    eventvalidation=request.session['eventvalidation']
    data1 = request.session.get['data1']
    telephone,email,password = request.session.get['data2']
    data1["__EVENTTARGET"] = 'ctl00$ContentPlaceHolder1$rdoregmode$0'
    data1["__VIEWSTATE"]=viewstate
    data1["__VIEWSTATEGENERATOR"] = viewstategenerator
    data1['__PREVIOUSPAGE']=previouspage
    data1["__EVENTVALIDATION"]=eventvalidation
    data1["ctl00$ContentPlaceHolder1$txtCaptcha"]='45145'
    data1["ctl00$ContentPlaceHolder1$txtMobile"]=telephone
    data1["ctl00$ContentPlaceHolder1$txtEmailId"]=email
    data1["ctl00$ContentPlaceHolder1$txtPassword"]=password
    data1["ctl00$ContentPlaceHolder1$txtPasswordCheck"]=password
    data1["ctl00$ContentPlaceHolder1$btnSave"]='Register with DSC'
    del data1["ctl00$ContentPlaceHolder1$btncheckID"]
    cookie = request.session.get['cookie']
    response = request_url(data1,cookie)
    return HttpResponse(response)