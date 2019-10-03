import base64
import cgi
import json
import os
import urllib
import webapp2

import logging

import website # Contains jinja2 boilerplate

from google.appengine.api import urlfetch

def verifyHuman(recaptchaResponse, remoteIp):
	if (recaptchaResponse):
		apiUrl = "https://www.google.com/recaptcha/api/siteverify"
		apiPayload = urllib.urlencode({
			"secret": os.environ['recaptcha_secret'],
			"response": recaptchaResponse,
			"remoteip": remoteIp
			})

		apiResponse = urlfetch.fetch(
			url=apiUrl,
			payload=apiPayload,
			method=urlfetch.POST,
			headers={'Content-Type': 'application/x-www-form-urlencoded'}
			)

		apiResponseJson = json.loads(apiResponse.content)
		return apiResponseJson["success"]
	else:
		return False

class MainHandler(webapp2.RequestHandler):
	def get(self):
		variables = {"title": "Leave a message", "recaptcha_site": os.environ['recaptcha_site']};

		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(website.render('index.html', variables))

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		isHuman = verifyHuman(cgi.escape(self.request.get('g-recaptcha-response')), self.request.remote_addr)
		if isHuman: # Verify reCAPTCHA passed, then send API request to Twilio to call IP phone
			apiUrl = "https://api.twilio.com/2010-04-01/Accounts/AC367d2a164f1e3d88d000e19fd9acb209/Calls.json"
			apiPayload = urllib.urlencode({
				"Url": "https://leaveamessage.victorli.co/message?" + urllib.urlencode({'m': self.request.get('message')}),
				"To": cgi.escape(self.request.get('recipient')),
				"From": os.environ['caller_id']
				})

			apiResponse = urlfetch.fetch(
				url=apiUrl,
				payload=apiPayload,
				method=urlfetch.POST,
				headers={'Content-Type': 'application/x-www-form-urlencoded',
					'Authorization': "Basic %s" % base64.b64encode(
						os.environ['twilio_sid'] + ':' + os.environ['twilio_secret']
					)}
			)

			apiResponseJson = json.loads(apiResponse.content)
			if apiResponseJson["status"] == 'queued': # Call to IP phone successful
				self.response.write(website.render('note.html', {"message": "Your message has been sent!"}))
			else:
				self.response.write(website.render('note.html', {"message": "Internal error."}))
				logging.debug	
		else: # reCAPTCHA failed
			self.response.write(website.render('note.html', {"message": "Please try the reCAPTCHA again."}))

app = webapp2.WSGIApplication([
	('/', MainHandler),
], debug=True)