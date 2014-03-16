import head
import validcheck
import secure
import database
import webapp2

class LoginHandler(head.BasicHandler):
	def get(self):
		cookie_val = self.request.cookies.get('user')
		cookie_page = self.request.cookies.get('prev')
                if cookie_val and secure.check_secure_val(cookie_val):
                        if secure.check_secure_val(cookie_page):
                                previous_page = cookie_page.split('|')[0]
                                self.redirect('/%s'%previous_page)
                        else:
                                self.redirect('/')
		self.render("login-form.html")

	def post(self):
		have_error = False
		username = self.request.get('username')
		password = self.request.get('password')

                hashvalue = None
		if not validcheck.valid_username(username):
                	have_error = True
                else:
                        q = database.Users.query(database.Users.user == username)
                        if not q.get():
                                have_error = True
                        else:
                                hashvalue = q.get().hashed_password

                if not validcheck.valid_password(password) or not hashvalue:
                        have_error = True
                elif not secure.check_password(username, password, hashvalue):
                        have_error = True


                if have_error:
                        self.render('login-form.html', error = 'Login failed!')
                else:
                        cookie_val = secure.make_secure_val(username)
                        self.response.set_cookie('user', cookie_val)
                        cookie_page = self.request.cookies.get('prev')
                        if cookie_page and secure.check_secure_val(cookie_page):
                                self.redirect('/%s'%cookie_page.split('|')[0])
                        else:
                                self.redirect('/')


class LogoutHandler(head.BasicHandler):
        def get(self):
                self.response.delete_cookie('user')
                cookie_page = self.request.cookies.get('prev')
                if cookie_page and secure.check_secure_val(cookie_page):
                        self.redirect('/%s'%cookie_page.split('|')[0])
                else:
                        self.redirect('/')

app = webapp2.WSGIApplication([
        ('/login',LoginHandler),
        ('/logout', LogoutHandler)
], debug=True)
