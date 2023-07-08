from time import sleep

import vk_api


class Finder:
    RPS_DELAY = 0.34
    def __init__(self, token) -> None:
        self.vk_user = vk_api.VkApi(token=token)
        self.vk_user_got_api = self.vk_user.get_api()
    
    def find_people(self):
        list_found_persons = []
        res = self.vk_user_got_api.users.search(  
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
        
        for person in res["items"]:
                if person["is_closed"] == False:
                        if "city" in person and person["city"]["id"] == 1 and person["city"]["title"] == 'Москва':
                            list_found_persons.append(person['id'])
        sleep(0.33)
        return list_found_persons

    def get_photo(self, user_id):                            
        attachment = []
        res = self.vk_user_got_api.photos.get(
                    owner_id= user_id,
                    album_id="profile",  
                    extended=1, 
                    count=30
                )
        sleep(0.33)
        photo_list = {}
        for i in res['items']:
            likes = i['likes']['count']
            photo_id = str(i['id'])
            photo_list[likes] = photo_id
        sorted_photo = dict(sorted(photo_list.items(), reverse=True))
        counter = 0 

        for id in sorted_photo.values():
            listr = ['https://vk.com/id',  user_id, '?z=photo',  user_id, '_', id]
            attachment.append(''.join(listr))
            counter +=1
            if counter == res['count'] or counter == 3:
                return attachment
            else:
                continue
            
    def get_info(self, user_id):
        info = self.vk_user_got_api.users.get(
                        user_id=user_id,
                        fields="name_case, nickname"
                    )
        sleep(0.33)
        for i in info:
            name = i['first_name']
            surname = i['last_name']
            url = ['https://vk.com/id', user_id]
            url = (''.join(url))
            return f'ФИО: {name} {surname},\nСсылка на профиль: {url}'
#
# for i in Finder().find_people():
#     print(Finder().get_info(str(i)))
#     time.sleep(0.33)
#     print(Finder().get_photo(str(i)))
#     time.sleep(0.33)