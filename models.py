# coding: utf-8
import re
from flask import current_app
from google.appengine.ext import ndb

class PagePhoto(ndb.Model):
    path = ndb.StringProperty()
    published_at = ndb.DateProperty()
    created_at   = ndb.DateTimeProperty(auto_now_add=True)

class Page(ndb.Model):
    title        = ndb.StringProperty()
    body         = ndb.TextProperty()
    tags         = ndb.StringProperty(repeated=True)
    thumbnail    = ndb.StringProperty()
    published_at = ndb.DateTimeProperty()
    page_type    = ndb.StringProperty(choices=['static', 'article'],
                                      default="article")
    is_pickup    = ndb.BooleanProperty(default=False)
    updated_at   = ndb.DateTimeProperty(auto_now=True)
    created_at   = ndb.DateTimeProperty(auto_now_add=True)

    def snippet(self):
        return self.body.split('<!-- pagebreak -->')[0]

    def permalink(self, full=False):
        domain = ""
        path   = "/p/%s.html" % self.key.urlsafe()
        if self.page_type == 'article':
            path = "/%04d/%02d/%s.html" % (self.published_at.year,
                                           self.published_at.month,
                                           self.key.id())
        if full:
            domain = ""
        return "%s%s" % (domain, path)
