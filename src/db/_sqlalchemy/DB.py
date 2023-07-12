import os

from dotenv import load_dotenv, find_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from src.db._sqlalchemy.models import create_tables, User, Blacklist, \
    Favourites


load_dotenv(find_dotenv())
DSN = os.getenv("DSN")

engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

if not database_exists(engine.url):
    create_database(engine.url)
create_tables(engine)


def insert_bd_user(user_id, cache):
    session.add(User(
        user_id=user_id,
        gender=cache[user_id]['gender'],
        age=cache[user_id]['age'],
        city=cache[user_id]['city']))
    session.commit()


def insert_bd_favorites(user_id, cache, info):
    res = session.query(Favourites). \
        filter(Favourites.user_id == user_id).filter(
        Favourites.target_id == cache[user_id]['now']).all()

    if not res:
        session.add(Favourites(
            user_id=user_id,
            target_id=cache[user_id]['now'],
            info=info
        ))
        session.commit()


def insert_bd_blacklist(user_id, cache):
    res = session.query(Blacklist). \
        filter(Blacklist.target_id == cache[user_id]['now']).filter(
        Blacklist.user_id == user_id).all()

    if not res:
        session.add(Blacklist(
            user_id=user_id,
            target_id=cache[user_id]['now']
        ))
        session.commit()


def get_favorites(user_id) -> str:
    res = session.query(Favourites).filter(
        Favourites.user_id == user_id).all()
    info = []
    for favourite in res:
        info.append(favourite.info)
    return '\n'.join(info)


def get_blacklist(user_id) -> list[int]:
    res = session.query(Blacklist).filter(
        Blacklist.user_id == user_id).all()
    blacklist = list()
    for target in res:
        blacklist.append(target.target_id)
    return blacklist
