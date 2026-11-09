import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

password = os.getenv('PASSWORD')

Base = declarative_base()


class VKUser(Base):
    __tablename__ = 'vk_user'

    id = sq.Column(sq.BigInteger, primary_key=True)
    age = sq.Column(sq.Integer, nullable=False)
    sex = sq.Column(sq.Integer, nullable=False)              #для поиска
    city_id = sq.Column(sq.Integer, nullable=False)          #для поиска

    candidates = relationship('Candidates', back_populates='owner', cascade='all, delete-orphan')
    favorite = relationship('Favorites', back_populates='user', cascade='all, delete-orphan')
    blacklist = relationship('BlackList', back_populates='user', cascade='all, delete-orphan')


class Candidates(Base):
    __tablename__ = 'candidates'

    id = sq.Column(sq.BigInteger, primary_key=True)
    owner_id = sq.Column(sq.Integer, sq.ForeignKey('vk_user.id', ondelete='CASCADE')) #ссылка на владельца
    name = sq.Column(sq.String(length=40), nullable=False)
    surname = sq.Column(sq.String(length=40), nullable=False)
    link = sq.Column(sq.String, nullable=False)
    age = sq.Column(sq.Integer)                              #для поиска
    sex = sq.Column(sq.Integer)                              #для поиска
    gender = sq.Column(sq.String(length=10))                 #для вывода
    city = sq.Column(sq.String(length=100))                  #для вывода

    __table_args__ = (
        sq.UniqueConstraint('owner_id', 'vk_id', name='uq_candidate_owner_vk'),
        sq.Index('ix_candidate_owner', 'owner_id'),
    )

    owner = relationship('VKUser', back_populates='candidates')
    photos = relationship('Photo', back_populates='candidate', cascade='all, delete-orphan',
                          order_by='Photo.id')
    favorites = relationship('Favorite', back_populates='candidate',
                         cascade='all, delete-orphan')
    blacklist_entries = relationship('Blacklist', back_populates='candidate',
                                 cascade='all, delete-orphan')


class Photo(Base):
    __tablename__ = 'photo'

    id = sq.Column(sq.Integer, primary_key=True)
    candidate_id = sq.Column(sq.Integer,sq.ForeignKey('candidate.id', ondelete='CASCADE'),nullable=False)
    attachment = sq.Column(sq.String, nullable=False)

    __table_args__ = (
        sq.UniqueConstraint('candidate_id', 'attachment',
                            name='uq_photo_candidate_attachment'),
    )

candidate = relationship('Candidate', back_populates='photos')


class Favorites(Base):
    __tablename__ = 'favorites'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_user_id = sq.Column(sq.Integer, sq.ForeignKey('vk_user.id', ondelete='CASCADE'), nullable=False)
    candidate_id = sq.Column(sq.Integer, sq.ForeignKey('candidates.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (
        sq.UniqueConstraint('vk_user_id', 'candidate_id',
                            name='uq_favorite_user_candidate'),
    )

    user = relationship('VKUser', back_populates='favorites')
    candidate = relationship('Candidate', back_populates='favorites')


class BlackList(Base):
    __tablename__ = 'black_list'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_user_id = sq.Column(sq.Integer, sq.ForeignKey('vk_user.id', ondelete='CASCADE'), nullable=False)
    candidate_id = sq.Column(sq.Integer, sq.ForeignKey('candidates.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (
        sq.UniqueConstraint('vk_user_id', 'candidate_id',
                            name='uq_blacklist_user_candidate'),
    )

    user = relationship('VKUser', back_populates='blacklist')
    candidate = relationship('Candidate', back_populates='blacklist_entries')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

DSN = f'postgresql://postgres:{password}@localhost:5432/db_vkinder'
engine = sq.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()
