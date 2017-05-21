# coding: utf-8
from flask import Blueprint, render_template
import logging, sys, os, traceback
from models import BlogArticle

app_admin = Blueprint('app_admin', __name__, url_prefix='/admin')

@app_admin.route('/', methods=['GET'])
def top():
    BlogArticle.query().fetch()
    #b = BlogArticle(
    #    id = "1",
    #    title = "テストタイトル",
    #    body  = "本文 あああ いいい",
    #    tags = ["小田急線", "世田谷線"],
    #    published_at = None
    #)
    #b.put()
    return render_template('admin_top.html')
