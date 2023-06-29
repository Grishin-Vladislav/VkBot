import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

def write_message (sender, message):
    authorize.method('messages.send',{'user_id':sender, 'message': message, 'random_id':get_random_id(), 'attachment':','.join(attachments)})
    
token = "vk1.a.nckBYzoLP7eiPIIlCS0NOERp-qNlojfNGbkPUUxbVtTbq3DMtsXGOnuvHhVZT028Xn9-RWpD40yvhGMhrUqVO4lB6reqGIZBg1jK12iU8PbMpHlX-kCtEo6_rXAhrzAxhR-zZb6GoSmO7ZNISt7T5X65ZUzdqRc1NJynQWzdgUG7NNJlDV2sBhM3Ox5SUUlLHHQth9e2L-5g8kK6mUgolg"
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