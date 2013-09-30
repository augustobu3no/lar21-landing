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
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'mailchimp-api-python'))

import webapp2
import urllib
from google.appengine.ext import ndb
from webapp2_extras import sessions
import jinja2
import webapp2
import json
import mailchimp

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'intestinopolis',
}


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


class DadosUsuario(ndb.Model):
	"""Models an individual Guestbook entry with content and date."""
	email = ndb.StringProperty()
	header = ndb.TextProperty()
	ip = ndb.StringProperty()
	time = ndb.DateTimeProperty(auto_now_add = True)

class DadosUsuarioPago(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    email = ndb.StringProperty()
    header = ndb.TextProperty()
    ip = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now_add = True)

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()
	
class MainHandler(BaseHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        params = {}
        params["email"] = self.session.get('email')
        self.response.write(template.render(params))

    def post(self):
    	email = self.request.get('email')
    	header = self.request.headers
    	ip =  self.request.remote_addr
    	inscricao = DadosUsuarioPago()
    	inscricao.ip = ip
    	inscricao.header = str(header)
    	inscricao.email = email
    	inscricao.put()
    	self.session['email'] = True
        chimp = mailchimp.Mailchimp('456c1fce8056e32998beef28653b47d0-us7')
        chimp.lists.subscribe('d5ab1e71b7', {'email':email}, merge_vars={'mc_language':'pt'})
    	self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], config=config, debug=True)
