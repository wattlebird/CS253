import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PSWD_RE = re.compile(r"^.{3,20}$")
MAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(pswd):
    return PSWD_RE.match(pswd)

def valid_email(email):
    return MAIL_RE.match(email)
