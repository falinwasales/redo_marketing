# -*- coding: utf-8 -*-
{
    'name': "Commission",
    'version': '13.3.1.0.0',
    'license': 'OPL-1',
    'summary': "Sales Comission",
    'category': 'Sales',
    'author': "CLuedoo",
    'website': "https://www.cluedoo.com",
    'support': 'cluedoo@falinwa.com',
    'description': """
        Commission
        ===============================================================

        Sales Commission
    """,
    'depends': ['sale_management'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/commission_view.xml',
        'views/account_view.xml',
    ],
    'images': [
    ],
    'demo': [
    ],
    'price': 0.00,
    'currency': 'EUR',
    'application': False,
}
