import requests
import os
from pprint import pprint
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

TOKEN = os.getenv('TOKEN')
url = 'https://api.vk.com/method/users.search'
headers = {'Authorization': f'Bearer {TOKEN}'}
params = {
    'sort': 0,
    'hometown': 'Moscow',
    'sex': 1,
    'status': 6,
    'has_photo': 1,
    'fields': 'about, bdate',
    'v': 5.131
}

response = requests.get(url, headers=headers, params=params)
pprint(response.json())
