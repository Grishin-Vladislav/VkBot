import os

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv, find_dotenv

from db._sqlalchemy.DB import insert_bd_user, insert_bd_favorites, \
    insert_bd_blacklist, get_favorites, get_blacklist
from db.redis.finis import FiniteStateMachineLocal
from vk.methods import VkBotHandler
from vk.find_people import Finder
from keyboards.kb import Markup
from utils.validation import is_valid_age, get_city

# Setting vars
load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")
USR_TOKEN = os.getenv("USR_TOKEN")

# Setting FSM
# r = redis.Redis(host='localhost', port=6379, decode_responses=True)
machine = FiniteStateMachineLocal()

# Deleting all redis data (Only for testing)
# for key in r.keys(): r.delete(key)
cache = {}

# Setting api, bot and polling
usr_api = vk_api.VkApi(token=USR_TOKEN)
api = vk_api.VkApi(token=TOKEN)
bot = VkBotHandler(api)
long_poll = VkLongPoll(api)
finder = Finder(token=USR_TOKEN)

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
                cache[user_id] = {'gender': message}
                machine.set(user_id, 'asked_age')
                bot.send_message(user_id, 'Твой возраст?')
            else:
                bot.send_message(user_id, "Нажми на кнопку.",
                                 markup=Markup.sex())

        if state == 'asked_age':
            if is_valid_age(message):
                cache[user_id]['age'] = message
                machine.set(user_id, 'asked_city')
                bot.send_message(user_id, 'Твой город?')
            else:
                bot.send_message(user_id, "Введи корректный возраст.")

        if state == 'asked_city':
            city = get_city(message, usr_api)
            if city:
                machine.set(user_id, 'ensure_city')
                cache[user_id]['city'] = city
                bot.send_message(user_id, f"Это твой город?\n{city}",
                                 markup=Markup.yes_no())
            else:
                bot.send_message(user_id, "Город не найден, попробуй ещё.")

        if state == 'ensure_city':
            if message == 'Да':
                insert_bd_user(user_id, cache)
                machine.set(user_id, 'main_menu')

                # for target in finder.find_people():
                #     r.rpush(f'user:{user_id}:cache', target)
                #
                # target_id = r.lpop(f'user:{user_id}:cache')
                # target_info = finder.get_info(target_id)
                # target_photo = finder.get_photo(target_id)

                cache[user_id]['targets'] = list()
                for target in finder.find_people(user_id, cache):
                    cache[user_id]['targets'].append(target)

                target_id = cache[user_id]['targets'].pop(0)
                target_info = finder.get_info(target_id)
                target_photo = finder.get_photo(target_id)
                cache[user_id]['now'] = target_id

                bot.send_message(user_id, target_info,
                                 attachments=target_photo,
                                 markup=Markup.main())

            elif message == 'Нет':
                machine.set(user_id, 'asked_city')
                bot.send_message(user_id, 'Твой город?')

            else:
                bot.send_message(user_id, "Нажми на кнопку.")

        if state == 'main_menu':
            if message == 'Далее':
                # target_id = r.lpop(f'user:{user_id}:cache')
                try:
                    target_id = cache[user_id]['targets'].pop(0)
                except IndexError:
                    blacklist = get_blacklist(user_id)
                    for target in finder.find_people(user_id, cache):
                        if target in blacklist:
                            continue
                        cache[user_id]['targets'].append(target)
                    target_id = cache[user_id]['targets'].pop(0)

                cache[user_id]['now'] = target_id
                target_info = finder.get_info(target_id)
                target_photo = finder.get_photo(target_id)

                bot.send_message(user_id, target_info,
                                 attachments=target_photo,
                                 markup=Markup.main())

            elif message == 'ЧС':
                insert_bd_blacklist(user_id, cache)
                bot.send_message(user_id, 'Юзер добавлен в blacklist')

            elif message == 'Добавить в Избранное':
                info = finder.get_info(cache[user_id]['now'])
                insert_bd_favorites(user_id, cache, info)
                bot.send_message(user_id, 'Юзер добавлен в избранное')

            elif message == 'Моё избранное':
                favourites = get_favorites(user_id)
                bot.send_message(user_id, favourites)

            else:
                bot.send_message(user_id, "Нажми на кнопку.")
