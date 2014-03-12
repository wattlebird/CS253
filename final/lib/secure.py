import hashlib
import hmac
import string
import random

SECRET = scut

def hash_str(s):
	return hmac.new(s,SECRET).hexdigest()

def make_secure_val(s):
        return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
        val = h.split('|')[0]
        if h == make_secure_val(val):
                return val

def make_salt():
	return ''.join(random.choice(string.letters) for x in xrange(5))

def hashed_password(user, pw, salt = None):
	if salt == None:
		salt = make_salt()
	h = hashlib.sha256(user + pw + salt).hexdigest()
	return '%s|%s' % (h, salt)

def check_password(user, pw, h):
	salt = h.split('|')[1]
	return h == hashed_password(name, pw, salt)