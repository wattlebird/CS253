from google.appengine.api import memcache
import time
import database
import string

timer = time.time()
per_timer={}

def top_articles(refresher = False):
	global timer
	key = 'top'
	post = memcache.get(key)
	if post == None or refresher:
		q = database.db.GqlQuery("select * from Post ORDER BY created DESC")
		post = list(q)
		timer = time.time()
		memcache.set('top', post)

	return post

def per_article(key, refresher = False):
	global per_timer
	key = str(key)
	post = memcache.get(key)
	if post == None or refresher:
		post = database.db.get(key)
		per_timer[key]=time.time()
		memcache.set(key, post)
	return post