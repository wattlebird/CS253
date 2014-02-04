from google.appengine.ext import db

class Users(db.Model):
    user = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.EmailProperty()

    