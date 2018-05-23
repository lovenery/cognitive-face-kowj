"""
refs:
https://stackoverflow.com/questions/10588644/how-can-i-see-the-entire-http-request-thats-being-sent-by-my-python-application
https://westcentralus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d
"""

import requests
from io import BytesIO
from os import path, environ
from pprint import pprint
import logging
base_dir = path.abspath(path.dirname(__file__))
api_host = 'https://westcentralus.api.cognitive.microsoft.com'
person_group_id = 'ko_wen-je_2018'

def http_debugger():
    try:
        import http.client as http_client
    except ImportError:
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

def detect_face(img_binary):
    headers = { 
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': environ['AZURE_FACE_API_KEY']
    }
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,smile',
    }
    api_url = api_host + '/face/v1.0/detect'
    try:
        response = requests.post(api_url, params=params, headers=headers, data=img_binary)
        faces = response.json() #list
    except Exception as e:
        print('Error:')
        print(e)

    return faces

def delete_group(person_group_id):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': environ['AZURE_FACE_API_KEY']
    }
    api_url = api_host + '/face/v1.0/persongroups/' + person_group_id
    try:
        response = requests.delete(api_url, headers=headers)
    except Exception as e:
        print('Error:')
        print(e)

    if response.text == '':
        return 'Delete Person group: ' + person_group_id
    else:
        return response.json()

def create_group(person_group_id, group_data):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': environ['AZURE_FACE_API_KEY']
    }
    api_url = api_host + '/face/v1.0/persongroups/' + person_group_id
    try:
        response = requests.put(api_url, headers=headers, json=group_data)
    except Exception as e:
        print('Error:')
        print(e)

    if response.text == '':
        return 'Create Person group: ' + person_group_id
    else:
        return response.json()

def create_person_in_group(person_group_id, person_data):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': environ['AZURE_FACE_API_KEY']
    }
    api_url = api_host + '/face/v1.0/persongroups/{}/persons'.format(person_group_id)
    try:
        response = requests.post(api_url, headers=headers, json=person_data)
    except Exception as e:
        print('Error:')
        print(e)

    return response.json()

def add_face_to_person_in_gorup(person_group_id, person_id, img_binary):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': environ['AZURE_FACE_API_KEY']
    }
    api_url = api_host + '/face/v1.0/persongroups/{}/persons/{}/persistedFaces'.format(person_group_id, person_id)
    try:
        response = requests.post(api_url, headers=headers, data=img_binary)
    except Exception as e:
        print('Error:')
        print(e)

    return response.json()

def train_person_group(person_group_id):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': environ['AZURE_FACE_API_KEY']
    }
    api_url = api_host + '/face/v1.0/persongroups/{}/train'.format(person_group_id)
    try:
        response = requests.post(api_url, headers=headers, data=img_binary)
    except Exception as e:
        print('Error:')
        print(e)

    if response.text == '':
        return 'Training Person group: ' + person_group_id
    else:
        return response.json()

# http_debugger()

# 列出所有person groups
# curl -v -X GET "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups" -H "Ocp-Apim-Subscription-Key: XXX"

# print('正在刪除Person Group...')
# print(delete_group(person_group_id))

print('正在建立Person Group...')
group_data = {
    'name': '柯p群組',
    'userData': '柯文哲群組'
}
print(create_group(person_group_id, group_data), end='\n\n')

print('正在加入Person到Person Group...')
person_data = {
    'name': '柯p本人',
    'userData': '柯文哲本人'
}
person_json = create_person_in_group(person_group_id, person_data)
print(person_json, end='\n\n')
person_id = person_json['personId']

for i in range(1, 6):
    file_name = "../training_data/ko{}.jpg".format(i)
    full_path = path.join(base_dir, file_name)
    with open(full_path, "rb") as image_file:
        img_binary = image_file.read()
    print('正在加入臉編號{}到該位Person'.format(i))
    face_json = add_face_to_person_in_gorup(person_group_id, person_id, img_binary)
    print(face_json, end='\n\n')

print('開始訓練Person Group...')
train_json = train_person_group(person_group_id)
print(train_json, end='\n')
