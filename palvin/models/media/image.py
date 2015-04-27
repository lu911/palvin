# -*- coding:utf-8 -*-
from sqlalchemy import Column, Enum, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from palvin.database import IdMixin, CRUDMixin, Base
from palvin.models.media.constants import IMAGE_SIZE_TYPES


class ImageType(IdMixin, CRUDMixin, Base):
    name = Column(String(20), nullable=False, index=True)
    parent_id = Column(
        Integer,
        ForeignKey('%s.id' % Base.__tablename__, ondelete='CASCADE')
    )
    parent = relationship(
        'ImageType',
        remote_side='ImageType.id',
        backref=backref('children', cascade='all, delete, delete-orphan'),
        cascade='all'
    )


class Image(IdMixin, CRUDMixin, Base):

    def __init__(self):
        pass

    @classmethod
    def from_image_object(cls, file_):
        pass

    @classmethod
    def from_image_url(cls, url):
        pass


class ImageSize(IdMixin, CRUDMixin, Base):
    size = Column(
        Enum(*IMAGE_SIZE_TYPES.keys(), name='size'),
        nullable=False,
        index=True
    )
    filename = Column(String(255), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    image_id = Column(Integer, ForeignKey('%s.id' % Image.__tablename__))