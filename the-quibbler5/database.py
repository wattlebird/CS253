from google.appengine.ext import db
import head

class Users(db.Model):
    user = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.EmailProperty()

    
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)


class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return head.render_str("post.html", p = self)