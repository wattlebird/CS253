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
import head
import secure
import database



class MainHandler(head.BasicHandler):
    def get(self, title):
        global current_title
        current_title = title
        cookie_val = self.request.cookies.get('user')
        if not cookie_val or not secure.check_secure_val(cookie_val):
            user = None
        else:
            username = cookie_val.split('|')[0]
            q = database.Users.query(database.Users.user == username)
            user = q.get()

        cookie_page = secure.make_secure_val(title)
        self.response.set_cookie('prev', cookie_page)

        version_str = self.request.get('v')
        if version_str:
            version_num = int(version_str)
        else: 
            version_num = None

        q = database.Post.query(database.Post.title == title)
        q = q.order(-database.Post.version)

        if q.count()!=0:
            if version_num:#This requires version_num MUST be valid!!!!!
                for item in q:
                    if item.version == version_num:
                        self.render("page-form.html", user=user, content=item)
                        break
            else:
        	self.render("page-form.html", user=user, content=q.get())
        else:
            if user:
        	self.redirect('/_edit/%s'%title)
            else:
        	self.redirect('/login')

class EditHandler(head.BasicHandler):

    def get(self, title):
        global current_title
        current_title = title
	cookie_val = self.request.cookies.get('user')
        #cookie_page = secure.make_secure_val(title)
        #self.response.set_cookie('prev', cookie_page)
        if not(cookie_val and secure.check_secure_val(cookie_val)):
            user = None
        else:
            username = cookie_val.split('|')[0]
            q = database.Users.query(database.Users.user == username)
            user = q.get()

        if not user:
            self.redirect('/%s'%title)

        q = database.Post.query(database.Post.title == title)
        if q.count() == 0:
            e = database.Post(title = title,
                              body = '',
                              version = 0)
            e.put()
        else:
            q = q.order(-database.Post.version)
            e = q.get()
        self.render("edit-form.html", user = user, content = e, title = title)

    def post(self, title):
        body = self.request.get('content')
        cookie_page = self.request.cookies.get('prev')
        if cookie_page and secure.check_secure_val(cookie_page):
            title = cookie_page.split('|')[0]
        else:
            title = current_title
        q = database.Post.query(database.Post.title == current_title).order(-database.Post.version)
        e = q.get()
        if e:
            new_e = database.Post(title = title, body = body, version = e.version+1)
        else:
            new_e = database.Post(title = title, body = body, version = 1)
        new_e.put()
        self.redirect('/%s'%title)

class HistoryHandler(head.BasicHandler):
    def get(self, title):
        return




app = webapp2.WSGIApplication([
    (r'/_edit/([A-Za-z0-9_\?]*)',EditHandler),
    (r'/_history/([A-Za-z0-9_\?]*)',HistoryHandler),
    (r'/([A-Za-z0-9_\?]*)', MainHandler)
], debug=True)
