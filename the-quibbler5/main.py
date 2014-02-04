import os
import webapp2
import jinja2

import secure
import validcheck
import database

### For templated document ###
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BasicHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
### end of templated document ###

class Signup(BasicHandler):

    def get(self):
        user_cookie_str = self.request.cookies.get("user")
        if user_cookie_str:
            cookie_val = secure.check_secure_val(user_cookie_str)
            if cookie_val:
                self.redirect('/hw4/welcome')
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
            self.response.headers.add_header('Set-Cookie','user='+str(new_cookie)+';Path=/hw4/welcome')
            self.redirect('/hw4/welcome')



class Welcome(BasicHandler):
    def get(self):
        user_cookie_str = self.request.cookies.get("user")
        if user_cookie_str:
            user = secure.check_secure_val(user_cookie_str)
            if user:
                self.render('welcome.html', username = user)
            else:
                self.redirect('/hw4/signup')
        else:
            self.redirect('/hw4/signup')

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
            self.response.headers.add_header('Set-Cookie','user='+str(new_cookie)+';Path=/hw4/welcome')
            self.redirect('/hw4/welcome')
        else:
            self.render("login-form.html", error = "Invalid login.")

class Logout(BasicHandler):
    def get(self):
        self.response.delete_cookie('user', path='/hw4/welcome')
        self.redirect('/hw4/signup')
        

class MainPage(BasicHandler):
  def get(self):
      self.write('Hello, Udacity!')

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/hw4/signup', Signup),
                               ('/hw4/welcome', Welcome),
                               ('/hw4/login', Login),
                               ('/hw4/logout', Logout)
                               ],
                              debug=True)
