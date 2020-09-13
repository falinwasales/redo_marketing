# -*- coding: utf-8 -*-
# Part of Odoo Falinwa Edition. See LICENSE file for full copyright and licensing details.
{
    'name': 'Redo extention from CLuedoo team   ',
    'version': '13.0.1.0.0',
    'license': 'OPL-1',
    'summary': "Redo extention",
    'category': 'sale',
    'author': "CLuedoo",
    'description': '''
        This module add features:
        =============================
        + Warn user when confirming an Sale order with Zero quantity on hand 
        + Sale price on product only editable by manager

    ''',
    'depends': [
        'sale_stock',
    ],
    'data': [
        'views/product_template_views.xml'
        'views/sale_order_views.xml'
    ],
    'images': [
        # 'static/description/lead_project_screenshot.png'
    ],
    'demo': [
    ],
    # 'price': 180.00,
    # 'currency': 'EUR',
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
