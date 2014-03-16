from google.appengine.ext import ndb
import head

def user_key():
    return ndb.Key('Users','default')

class Users(ndb.Model):
    user = ndb.StringProperty(required = True)
    hashed_password = ndb.StringProperty(required = True)
    email = ndb.StringProperty()





class Post(ndb.Model):
    title = ndb.StringProperty(required = True)
    body = ndb.TextProperty(required = True)
    version = ndb.IntegerProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)

