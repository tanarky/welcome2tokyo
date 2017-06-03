# coding: utf-8
from flask import Blueprint, render_template, flash, redirect, url_for, current_app, request
import logging, sys, os, traceback
from datetime import datetime, tzinfo
from models import Page, PagePhoto
from google.appengine.ext import blobstore

app_admin = Blueprint('app_admin', __name__, url_prefix='/admin')

@app_admin.route('/', methods=['GET'])
def top():
    return render_template('admin_top.html')

@app_admin.route('/pages', methods=['GET'])
def pages():
    pages = Page().query(Page.page_type == 'article').order(-Page.updated_at)
    return render_template('admin_pages.html', T={'pages':pages})

@app_admin.route('/pages/new', methods=['GET'])
def pages_new():
    return render_template('admin_pages_new.html', T={})

@app_admin.route('/pages/<page_id>/edit', methods=['GET'])
def pages_edit(page_id):
    p = Page().get_by_id(int(page_id))
    img_upload_url = blobstore.create_upload_url(url_for('app_admin.page_images_upload', page_id=page_id))
    current_app.logger.info(img_upload_url)
    return render_template('admin_pages_edit.html', T={'page':p,
                                                       'img_upload_url': img_upload_url})

@app_admin.route('/pages/<page_id>', methods=['POST'])
def pages_update(page_id):
    try:
        p = Page().get_by_id(int(page_id))
        p.title     = request.form['title']
        p.body      = request.form['body']
        p.page_type = request.form['page_type']
        if request.form['published_at'] and request.form['published_at'] != '':
            d = datetime.strptime(request.form['published_at'],
                                  '%Y-%m-%d %H:%M:%S')
            p.published_at = d
        p.put()
        flash('page updated', 'success')
    except Exception as e:
        current_app.logger.info(e)
        flash('page save error', 'error')
    return redirect(url_for('app_admin.pages_edit', page_id=page_id))

@app_admin.route('/pages/create', methods=['POST'])
def pages_create():
    try:
        p = Page(
            title=request.form['title'],
            body=request.form['body'],
            page_type=request.form['page_type'],
        )
        p.put()
        flash('page created', 'success')
        return redirect(url_for('app_admin.pages_edit', page_id=p.key.id()))
    except Exception as e:
        current_app.logger.info(e)
        flash('page save error', 'error')
    return redirect(url_for('app_admin.pages'))

@app_admin.route('/pages/<page_id>/images', methods=['POST'])
def page_images_upload(page_id):
    try:
        p = Page().get_by_id(int(page_id))
        f = request.files
        current_app.logger.info(f)
        flash('page image uploaded', 'success')
    except Exception as e:
        current_app.logger.info(e)
        flash('page save error', 'error')
    return redirect(url_for('app_admin.pages_edit', page_id=page_id))
