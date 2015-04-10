# -*- coding:utf-8 -*-
"""
    This module provides configurations. Secret data is stored in `secret` module.
    :secret.DATABASE_USERNAME: A username for database
    :secret.DATABASE_PASSWORD: A password for database.
    :secret.DATABASE: A name for database.
"""
import secret

SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@localhost/%s' % (
    secret.DATABASE_USERNAME,
    secret.DATABASE_PASSWORD,
    secret.DATABASE
)