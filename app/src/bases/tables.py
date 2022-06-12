from os import environ
from sqlalchemy import Column, ForeignKey, BigInteger, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

POSTGRES_DB = environ.get("POSTGRES_DB")
POSTGRES_USER = environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")

engine_settings = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@parallel_db:5432/{POSTGRES_DB}"
engine = create_engine(engine_settings)
Base = declarative_base()

class Channel(Base):
    '''
    Таблица настроек чата
    '''
    __tablename__ = 'channels'

    id_telegram = Column(BigInteger, primary_key=True, autoincrement = False)
    linked_chat_id = Column(BigInteger)
    mute_timer = Column(Integer)
    votes_for_block = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    posts = relationship('Post', back_populates='channels')
    blacklist = relationship('Blacklist', back_populates='channels')

class Post(Base):
    '''
    Таблица для постов
    '''
    __tablename__ = 'posts'  
    
    id_telegram = Column(Integer, primary_key=True, autoincrement = False)  
    channel_id = Column(ForeignKey('channels.id_telegram'))
    author_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    channels = relationship('Channel', back_populates='posts')
    votes = relationship('Vote', back_populates='posts')

class Vote(Base):
    '''
    Таблица для жалоб
    '''
    __tablename__ = 'votes'  
    
    id_vote = Column(Integer, primary_key=True)
    post_id = Column(ForeignKey('posts.id_telegram'))
    author_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False) 
    posts = relationship('Post', back_populates='votes')

class Blacklist(Base):
    '''
    Таблица для черного списка
    '''
    __tablename__ = 'blacklist'
    
    id_telegram = Column(BigInteger, primary_key=True, autoincrement = False)
    channel_id = Column(ForeignKey('channels.id_telegram'))
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    type_of_access_restriction = Column(String)
    mute_end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    channels = relationship('Channel', back_populates='blacklist')

Base.metadata.create_all(engine)