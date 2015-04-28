# -*- coding:utf-8 -*-
from sqlalchemy import Column, Enum, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr

from database import IdMixin, Base
from models.media.constants import IMAGE_SIZE_TYPES


class ImageType(IdMixin, Base):
    name = Column(String(20), nullable=False, index=True)

    @declared_attr
    def parent_id(cls):
        return Column(
            Integer,
            ForeignKey('%s.id' % cls.__tablename__, ondelete='CASCADE')
        )

    @declared_attr
    def parent(cls):
        return relationship(
            cls.__name__,
            remote_side='%s.id' % cls.__name__,
            backref=backref('children', cascade='all, delete, delete-orphan')
        )


class Image(IdMixin, Base):

    def __init__(self):
        pass

    @classmethod
    def from_image_object(cls, file_):
        pass

    @classmethod
    def from_image_url(cls, url):
        pass


class ImageSize(IdMixin, Base):
    size = Column(
        Enum(*IMAGE_SIZE_TYPES, name='size'),
        nullable=False,
        index=True
    )
    filename = Column(String(255), nullable=False, index=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    image_id = Column(Integer, ForeignKey('%s.id' % Image.__tablename__))