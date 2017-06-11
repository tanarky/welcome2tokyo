# coding: utf-8
from flask import Flask, render_template
import os
from admin import app_admin
from google.appengine.ext import ndb

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']
app.debug = True
app.register_blueprint(app_admin)

@app.route('/')
def doc_root():
    return render_template('pages_top.html')

@app.route('/p/<page_key>.html')
def show_page(page_key):
    page = ndb.Key(urlsafe=page_key).get()
    return render_template('pages_show.html', T={'page':page})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
