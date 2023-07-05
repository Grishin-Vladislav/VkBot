import os

from dotenv import load_dotenv, find_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from models import create_tables
from sqlalchemy_utils import database_exists, create_database

load_dotenv(find_dotenv())
DSN = os.getenv("DSN")

engine = sqlalchemy.create_engine(DSN)

if not database_exists(engine.url):
    create_database(engine.url)
# MetaData.drop_all()
# MetaData.drop_all(engine)
create_tables(engine)


# Session = sessionmaker(bind = engine)
# session = Session()