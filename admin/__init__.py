# coding: utf-8
from flask import Flask, Blueprint, render_template, flash, redirect, url_for, current_app, request, jsonify
import logging, sys, os, traceback
from datetime import datetime, tzinfo
from models import Page, PagePhoto
from google.appengine.ext import blobstore
from functools import wraps
import helper

app_admin = Blueprint('app_admin', __name__, url_prefix='/admin')

@app_admin.route('/401.html')
def admin_401():
    T = {'admin_login_url': helper.admin_login_url()}
    return render_template('admin_401.html', T=T)

@app_admin.route('/login_callback', methods=['GET'])
@helper.admin_required
def login_callback(user):
    flash('login successfully', 'success')
    return redirect(url_for('app_admin.top'))

@app_admin.route('/', methods=['GET'])
@helper.admin_required
def top(user):
    T = {'user': user}
    return render_template('admin_top.html', T=T)

@app_admin.route('/pages', methods=['GET'])
@helper.admin_required
def pages(user):
    pages = Page().query(Page.page_type == 'article').order(-Page.updated_at)
    T = {'user': user,
         'pages': pages}
    return render_template('admin_pages.html', T=T)

@app_admin.route('/pages/new', methods=['GET'])
@helper.admin_required
def pages_new(user):
    T = {'user': user}
    return render_template('admin_pages_new.html', T=T)

@app_admin.route('/pages/<page_id>/edit', methods=['GET'])
@helper.admin_required
def pages_edit(user, page_id):
    p = Page().get_by_id(int(page_id))
    img_upload_url = url_for('app_admin.page_images_upload',
                             page_id=page_id)
    imgs = helper.get_page_imgs(page_id)
    T = {'page':p,
         'img_upload_url': img_upload_url,
         'imgs': imgs,
         'user': user}
    return render_template('admin_pages_edit.html', T=T)

@app_admin.route('/pages/<page_id>/image_list', methods=['GET'])
@helper.admin_required
def pages_image_list(user, page_id):
    p = Page().get_by_id(int(page_id))
    imgs = helper.get_page_imgs(page_id)
    return jsonify(imgs)

@app_admin.route('/pages/<page_id>', methods=['POST'])
@helper.admin_required
def pages_update(user, page_id):
    try:
        p = Page().get_by_id(int(page_id))
        p.title     = request.form.get('title')
        p.body      = request.form.get('body')
        p.page_type = request.form.get('page_type')
        p.tags      = request.form.get('tags',"").split(",")
        p.thumbnail = request.form.get('thumbnail')
        if request.form.get('published_at') and request.form.get('published_at') != '':
            d = datetime.strptime(request.form.get('published_at'),
                                  '%Y-%m-%d %H:%M:%S')
            p.published_at = d
        p.put()
        flash('page updated', 'success')
    except Exception as e:
        current_app.logger.info(e)
        flash('page save error', 'error')
    return redirect(url_for('app_admin.pages_edit', page_id=page_id))

@app_admin.route('/pages/create', methods=['POST'])
@helper.admin_required
def pages_create(user):
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
@helper.admin_required
def page_images_upload(user, page_id):
    try:
        p = Page().get_by_id(int(page_id))
        f = request.files['image']
        current_app.logger.info(f)
        current_app.logger.info(f.filename)
        current_app.logger.info(f.content_type)
        helper.save_page_img(page_id, f.filename,
                             f.read(), f.content_type)
        flash('page image uploaded', 'success')
    except Exception as e:
        current_app.logger.info(e)
        flash('page save error', 'error')
    return redirect(url_for('app_admin.pages_edit', page_id=page_id))

