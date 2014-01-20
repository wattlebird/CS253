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
import rot13
import cgi
import isvalid

form21 = """
<!DOCTYPE html>

<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%(userinput)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
"""

form22 = """
<!DOCTYPE html>

<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(usrname)s">
          </td>
          <td class="error">
            %(erruser)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password">
          </td>
          <td class="error">
            %(errpass)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify">
          </td>
          <td class="error">
            %(errpass2)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(erremail)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>
"""

def escape_html(s):
    return cgi.escape(s, quote = True)

class HW21Handler(webapp2.RequestHandler):
    def write_form(self, usertext="", ):
        self.response.out.write(form21 %{"userinput": escape_html(usertext)})
    
    def get(self):
        self.write_form()

    def post(self):
        originaltext = self.request.get("text")
        usertext = rot13.rot13(originaltext)
        self.write_form(usertext)


class HW22Handler(webapp2.RequestHandler):
    def write_form(self, usrname="", email="", erruser="", errpass="", errpass2="", erremail=""):
        self.response.out.write(form22 %{"usrname": escape_html(usrname),
                                         "email": escape_html(email),
                                         "erruser": escape_html(erruser),
                                         "errpass": escape_html(errpass),
                                         "errpass2": escape_html(errpass2),
                                         "erremail": escape_html(erremail)})

    def get(self):
        self.write_form()

    def post(self):
        valid = True

        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        if isvalid.valid_username(username)==None:
            valid = False
            usernameinfo = "That's not a valid username."
        else:
            usernameinfo = ""

        if isvalid.valid_password(password)==None:
            valid = False
            passwordinfo = "That wasn't a valid password."
            verifyinfo = ""
        elif password!=verify:
            valid = False
            passwordinfo = ""
            verifyinfo = "Your passwords didn't match."
        else:
            passwordinfo = ""
            verifyinfo = ""

        if email=="" or isvalid.valid_email(email)!=None:
            emailinfo=""
        else:
            emailinfo = "That's not a valid email."
            valid = False

        if valid==False:
            self.write_form(username, email, usernameinfo, passwordinfo, verifyinfo, emailinfo)
        else:
            self.redirect("/hw2-2/welcome?username=%s"%username) 

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.out.write("Welcome, %s!" %escape_html(username))

app = webapp2.WSGIApplication([
    ('/hw2-1', HW21Handler),
    ('/hw2-2', HW22Handler),
    ('/hw2-2/welcome', WelcomeHandler)
], debug=True)
