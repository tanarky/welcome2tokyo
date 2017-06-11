# coding: utf-8
from flask import Flask, render_template, current_app
import os
from admin import app_admin
from models import Page, PagePhoto
from datetime import datetime
from google.appengine.ext import ndb

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']
app.debug = True
app.register_blueprint(app_admin)

def show_page(page_id):
    page = Page.get_by_id(page_id)
    # FIXME: check if published_at
    return render_template('pages_show.html', T={'page':page})

def show_pages(pages):
    return render_template('pages.html', T={'pages':pages})

@app.route('/')
def doc_root():
    pickups = Page().query(Page.page_type == 'article')
    pickups = pickups.filter(Page.is_pickup == True)
    pickups = pickups.filter(Page.published_at != None)
    pickups = pickups.filter(Page.published_at < datetime.now())
    pickups = pickups.order(-Page.published_at)

    pages = Page().query(Page.page_type == 'article')
    pages = pages.filter(Page.is_pickup == False)
    pages = pages.filter(Page.published_at != None)
    pages = pages.filter(Page.published_at < datetime.now())
    pages = pages.order(-Page.published_at)
    T = {'pages': pages, 'pickups': pickups}
    return render_template('pages_top.html', T=T)

@app.route('/p/<page_id>.html')
def show_pages_static(page_id):
    return show_page(page_id)

@app.route('/<int:year>/<int:month>/<page_id>.html')
def show_pages_article(year, month, page_id):
    return show_page(page_id)

@app.route('/search/label/<tag>')
def show_pages_tag(tag):
    pages = Page().query(Page.page_type == 'article')
    pages = pages.filter(Page.published_at != None)
    pages = pages.filter(Page.published_at < datetime.now())
    pages = pages.filter(Page.tags == tag)
    pages = pages.order(-Page.published_at)
    return show_pages(pages)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
