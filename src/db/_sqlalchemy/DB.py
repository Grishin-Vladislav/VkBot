import os

from dotenv import load_dotenv, find_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from models import create_tables

load_dotenv(find_dotenv())
DSN = os.getenv("DSN")         
engine = sqlalchemy.create_engine(DSN)
# MetaData.drop_all()
# MetaData.drop_all(engine)
create_tables(engine)


# Session = sessionmaker(bind = engine)
# session = Session()