# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Hugo Santos Redondo (<hugosantosred@gmail.com>).
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
{
    'name': 'Dropbox Document Manager',
    'version': '1.0',
    'category': 'Document',
    "sequence": 14,
    'complexity': "easy",
    'description': """Dropbox Document Manager
    """,
    'author': 'Factor Libre',
    'website': '',
    'images': [],
    'depends': ['base'],
    'init_xml': [],
    'update_xml': [
        'wizard/dropbox_auth_app_view.xml',
        'wizard/dropbox_attach_file.xml',
        'wizard/dropbox_ir_attach.xml',
        'wizard/dropbox_download_file_view.xml',
        'ir_attachment_view.xml',
    ],
    'demo_xml': [],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: