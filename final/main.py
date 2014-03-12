#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import signup
import login
import secure
import database

class MainHandler(head.BasicHandler):
    def get(self, title):
        cookie_val = self.request.cookie.get('user')
        if cookie_val and secure.check_secure_val(cookie_val):
        	user = None
        else:
        	username = cookie_val.split('|')[0]
        	q = database.Users.query(Users.user == username)
        	user = q.get()

        q = database.Post.query(Post.title == title)
        if q.get():
        	self.render("page-form.html", user=user, content=q.get())
        elif user:
        	self.redirect('/_edit/%s'%title)
        else:
        	self.redirect('/login')

class EditHandler(head.BasicHandler):
	def get(self, title):
		cookie_val = self.request.cookie.get('user')
        if cookie_val and secure.check_secure_val(cookie_val):
        	user = None
        else:
        	username = cookie_val.split('|')[0]
        	q = database.Users.query(Users.user == username)
        	user = q.get()

        self.render("edit-form.html", )





app = webapp2.WSGIApplication([
	('/signup',signup.SignupHandler),
	('/login',login.LoginHandler),
    (r'/([:alaum:]*)', MainHandler),
    (r'/_edit/([:alaum:]*)',EditHandler),
    (r'/_history/([:alaum:]*)',HistoryHandler)
], debug=True)
