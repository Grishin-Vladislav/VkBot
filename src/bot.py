import os
import redis

from dotenv import load_dotenv, find_dotenv
from src.db.redis.finis import FiniteStateMachine

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
machine = FiniteStateMachine(r)


if __name__ == '__main__':
    for i in range(5):
        user = 123456
        state = machine.get(user)

        if state is None:
            print(f'no state, switching to state1')
            machine.set(user, 'state1')

        if state == 'state1':
            print(f'{state}, switching to state2')
            machine.set(user, 'state2')

        if state == 'state2':
            print(f'{state}, switching to state1')
            machine.set(user, 'state1')
