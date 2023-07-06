import asyncio
import os
from aiohttp import ClientSession
import json
import nest_asyncio
from dotenv import load_dotenv, find_dotenv
nest_asyncio.apply()

load_dotenv(find_dotenv())

TOKEN = os.getenv('USR_TOKEN')
list_data=[]

async def bound_fetch_zero(sem,id,session):
        async with sem:
            await fetch_zero(id,session)

async def fetch_zero(id, session):
    url = build_url(id)
    try:
        async with session.get(url) as response:

                # Считываем json
                resp=await response.text()
                js=json.loads(resp)
                list_users=[x for x in js['response'] if x != False]

                # Проверяем если город=1(Москва) тогда добавляем в лист
                for it in list_users:
                    try:
                        if it[0]['city']['id']=="Москва":
                                list_data.append(it[0]['id'])
                    except Exception:
                        pass

    except Exception as ex:
        print(f'Error: {js}')

#  Генерация url к апи вк, 25 запросов в одном
def build_url(id):
    api = 'API.users.get({{\'user_ids\':{},\'fields\':\'city\'}})'.format(
        id * 25 + 1)
    for i in range(2, 26):
        api += ',API.users.get({{\'user_ids\':{},\'fields\':\'city\'}})'.format(
            id * 25 + i)
    url = 'https://api.vk.com/method/execute?access_token={}&v=5.101&code=return%20[{}];'.format(
        TOKEN[id%len(TOKEN)], api)
    return url

async def run_zero(id):
    tasks = []
    sem = asyncio.Semaphore(1000)

    async with ClientSession() as session:

#  Значение 3200 зависит от вашего числа токенов 
        for id in range((id - 1) * 40, id * 40):
            task = asyncio.ensure_future(bound_fetch_zero(sem,id, session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses
        del responses
        await session.close()

# Запускаем  сборщик
for i in range(0,17):
  for id in range(i*500+1,(i+1)*500+1):
      print(id)
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      loop.run_until_complete(run_zero(id))