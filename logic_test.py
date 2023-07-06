import requests
import os
import re
import vk_api
from pprint import pprint
from dotenv import load_dotenv, find_dotenv
from Photo_download import VK

load_dotenv(find_dotenv())

TOKEN = os.getenv('USR_TOKEN')

vk_user = vk_api.VkApi(token=TOKEN)  # Создаем переменную сессии, авторизованную личным токеном пользователя.
vk_user_got_api = vk_user.get_api()
res = vk_user_got_api.users.search(  
            sort=0,  # 1 — по дате регистрации, 0 — по популярности.
            city=1,
            hometown= 'Москва',
            sex= 1,  # 1— женщина, 2 — мужчина, 0 — любой (по умолчанию).
            status=1,  # 1 — не женат или не замужем, 6 — в активном поиске.
            age_from= 20,
            has_photo=1,  # 1 — искать только пользователей с фотографией, 0 — искать по всем пользователям
            count=1000,
            fields="can_write_private_message, "  # Информация о том, может ли текущий пользователь отправить личное сообщение. Возможные значения: 1 — может; 0 — не может.
                   "city, "  # Информация о городе, указанном на странице пользователя в разделе «Контакты».
                   "domain, "  # Короткий адрес страницы.
                   "home_town, "  # Название родного города.
        )
number = 0
list_found_persons = []
for person in res["items"]:
        if not person["is_closed"]:
                if "city" in person and person["city"]["id"] == 1 and person["city"]["title"] == 'Москва':
                    number += 1
                    id_vk = person["id"]
                    list_found_persons.append(person)
# print(f'Bot found {number} opened profiles for viewing from {res["count"]}')
print(list_found_persons)



url = 'https://api.vk.com/method/users.search'
headers = {'Authorization': f'Bearer {TOKEN}'}
params = {
    'sort': 0,
    'hometown': 'Moscow',
    'sex': 1,
    'status': 6,
    'has_photo': 1,
    'fields': 'bdate',
    'v': 5.131
}

responsed = requests.get(url, headers=headers, params=params)
# pprint(responsed.json())



# name = "айди пользователя в буквах"либа 
# if any(c.isalpha() for c in name) == True:
#     user_id = VK.get_id(TOKEN, name) # получение числового айди цели

# users = []

# for i in responsed.json()['response']['items']:
#     for k, v in i.items():
#         if k == "bdate":
#             pattern = r'\d.\d.\d{4}'        
#             r = re.findall(pattern, v)
#             if len(r) >0:
#                 users.append(i)
            
# print(users)        

