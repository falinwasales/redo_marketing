# -*- coding: utf-8 -*-
# Part of Odoo Falinwa Edition. See LICENSE file for full copyright and licensing details.
{
    "name": "ACC: Bank Statement Reconciliation Ext",
    "version": "13.0.1.0.0",
    'license': 'OPL-1',
    'summary': "Extend bank statement reconciliation.",
    'sequence': 36,
    'category': 'Accounting',
    'author': 'CLuedoo',
    'website': 'https://www.cluedoo.com',
    'support': 'cluedoo@falinwa.com',
    "description": """
        Module to extend bank statement reconciliation
        =======================================================
    """,
    "depends": ['account'],
    'init_xml': [],
    'data': [
        # javascript still not working
        # 'views/assets.xml',
        'views/account_bank_statement_reconciliation_view.xml',
    ],
    'images': [
        'static/description/absr-image2_screenshot.png'
    ],
    'demo': [],
    'css': [],
    'js': [
    ],
    'installable': True,
    'active': False,
    'price': 270.00,
    'currency': 'EUR',
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
