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
from dropbox_document_manager import dropbox_config as config
from dropbox_document_manager.dropbox import client, rest, session
import base64

from osv import osv, fields

class dropbox_download_file(osv.osv_memory):
    _name = 'dropbox.download.file'
    _columns = {
        'name': fields.char('File name', size=255),
        'file': fields.binary('File', readonly=True)
    }
    
    def default_get(self, cr, uid, fields_list, context=None):
        if context is None:
            context = {}
        if context.get('active_model', False) and context.get('active_id', False):
            obj = self.pool.get(context['active_model']).browse(cr, uid, context.get('active_id'))
            if obj.dropbox_path:
                user = self.pool.get('res.users').browse(cr, uid, uid, context=context)

                active_id = context.get('active_id', False)
        
                if not user.dropbox_token or not user.dropbox_secret:
                    raise osv.except_osv(_('Warning !'),"You can not upload files if you didn't give OpenERP\
         access to your dropbox account")
                else:
                    try:
                        sess = session.DropboxSession(config.APP_KEY, config.APP_SECRET, config.ACCESS_TYPE)
                        sess.set_token(user.dropbox_token, user.dropbox_secret)
                        dropbox_client = client.DropboxClient(sess)
                        file, metadata = dropbox_client.get_file_and_metadata(obj.dropbox_path)
                        return {'file': base64.b64encode(file.read()), 'name': metadata['path'].split('/')[-1]}
                        sess.unlink()                        
                    except rest.ErrorResponse as http_resp:
                        raise osv.except_osv(_('Warning !'),"%s" % http_resp)
            else:
                raise osv.except_osv(_('Error !'), _('You must upload a file to dropbox first'))                    
                    
        return {}
        
dropbox_download_file()