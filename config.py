# -*- coding:utf-8 -*-
"""
    Secret data is stored in `secret` module.
    :secret.DATABASE_USERNAME: A username for database
    :secret.DATABASE_PASSWORD: A password for database.
    :secret.DATABASE: A name for database.
"""
try:
    import secret
except ImportError:
    raise ImportError("Secret module doesn't exist in 'palvin'")


SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://%s:%s@localhost/%s' % (
    secret.DATABASE_USERNAME,
    secret.DATABASE_PASSWORD,
    secret.DATABASE
)

AWS_ACCESS_KEY = secret.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = secret.AWS_SECRET_ACCESS_KEY
AWS_S3_BUCKET_NAME = 'palvin'


try:
    from local_config import *
except ImportError:
    pass
