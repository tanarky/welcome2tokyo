# coding: utf-8
from google.appengine.ext import ndb

class PagePhoto(ndb.Model):
    path = ndb.StringProperty()
    published_at = ndb.DateProperty()
    created_at   = ndb.DateTimeProperty(auto_now_add=True)

class Page(ndb.Model):
    title        = ndb.StringProperty()
    body         = ndb.TextProperty()
    tags         = ndb.StringProperty(repeated=True)
    photos       = ndb.StructuredProperty(PagePhoto, repeated=True)
    published_at = ndb.DateTimeProperty()
    page_type    = ndb.StringProperty(choices=['static', 'article'], default="article")
    updated_at   = ndb.DateTimeProperty(auto_now=True)
    created_at   = ndb.DateTimeProperty(auto_now_add=True)

