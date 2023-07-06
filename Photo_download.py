import os
import requests
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

TOKEN = os.getenv('USR_TOKEN')

class VK:
    def __init__(self):
        pass
                        
    def get_id(self, name):
        URL = 'https://api.vk.com/method/utils.resolveScreenName'
        params = {
                "screen_name" : name,
                'access_token': TOKEN,
                'v':'5.131'
                }
        res = requests.get(URL, params=params).json()
        return res['response']['object_id']

    def photo_upload (self, ID):
        URL = 'https://api.vk.com/method/photos.get'
        params = {
            "owner_id" : ID,
            'album_id' : 'profile',
            'access_token': TOKEN, 
            'extended' : 'likes',
            'photo_sizes': '1',
            'v':'5.131',
            'count': 3
        }
        res = requests.get(URL, params=params).json()
        photos = res['response']['items']
        return photos

    def get_3_photos(self, photo):
        photo_list = {}
        for i in photo:
            for j in i['sizes']:
                for k, f in j.items():
                    if k == 'type' and f == 'w' or "z" or "y": 
                        url_photo = (j['url'])
                        date = str(i['date'])
                        likes = str(i['likes']['count'])
                        ld = likes + '_' + date + '.jpg'
                        info = {'file_name':ld,'size':j['type']}
                        url_info = {url_photo:info}
                        photo_list[ld] = url_info
        return photo_list 