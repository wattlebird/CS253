import head
import validcheck
import secure
import webapp2

class SignupHandler(head.BasicHandler):
        def get(self):
                cookie_val = self.request.cookies.get('user')
                if cookie_val:
	               if secure.check_secure_val(cookie_val):
		              self.redirect('/')
                self.render("signup-form.html")
	
        def post(self):
        	have_error = False
        	username = self.request.get('username')
                password = self.request.get('password')
                verify = self.request.get('verify')
                email = self.request.get('email')

                param = dict(username = username,
                	email = email)

                if not validcheck.valid_username(username):
                	have_error = True
                	param['error_username'] = 'Invalid Username'
                else:
                	q = database.Users.query_users('user == %s'%username)
                	if q.get():
                		have_error = True
                		param['error_username'] = 'User already exists'

                if not validcheck.valid_password(password):
                	have_error = True
                	param['error_password'] = 'Invalid Password'
                else:
                	if password != verify
                	have_error = True
                	param['error_verify']= 'Passwords didn\'t match.'

                if not valid_email(email):
                	have_error = True
                	param['error_email'] = 'Invalid Email'

                if have_error:
                	self.render("signup-form.html", **param)
                else:
                	if email:
                		kk = database.User(user = username, hashed_password = secure.hashed_password(username, password),
                			email = email)	
                	else:
                		kk = database.User(user = username, hashed_password = secure.hashed_password(username, password))
                	kk.put()
                	cookie_val = secure.make_secure_val(username)
                	self.response.set_cookie('user', cookie_val)
                        self.redirect('/')


