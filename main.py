from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from google.appengine.api import urlfetch
import base64, time

# Make sure you make a keys.py file with these
from keys import ACCOUNTSID, AUTHTOKEN, REALTIME_HOST

def baseN(num,b=36,numerals="0123456789abcdefghijklmnopqrstuvwxyz"): 
    return ((num == 0) and  "0" ) or (baseN(num // b, b).lstrip("0") + numerals[num % b])

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('main.html', locals()))
    
    def post(self):
        self.redirect('/%s' % baseN(abs(hash(time.time()))))

class LoungeHandler(webapp.RequestHandler):
    def get(self, lounge):
        self.response.out.write(template.render('lounge.html', {'realtime_host': REALTIME_HOST, 'lounge': lounge}))
    
    def post(self, lounge):
        if self.request.query_string == 'send':
            urlfetch.fetch('https://%s/boxlounge/%s' % (REALTIME_HOST,lounge), 
                method='POST', 
                headers={"Authorization": "Basic "+base64.b64encode('%s:%s' % (ACCOUNTSID, AUTHTOKEN))},
                payload=self.request.body)


def main():
    application = webapp.WSGIApplication([('/', MainHandler), ('/(.*)', LoungeHandler)], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
