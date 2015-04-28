# -*- coding:utf-8 -*-
from StringIO import StringIO

from sqlalchemy import Column, Enum, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship, backref

from palvin.database import IdMixin, TimestampMixin, Base
from palvin.utils import get_uuid
from palvin.aws.s3 import file_upload
from palvin.models.media.constants import IMAGE_SIZE, IMAGE_SIZE_TYPES


class Image(IdMixin, TimestampMixin, Base):
    filename = Column(String(255), nullable=False, index=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)

    @classmethod
    def from_image_object(cls, file_, path='/'):
        from wand.image import Image as WandImage
        from wand.exceptions import WandException

        try:
            wand_image = WandImage(file=file_)
        except WandException, e:
            ImageErrorLog.create(
                name=e.__class__.__name__,
                description=e.message
            ).save(commit=True)
            return None
        with wand_image:
            uuid = get_uuid()
            filename = file_upload(
                file_, path, '%s/%sx%s' % (
                    uuid,
                    wand_image.width,
                    wand_image.height
                )
            )
            if not filename:
                ImageErrorLog.create(
                    name='FileUploadFailed',
                    description='original image saving error.'
                ).save(commit=True)
                return None

            image = cls.create(
                filename=filename,
                width=wand_image.width,
                height=wand_image.height
            )

            for type_, (width, height) in IMAGE_SIZE.items():
                wand_image.resize(width, height)
                output = StringIO()
                wand_image.save(file=output)
                filename = file_upload(
                    file_, path, '%s/%sx%s' % (
                        uuid,
                        wand_image.width,
                        wand_image.height
                    )
                )
                if not filename:
                    ImageErrorLog.create(
                        name='FileUploadFailed',
                        description='%s type image saving error.' % type_,
                        image=image
                    )
                    continue

                ImageSize.create(
                    type=type_,
                    filename=filename,
                    width=wand_image.width,
                    height=wand_image.height,
                    image=image
                )
            image.save(commit=True)
            return image
        return None

    @classmethod
    def from_image_url(cls, url, path='/'):
        import requests

        try:
            r = requests.get(url, timeout=3)
        except requests.exceptions.RequestException, e:
            ImageErrorLog.create(
                name=e.__class__.__name__,
                description=e.message
            ).save(commit=True)
            return None
        output = StringIO(r.content)
        return cls.from_image_object(output, path=path)


class ImageSize(IdMixin, Base):
    type = Column(
        Enum(*IMAGE_SIZE_TYPES, name='size'),
        nullable=False,
        index=True
    )
    filename = Column(String(255), nullable=False, index=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    image_id = Column(
        Integer,
        ForeignKey('%s.id' % Image.__tablename__, ondelete='CASCADE'),
        nullable=False
    )
    image = relationship(
        Image,
        backref=backref('sizes', cascade='all, delete, delete-orphan')
    )

    @property
    def repr(self):
        return '<%s %s>' % (self.__class__.__name__, self.type)


class ImageErrorLog(IdMixin, TimestampMixin, Base):
    name = Column(String(40), nullable=False, index=True)
    description = Column(Text)
    image_id = Column(
        Integer,
        ForeignKey('%s.id' % Image.__tablename__, ondelete='CASCADE')
    )
    image = relationship(
        Image,
        backref=backref('error_logs', cascade='all, delete, delete-orphan')
    )

    @property
    def repr(self):
        return '<%s %s>' % (self.__class__.__name__, self.name)