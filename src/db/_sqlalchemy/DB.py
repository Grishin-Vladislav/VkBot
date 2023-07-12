import os

from dotenv import load_dotenv, find_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from db._sqlalchemy.models import create_tables, User, Target, Blacklist, Favourites
from sqlalchemy_utils import database_exists, create_database


load_dotenv(find_dotenv())
DSN = os.getenv("DSN")

engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

if not database_exists(engine.url):
    create_database(engine.url)
create_tables(engine) 

def insert_bd_user(user_id, value):
    session.add(User(
        user_id = user_id,
        gender = value[user_id]['gender'], 
        age = value[user_id]['age'], 
        city = value[user_id]['city']))
    session.commit()

def insert_bd_target(user_id, value):
    for one in value[user_id]['targets']:
        session.add(Target(
            target_id = one,
            ))
    session.commit()
    
def insert_bd_favorites(user_id, value):
    session.add(Favourites(
        user_id = user_id,
        target_id = value[user_id]['now']
        ))
    session.commit()
    
def insert_bd_blacklist(user_id, value):
    session.add(Blacklist(
        user_id = user_id,
        target_id = value[user_id]['now']
        ))
    session.commit()

def get_favorites():
    session.query(Favourites).filter(Favourites.target_id).all()   

