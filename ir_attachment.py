# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Hugo Santos (<hugosantosred@gmail.com>).
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
from osv import osv, fields

class ir_attachment(osv.osv):
	_inherit = 'ir.attachment'

	_columns = {
		'type': fields.selection(
                [ ('url','URL'), ('binary','Binary'), ('dropbox', 'Dropbox')],
                'Type', help="Binary File or external URL", required=True, change_default=True),
        'dropbox_path': fields.char('File', size=255, readonly=True),
        'dropbox_rev': fields.char('Revision', size=64, readonly=True),
	}

ir_attachment()