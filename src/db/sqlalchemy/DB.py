import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from models import create_tables


DSN = os.getenv("DSN")         
engine = sqlalchemy.create_engine(DSN)
# MetaData.drop_all()
MetaData.drop_all(engine)
# create_tables(engine)


# Session = sessionmaker(bind = engine)
# session = Session()