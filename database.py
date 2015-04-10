# -*- coding:utf-8 -*-
"""
    This module provides configurations. Secret data is stored in `secret` module.
    :secret.DATABASE_USERNAME: A username for database
    :secret.DATABASE_PASSWORD: A password for database.
    :secret.DATABASE: A name for database.
"""
try:
    import secret
except ImportError:
    raise ImportError("Secret module doesn't exist in 'palvin'")

import datetime

from sqlalchemy import create_engine, Column, BigInteger, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class IdMixin(object):
    """
    Provides the :attr:`id` primary key column
    """
    #: Database identity for this model, used for foreign key
    #: references from other models
    id = Column(BigInteger, primary_key=True)


class TimestampMixin(object):
    """
    Provides the :attr:`created_at` and :attr:`updated_at` audit timestamps
    """
    #: Timestamp for when this instance was created, in UTC
    created_at = Column(
        DateTime,
        default=datetime.datetime.now,
        nullable=False
    )
    #: Timestamp for when this instance was last updated (via the app), in UTC
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False
    )


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    @classmethod
    def query(cls):
        return db_session.query(cls)

    @classmethod
    def get(cls, _id):
        if any((isinstance(_id, basestring) and _id.isdigit(),
                isinstance(_id, (int, float))),):
            return cls.query.get(int(_id))
        return None

    @classmethod
    def get_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def get_or_create(cls, **kwargs):
        r = cls.get_by(**kwargs)
        if not r:
            r = cls(**kwargs)
            db_session.add(r)
        return r

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save(commit=commit) or self

    def save(self, commit=False):
        db_session.add(self)
        if commit:
            try:
                db_session.commit()
            except Exception:
                db_session.rollback()
                raise
        return self

    def delete(self, commit=True):
        db_session.delete(self)
        return commit and db_session.commit()


class PalvinBase(CRUDMixin, object):

    @declared_attr
    def __tablename__(cls):
        import inflect

        p = inflect.engine()
        modules = cls.__module__.split('.')
        modules[-1] = p.plural(modules[-1])
        exclude_modules = ['palvin', 'models']
        return '_'.join(list(set(modules) - set(exclude_modules)))


SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@localhost/%s' % (
    secret.DATABASE_USERNAME,
    secret.DATABASE_PASSWORD,
    secret.DATABASE
)

engine = create_engine(SQLALCHEMY_DATABASE_URI,
                       convert_unicode=True)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=engine
    )
)

Base = declarative_base(cls=PalvinBase)
Base.query = db_session.query_property()

