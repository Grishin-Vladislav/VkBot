from sqlalchemy import Column, BIGINT, ForeignKey, VARCHAR, INTEGER, String
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


class Favourites(Base):
    __tablename__ = "favourites"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, ForeignKey('user.user_id'), nullable=False)
    target_id = Column(BIGINT, nullable=False)
    info = Column(VARCHAR(200), nullable=False)

    user = relationship('User', back_populates='favourites')


class Blacklist(Base):
    __tablename__ = "blacklist"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, ForeignKey('user.user_id'), nullable=False)
    target_id = Column(BIGINT, nullable=False)

    user = relationship('User', back_populates='blacklist')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
