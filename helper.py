# coding: utf-8
from flask import Flask, Blueprint, render_template, flash, redirect, url_for, current_app, request
import logging, sys, os, traceback
import cloudstorage
from datetime import datetime, tzinfo
from models import Page, PagePhoto
from google.appengine.ext import blobstore
from functools import wraps
from google.appengine.api import users
from google.appengine.api import app_identity

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = users.get_current_user()
        if user and users.is_current_user_admin():
            kwargs['user'] = {
                'email': user,
                'logout_url': users.create_logout_url('/')
            }
            return f(*args, **kwargs)
        return redirect(url_for('app_admin.admin_401'))
    return decorated_function

def admin_login_url():
    return users.create_login_url(url_for('app_admin.login_callback'))

def get_bucket_name():
    return os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())

def get_page_imgs(page_id, bucket=None):
    if not bucket:
        bucket = get_bucket_name()

    ret = []
    page_size = 100
    prefix = "/".join(['', bucket, 'img', str(page_id), ''])
    current_app.logger.info(prefix)
    stats = cloudstorage.listbucket(prefix, max_keys=page_size)
    while True:
        count = 0
        for stat in stats:
            count += 1
            ret.append(img_full_url(stat.filename))

        if count != page_size or count == 0:
            break
        stats = cloudstorage.listbucket(prefix,
                                        max_keys=page_size,
                                        marker=stat.filename)
    return ret

def is_development():
    return os.environ["SERVER_NAME"] in ("localhost")

def img_full_url(img_path):
    if is_development():
        return 'http://localhost:8080/_ah/gcs%s' %img_path
    else:
        return 'https://storage.googleapis.com%s' % img_path

def save_file(name, body, content_type, bucket=None):
    if not bucket:
        bucket = get_bucket_name()
    filename = "/".join(['', bucket, name])
    current_app.logger.info(filename)
    write_retry_params = cloudstorage.RetryParams(backoff_factor=1.1)
    with cloudstorage.open(
            filename, 'w',
            content_type=content_type,
            options={},
            retry_params=write_retry_params) as cloudstorage_file:
        cloudstorage_file.write(body)

def save_page_img(page_id, name, body, content_type, bucket=None):
    path = "/".join(["img", str(page_id), name])
    save_file(path, body, content_type, bucket)
