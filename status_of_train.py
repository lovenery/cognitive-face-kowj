import requests
from os import environ
api_host = 'https://westcentralus.api.cognitive.microsoft.com'
person_group_id = 'ko_wen-je_2018'

def training_status(person_group_id):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': environ['AZURE_FACE_API_KEY']
    }
    api_url = api_host + '/face/v1.0/persongroups/{}/training'.format(person_group_id)
    try:
        response = requests.get(api_url, headers=headers)
    except Exception as e:
        print('Error:')
        print(e)

    return response.json()

print(training_status(person_group_id))