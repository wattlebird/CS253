import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Post(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    time = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class FrontPageHandler(Handler):
    def get(self):
        posts = db.GqlQuery("Select * from Post order by time desc")
        self.render("front.html", posts = posts)

class NewPostHandler(Handler):
    def get(self):
        self.render("newpost.html", title="", blog="", error="")

    def post(self):
        title = self.request.get("subject")
        blog = self.request.get("content")

        if title and blog:
            a = Post(title = title, content = blog)
            a.put()
            self.redirect("/hw3/%d" %a.key().id())
        else:
            error = "Blog submit failed."
            self.render("newpost.html", title = title, blog = blog, error = error)
            

class ArticleHandler(Handler):
    def get(self, article_id):
        post = Post.get_by_id(int(article_id))
        self.render("entity.html", title = post.title, time = post.time, content= post.content)

app = webapp2.WSGIApplication([('/hw3', FrontPageHandler),
                               ('/hw3/newpost', NewPostHandler),
                               (r'/hw3/(\d+)', ArticleHandler)
                               ],debug=True)
