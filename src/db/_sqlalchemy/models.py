from sqlalchemy import Column, BIGINT, ForeignKey, Text, VARCHAR, Float, \
    INTEGER, TIMESTAMP, BOOLEAN, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    user_id = Column(BIGINT, primary_key=True)
    gender = Column(String(length=6), nullable=False)
    age = Column(INTEGER, nullable=False)
    city = Column(String(length=30), nullable=False)

    favourites = relationship('Favourites', back_populates='user')
    blacklist = relationship('Blacklist', back_populates='user')


class Target(Base):
    __tablename__ = "target"

    target_id = Column(INTEGER, primary_key=True)

    favourites = relationship('Favourites', back_populates='target')
    blacklist = relationship('Blacklist', back_populates='target')


class Favourites(Base):
    __tablename__ = "favourites"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, ForeignKey('user.user_id'))
    target_id = Column(BIGINT, ForeignKey('target.target_id'))

    user = relationship('User', back_populates='favourites')
    target = relationship('Target', back_populates='favourites')

class Blacklist(Base):
    __tablename__ = "blacklist"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, ForeignKey('user.user_id'))
    target_id = Column(BIGINT, ForeignKey('target.target_id'))

    user = relationship('User', back_populates='blacklist')
    target = relationship('Target', back_populates='blacklist')

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

