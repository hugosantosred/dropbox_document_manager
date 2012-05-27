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

class dropbox_ir_attach(osv.osv_memory):
    _name = 'dropbox.ir.attach'

    _columns = {
        'name': fields.char('File Name', size=64),
        'file': fields.binary('File'),
        'state': fields.selection( 
            (('select_file', 'select_file'),
             ('send_file', 'send_file'))
        ),
    }

    _defaults = {
        'state': lambda *a: 'select_file',
    }

    def view_init(self, cr, uid, fields_list, context=None):
        if context is None:
            context = {}
        #Comprobamos que el usuario tiene Acceso a dropbox
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
                print dropbox_client.account_info()
                sess.unlink()
            except rest.ErrorResponse as http_resp:
                raise osv.except_osv(_('Warning !'),"%s" % http_resp)
        return False

    def dropbox_send_file(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        active_id = context.get('active_id', False)
        ir_att = self.pool.get('ir.attachment').browse(cr, uid, active_id)
        
        this = self.browse(cr, uid, ids)[0]
        attachment = this.file
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        try:
            sess = session.DropboxSession(config.APP_KEY, config.APP_SECRET, config.ACCESS_TYPE)
            sess.set_token(user.dropbox_token, user.dropbox_secret)
            dropbox_client = client.DropboxClient(sess)
            model_name = ir_att.res_model and ir_att.res_model.replace(".","_")
            file_path = '/%s/%s/%s/%s' % (cr.dbname, model_name, ir_att.res_id, this.name)
            resp = dropbox_client.put_file(file_path, base64.decodestring(attachment))
            self.pool.get('ir.attachment').write(cr, uid, ir_att.id, {'dropbox_path': resp['path'], 'dropbox_rev': resp['rev']})
            sess.unlink()

        except rest.ErrorResponse as http_resp:
                raise osv.except_osv(_('Error !'),"%s" % http_resp)

        return {'type': 'ir.actions.act_window_close'}

dropbox_ir_attach()