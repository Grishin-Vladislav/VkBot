import os

import redis
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv, find_dotenv

from db.redis.finis import FiniteStateMachine
from vk.methods import VkBotHandler
from keyboards.kb import Markup
from utils.validation import is_valid_age, is_valid_city

# Setting vars
load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

# Setting FSM
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
machine = FiniteStateMachine(r)

# Deleting all redis data (Only for testing)
for key in r.keys(): r.delete(key)

# Setting api, bot and polling
api = vk_api.VkApi(token=TOKEN)
bot = VkBotHandler(api)
long_poll = VkLongPoll(api)

if __name__ == '__main__':
    for event in long_poll.listen():

        if not event.to_me or not VkEventType.MESSAGE_NEW:
            continue

        user_id = event.user_id
        message = event.message
        state = machine.get(user_id)

        if state is None:
            machine.set(user_id, 'started_dialogue')
            bot.send_message(user_id, "Пройди опрос, нажми начать.",
                             markup=Markup.start())

        if state == 'started_dialogue':
            if message == 'Начать':
                machine.set(user_id, 'asked_sex')
                bot.send_message(user_id, "Твой пол?",
                                 markup=Markup.sex())
            else:
                bot.send_message(user_id, "Нажми на кнопку.",
                                 markup=Markup.start())

        if state == 'asked_sex':
            if message in ('М', 'Ж'):
                machine.set(user_id, 'asked_age')
                bot.send_message(user_id, 'Твой возраст?')
            else:
                bot.send_message(user_id, "Нажми на кнопку.",
                                 markup=Markup.sex())

        if state == 'asked_age':
            if is_valid_age(message):
                machine.set(user_id, 'asked_city')
                bot.send_message(user_id, 'Твой город?')
            else:
                bot.send_message(user_id, "Введи корректный возраст.")

        if state == 'asked_city':
            if is_valid_city(message):
                machine.set(user_id, 'main_menu')
                bot.send_message(user_id, "вот первое фото",
                                 attachments=['https://sun1-99.userapi.com/impg/Qkf2GVaPMmYD4n3ZoaqpwW3uZKwZ0wYqnbs6lQ/HYbgMSffQB0.jpg?size=1440x2160&quality=95&sign=e4832ceeb9a2112e04b0a8dc9dc86bdb&type=album'],
                                 markup=Markup.main())
            else:
                bot.send_message(user_id, "Введи корректный город.")

        if state == 'main_menu':
            bot.send_message(user_id, "Это всё.")
