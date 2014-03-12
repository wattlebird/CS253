import head
import validcheck
import secure
import webapp2

class LoginHandler(head.BasicHandler):
	def get(self):
		cookie_val = self.request.cookies.get('user')
		if cookie_val:
			if secure.check_secure_val(cookie_val):
				self.redirect('/')
		self.render("login-form.html")

	def post(self):
		have_error = False
		username = self.request.get('username')
		password = self.request.get('password')

		if not validcheck.valid_username(username):
            have_error = True
        else:
          	q = database.Users.query(Users.user == username)
           	if not q.get():
           		have_error = True
           	else:
           		hashvalue = q.get().hashed_passedword

        if not validcheck.valid_password(password):
           	have_error = True
        elif not secure.check_password(username, password, hashvalue):
        	have_error = True


        if have_error:
        	self.render('login-form.html', error = 'Login failed!')
        else:
        	cookie_val = secure.make_secure_val(username)
            self.response.set_cookie('user', cookie_val)
            self.redirect('/')

