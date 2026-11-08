import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

password = os.getenv('PASSWORD')

Base = declarative_base()


class VKUser(Base):
    __tablename__ = 'vk_user'

    id = sq.Column(sq.Integer, primary_key=True)
    age = sq.Column(sq.Integer)
    gender = sq.Column(sq.String(length=10))
    city = sq.Column(sq.String(length=100))

    candidates = relationship('Candidates', back_populates='user', cascade='all, delete-orphan')
    favorite = relationship('Favorites', back_populates='vk_user', cascade='all, delete-orphan')
    blacklist = relationship('BlackList', back_populates='user_link', cascade='all, delete-orphan')


class Candidates(Base):
    __tablename__ = 'candidates'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_user_id = sq.Column(sq.Integer, sq.ForeignKey('vk_user.id', ondelete='CASCADE'))
    name = sq.Column(sq.String(length=40), nullable=False)
    surname = sq.Column(sq.String(length=40), nullable=False)
    link = sq.Column(sq.String, nullable=False)

    user = relationship('VKUser', back_populates='candidates', cascade='all, delete-orphan')
    photo = relationship('Photos', back_populates='candidate', cascade='all, delete-orphan')
    favor = relationship('Favorites', back_populates='cand', cascade='all, delete-orphan')
    black_list = relationship('BlackList', back_populates='candidate_link', cascade='all, delete-orphan')


class Photos(Base):
    __tablename__ = 'photos'

    id = sq.Column(sq.Integer, primary_key=True)
    candidate_id = sq.Column(sq.Integer, sq.ForeignKey('candidates.id', ondelete='CASCADE'), nullable=False)
    photo_id = sq.Column(sq.Integer, nullable=False)

    candidate = relationship('Candidates', back_populates='photo', cascade='all, delete-orphan')


class Favorites(Base):
    __tablename__ = 'favorites'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_user_id = sq.Column(sq.Integer, sq.ForeignKey('vk_user.id', ondelete='CASCADE'), nullable=False)
    candidate_id = sq.Column(sq.Integer, sq.ForeignKey('candidates.id', ondelete='CASCADE'), nullable=False)

    vk_user = relationship('VKUser', back_populates='favorite', cascade='all, delete-orphan')
    cand = relationship('Candidates', back_populates='favor', cascade='all, delete-orphan')


class BlackList(Base):
    __tablename__ = 'black_list'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_user_id = sq.Column(sq.Integer, sq.ForeignKey('vk_user.id', ondelete='CASCADE'), nullable=False)
    candidate_id = sq.Column(sq.Integer, sq.ForeignKey('candidates.id', ondelete='CASCADE'), nullable=False)

    user_link = relationship('VKUser', back_populates='blacklist', cascade='all, delete-orphan')
    candidate_link = relationship('Candidates', back_populates='black_list', cascade='all, delete-orphan')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

DSN = f'postgresql://postgres:{password}@localhost:5432/db_vkinder'
engine = sq.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()
