import sqlalchemy as sq
from sqlalchemy.orm import relationship, Mapped, DeclarativeBase, mapped_column
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "User"
    
    user_id: Mapped[int] = mapped_column(primary_key=True)
    gender = sq.Column(sq.String(length=15), unique = True)
    age = sq.Column(sq.Integer, nullable=False)
    city = sq.Column(sq.String(length=30), unique = True)
    
    favorites: Mapped['Favorites'] = relationship(back_populates='User')  
    blacklist: Mapped['Blacklist'] = relationship(back_populates='User')      
        
class Target(Base):
    __tablename__ = "Target"
    
    target_id: Mapped[int] = mapped_column(primary_key=True)
    link = sq.Column(sq.String(length=100), unique = True)
    
    favorites: Mapped['Favorites'] = relationship(back_populates='Target')  
    blacklist: Mapped['Blacklist'] = relationship(back_populates='Target')         
        
    
class Favorites(Base):
    __tablename__ = "Favorites"

    user_id: Mapped[int] = mapped_column(ForeignKey('User.user_id'))
    target_id: Mapped[int] = mapped_column(ForeignKey('Target.target_id'), primary_key=True)
    
    user: Mapped['User'] = relationship(back_populates='favorites')
    target: Mapped['Target'] = relationship(back_populates='favorites') 

class Blacklist(Base):
    __tablename__ = "Blacklist"
    
    # id = sq.Column(sq.Integer, primary_key=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey('User.user_id'))
    target_id: Mapped[int] = mapped_column(ForeignKey('Target.target_id'), primary_key=True)
    
    user: Mapped['User'] = relationship(back_populates='blacklist')
    target: Mapped['Target'] = relationship(back_populates='blacklist')  

def create_tables(engine):
    Base.metadata.drop_all(engine)         
    Base.metadata.create_all(engine)