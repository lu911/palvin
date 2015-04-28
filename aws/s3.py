# -*- coding:utf-8 -*-
import os

from boto.s3.connection import S3Connection, S3ResponseError, Location
from boto.s3.key import Key

from palvin.config import (
    AWS_ACCESS_KEY,
    AWS_SECRET_ACCESS_KEY,
    AWS_S3_BUCKET_NAME
)
from utils import get_uuid


conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)
try:
    bucket = conn.get_bucket(AWS_S3_BUCKET_NAME)
except S3ResponseError, e:
    if e.status == 404:
        bucket = conn.create_bucket(
            AWS_S3_BUCKET_NAME,
            location=Location.APNortheast
        )
    else:
        # TODO handling error.
        pass


def file_upload(file_, path='/', filename=get_uuid()):
    global bucket

    if not bucket:
        return None

    file_.seek(0)
    filename = os.path.join(path, filename)
    k = Key(bucket)
    k.key = filename
    k.set_contents_from_file(file_)
    return filename


def get_uploaded_filename():
    pass