import requests
from os import environ, path
from json import load
base_dir = path.abspath(path.dirname(__file__))
api_host = 'https://westcentralus.api.cognitive.microsoft.com'
person_group_id = 'ko_wen-je_2018'

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
        faces = response.json()
    except Exception as e:
        print('Error:')
        print(e)

    return faces

def identify_face(person_group_id, face_list):
    headers = { 
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': environ['AZURE_FACE_API_KEY']
    }
    body = {
        'personGroupId': person_group_id,
        'faceIds': face_list,
        "maxNumOfCandidatesReturned": 1,
        "confidenceThreshold": 0.5
    }
    api_url = api_host + '/face/v1.0/identify'
    try:
        response = requests.post(api_url, headers=headers, json=body)
        faces = response.json()
    except Exception as e:
        print('Error:')
        print(e)

    return response.json()

def get_person_group(person_group_id, person_id):
    headers = { 
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': environ['AZURE_FACE_API_KEY']
    }
    api_url = api_host + '/face/v1.0/persongroups/{}/persons/{}'.format(person_group_id, person_id)
    try:
        response = requests.get(api_url, headers=headers)
        faces = response.json()
    except Exception as e:
        print('Error:')
        print(e)

    return response.json()

# file_name = "../testing_data/chen.jpg"
file_name = "../testing_data/ko.jpg"
full_path = path.join(base_dir, file_name)
with open(full_path, "rb") as image_file:
    img_binary = image_file.read() # BytesIO(image_file.read()) 也可
print('DetectFace Response:')
face_json = detect_face(img_binary)
print(face_json, end='\n\n')

print('IdentifyPerson Response:')
face_list = []
for f in face_json:
    face_list.append(f['faceId'])
result_json = identify_face(person_group_id, face_list)
print(result_json, end='\n\n')

print('GetPerson Response:')
for f in result_json:
    for c in f['candidates']:
        person_json = get_person_group(person_group_id, c['personId'])
        print(person_json, end='\n\n')
        print('GetPerson name:')
        print(person_json['name'])        
