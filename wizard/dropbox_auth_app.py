# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 (<hugosantosred@gmail.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from dropbox import client, rest, session
from oauth import oauth

from osv import osv, fields

APP_KEY = '70n6j9ap5opwpcm'
APP_SECRET = 'tzarefzm4a2wu6p'
ACCESS_TYPE = 'app_folder'

class session_token:
	def __init__(self, *args):
		self.sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
		self.request_token = self.sess.obtain_request_token()

class dropbox_auth_app(osv.osv_memory):
	_name = 'dropbox.auth.app'

	def _get_default_state(self, cr, uid, context=None):
		if context is None:
			context = {}
		state = 'start'
		user = self.pool.get('res.users').browse(cr, uid, uid)
		#Todo: Check real authentication state
		if user.dropbox_token and user.dropbox_secret:
			state = 'done'
		return state


	_columns = {
		'auth_url': fields.char('Auth Url', size=255),
		'oauth_secret': fields.char('Secret', size=255),
		'oauth_token': fields.char('Oauth Token', size=255),
		'access_token': fields.char('Access Token', size=255),
		'state': fields.selection( ( ('start','start'),   
                                     ('confirm','confirm'),
                                     ('done','done')
                                       ) ),
	}

	_defaults = {
		'state': _get_default_state,
	}

	def generate_auth_url(self, cr, uid, ids, context=None):
		sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
		request_token = sess.obtain_request_token()
		url = sess.build_authorize_url(request_token)
		return self.write(cr, uid, ids, {'auth_url': url, 'state': 'confirm',
			'oauth_secret': request_token.secret, 'oauth_token': request_token.key})
		#Login
		#sess.set_token(key,secret)

	def set_token_to_user(self, cr, uid, ids, context=None):
		this = self.browse(cr, uid, ids)[0]
		sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
		request_token = oauth.OAuthToken(this.oauth_token, this.oauth_secret)
		access_token = sess.obtain_access_token(request_token)
		if access_token:
			self.pool.get('res.users').write(cr, uid, [uid],
				{'dropbox_token': access_token.key, 'dropbox_secret': access_token.secret})
			return self.write(cr, uid, ids, {'state': 'done'})


dropbox_auth_app()