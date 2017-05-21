# coding: utf-8
from google.appengine.ext import ndb

class BlogArticle(ndb.Model):
    title        = ndb.StringProperty()
    body         = ndb.TextProperty()
    tags         = ndb.StringProperty(repeated=True)
    published_at = ndb.DateProperty()
    created_at   = ndb.DateTimeProperty(auto_now_add=True)
