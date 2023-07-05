import os





from dotenv import load_dotenv, find_dotenv
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType  
from vk_api.utils import get_random_id
<<<<<<< HEAD
=======
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
>>>>>>> 054a007224bf7560f1ce9d47655982964f7364bb

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

keyboard_start = VkKeyboard(one_time=True)
keyboard_start.add_button('Начать', color= VkKeyboardColor.SECONDARY)

keyboard_work = VkKeyboard(one_time=False)
keyboard_work.add_button('Назад', color= VkKeyboardColor.NEGATIVE)
keyboard_work.add_button('Далее', color= VkKeyboardColor.POSITIVE)
keyboard_work.add_line()
keyboard_work.add_button('Добавить в Избранное', color= VkKeyboardColor.PRIMARY)
keyboard_work.add_openlink_button('Страница пользователя', link= 'https://github.com/netology-code/adpy-team-diplom/blob/main/README.md')

def bot_start (sender, message):
    authorize.method('messages.send',{'user_id':sender, 'message': message, 'random_id':get_random_id(), 'keyboard':keyboard_start.get_keyboard()})

def bot_work (sender, message):
    authorize.method('messages.send',{'user_id':sender, 'message': message, 'random_id':get_random_id(), 'attachment':','.join(photos), 'keyboard':keyboard_work.get_keyboard()})

image = "test_image.png"
authorize = vk_api.VkApi(token = TOKEN)
longpoll = VkLongPoll(authorize)
upload = VkUpload (authorize)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        reseave_message = event.text
        sender = event.user_id
        if reseave_message == "Начать":
            photos = []
            upload_image = upload.photo_messages(photos=image)[0]
            photos.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
            bot_work(sender, "Анкета (ФИО), ссылка ниже + 3 фото")
        else:
            attachments = [] 
            upload_image = upload.photo_messages(photos=image)[0]
            bot_start(sender, "Начало работы")

        