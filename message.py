import webapp2
import website

class MessageHandler(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/xml'

		message = self.request.get('m')
		self.response.write(website.render('message.xml', {'message': message}))

app = webapp2.WSGIApplication([
	('/message', MessageHandler),
], debug=True)
