
import webapp2
import json

import secure
import validcheck
import database
import head

### For templated document ###


class BasicHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return head.render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
### end of templated document ###

class Signup(BasicHandler):

    def get(self):
        user_cookie_str = self.request.cookies.get("user")
        if user_cookie_str:
            cookie_val = secure.check_secure_val(user_cookie_str)
            if cookie_val:
                self.redirect('/hw/welcome')
        self.render("signup-form.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)

        q = database.Users.all()

        if not validcheck.valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True
        else:
            q.filter("user =", username)
            if q.get():
                params['error_username'] = "The user already exists."
                have_error = True


        if not validcheck.valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not validcheck.valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            if email:
                a = database.Users(user = username, password = secure.hash_str(password), email = email)
            else:
                a = database.Users(user = username, password = secure.hash_str(password))
            a.put()
            new_cookie = secure.make_secure_val(username)
            self.response.headers.add_header('Set-Cookie','user='+str(new_cookie)+';Path=/hw/welcome')
            self.redirect('/hw/welcome')



class Welcome(BasicHandler):
    def get(self):
        user_cookie_str = self.request.cookies.get("user")
        if user_cookie_str:
            user = secure.check_secure_val(user_cookie_str)
            if user:
                self.render('welcome.html', username = user)
            else:
                self.redirect('/hw/signup')
        else:
            self.redirect('/hw/signup')

class Login(BasicHandler):
    def get(self):
        self.render("login-form.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        q = database.Users.all()
        q.filter("user =", username)
        li = q.get()

        if li != None and li.user == username and secure.hash_str(password) == li.password:
            new_cookie = secure.make_secure_val(username)
            self.response.headers.add_header('Set-Cookie','user='+str(new_cookie)+';Path=/hw/welcome')
            self.redirect('/hw/welcome')
        else:
            self.render("login-form.html", error = "Invalid login.")

class Logout(BasicHandler):
    def get(self):
        self.response.delete_cookie('user', path='/hw/welcome')
        self.redirect('/hw/signup')
        
##### blog stuff



class BlogFront(BasicHandler):
    def get(self):
        posts = database.db.GqlQuery("select * from Post order by created desc")
        self.render('front.html', posts = posts)

class PostPage(BasicHandler):
    def get(self, post_id):
        key = database.db.Key.from_path('Post', int(post_id), parent=database.blog_key())
        post = database.db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)

class NewPost(BasicHandler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = database.Post(parent = database.blog_key(), subject = subject, content = content)
            p.put()
            self.redirect('/hw/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)

class FrontJson(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type']='application/json'

        posts = database.db.GqlQuery("select * from Post order by created desc")
        l = []
        for p in posts:
            e = dict(content = p.content, created = p.created.strftime("%b %d, %Y"),
                last_modified = p.last_modified.strftime("%b %d, %Y"), subject = p.subject)
            l.append(e)
        jsontext = json.dumps(l)

        self.response.out.write(jsontext)

class PostJson(webapp2.RequestHandler):
    def get(self, post_id):
        self.response.headers['Content-Type']='application/json'

        key = database.db.Key.from_path('Post', int(post_id), parent=database.blog_key())
        post = database.db.get(key)
        e = dict(content = post.content, created = post.created.strftime("%b %d, %Y"),
                last_modified = post.last_modified.strftime("%b %d, %Y"), subject = post.subject)
        jsontext = json.dumps(e)

        self.response.out.write(jsontext)
        

class MainPage(BasicHandler):
  def get(self):
      self.write('Hello, Udacity!')

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/hw/signup', Signup),
                               ('/hw/welcome', Welcome),
                               ('/hw/login', Login),
                               ('/hw/logout', Logout),
                               ('/hw', BlogFront),
                               ('/hw/([0-9]+)', PostPage),
                               ('/hw/newpost', NewPost),
                               ('/hw/.json', FrontJson),
                               ('/hw/([0-9]+).json', PostJson)
                               ],
                              debug=True)
