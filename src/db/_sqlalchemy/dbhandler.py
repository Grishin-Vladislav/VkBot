import os

from dotenv import load_dotenv, find_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import *
from sqlalchemy_utils import database_exists, create_database

load_dotenv(find_dotenv())
DSN = os.getenv("DSN")


class DbHandler:
    def __init__(self, DSN):
        self.__engine = sqlalchemy.create_engine(DSN)

        if not database_exists(self.__engine.url):
            create_database(self.__engine.url)
            self.__create_tables(self.__engine)
        else:
            self.__create_tables(self.__engine)

        self.__Session = sessionmaker(bind=self.__engine)
        self.__s = None

    def __enter__(self):
        self.__s = self.__Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__s:
            self.__s.close()

    def commit(self):
        try:
            self.__s.commit()
        except:
            self.__s.rollback()

    @staticmethod
    def __create_tables(engine) -> None:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    # Это первый тестовый метод для работы с бд
    def write_user(self, user_id, age, city, sex):
        user = User(user_id=user_id, gender=sex, age=age, city=city)
        self.__s.add(user)
        self.__s.commit()
        return user.user_id


with DbHandler(DSN) as db:
    user_id = db.write_user('8800555', 80, 'moscow', 'male')
