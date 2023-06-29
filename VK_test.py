import vk_api
from secrets_1 import token
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

def write_message (sender, message):
    authorize.method('messages.send',{'user_id':sender, 'message': message, 'random_id':get_random_id(), 'attachment':','.join(attachments)})

image = "test_image.png"
authorize = vk_api.VkApi(token = token)
longpoll = VkLongPoll(authorize)
upload = VkUpload (authorize)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        reseave_message = event.text
        sender = event.user_id
        attachments = []
        upload_image = upload.photo_messages(photos=image)[0]
        attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
        write_message(sender, "Привет")