import os

from dotenv import load_dotenv, find_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, create_engine
from models import create_tables
from sqlalchemy_utils import database_exists, create_database


load_dotenv(find_dotenv())
DSN = os.getenv("DSN")


engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

if not database_exists(engine.url):
    create_database(engine.url)
create_tables(engine)


user_id = 1
target = 1 
now = 1

cache = {
    user_id: {'age':'loh', 'gender':'chmo', 'city': 'GGG'},
    "user_id:target":[123, 234],
    "user_id:now": 123}

t = User(gender = cache[user_id]['gender'])
session.add(t)
session.commit()

# def insert_bd(value):
#     with session() as conn:
#         user_info = conn.execute(insert('User').values(user_id=user_id), [
#             {"user_id" : user_id},
#             {"gender": value[user_id]['gender']},
#             {"age": value[user_id]['age']},
#             {"city": value[user_id]['city']}
#             ]
#         ) 
#         conn.commit()

# insert_bd(cache)

