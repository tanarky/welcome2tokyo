# coding: utf-8
from flask import Flask, Blueprint, render_template, flash, redirect, url_for, current_app, request
import logging, sys, os, traceback
from datetime import datetime, tzinfo
from models import Page, PagePhoto
from google.appengine.ext import blobstore
from functools import wraps
from google.appengine.api import users

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
    return users.create_login_url('/admin/')
