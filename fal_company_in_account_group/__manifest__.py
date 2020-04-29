# encoding: utf-8
# Part of Odoo - CLuedoo Edition. Ask Falinwa / CLuedoo representative for full copyright And licensing details.
{
    'name': "Company in Account Group",
    'version': '13.0.1.0.0',
    'license': 'OPL-1',
    # 'sequence': 18,
    'summary': 'Add company field on account group',
    'category': 'Accounting and Finance',
    'author': "CLuedoo",
    'website': "https://www.cluedoo.com",
    'support': 'cluedoo@falinwa.com',
    'description': """

    """,
    'depends': [
        'account',
    ],
    'data': [
        'security/account_security.xml',
        'views/account_views.xml',
    ],
    'images': [
    ],
    'demo': [
    ],

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
