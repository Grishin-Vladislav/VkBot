import os

from dotenv import load_dotenv, find_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, User, Target, Blacklist, Favourites
from sqlalchemy_utils import database_exists, create_database


load_dotenv(find_dotenv())
DSN = os.getenv("DSN")

engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

if not database_exists(engine.url):
    create_database(engine.url)
create_tables(engine) 

def insert_bd_user(value):
    for key in value.keys():
        key = key
    session.add(User(
        user_id = key,
        gender = value[user_id]['gender'], 
        age = value[user_id]['age'], 
        city = value[user_id]['city']))
    session.commit()

def insert_bd_target(value):
    for one in value[user_id]['targets']:
        session.add(Target(
            target_id = one,
            ))
    session.commit()
    
def insert_bd_favorites(value):
    for key in value.keys():
        key = key
    session.add(Favourites(
        user_id = key,
        target_id = value[user_id]['now']
        ))
    session.commit()
    
def insert_bd_blacklist(value):
    for key in value.keys():
        key = key
    session.add(Blacklist(
        user_id = key,
        target_id = value[user_id]['now']
        ))
    session.commit()

def get_favorites():
    session.query(Favourites).filter(Favourites.target_id).all()   

