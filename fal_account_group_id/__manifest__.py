# -*- coding: utf-8 -*-
{
    "name": "Indonesian Account Group Library",
    "version": "13.0.1.0.0",
    'license': 'OPL-1',
    'summary': 'Propose a hierarchized chart of account by adding the parent account in account groups for Indonesia Chart of Account.',
    'category': 'Localization',
    'website': "https://www.cluedoo.com",
    'support': 'cluedoo@falinwa.com',
    "description": """
        Account Groups
        ======================

        Add libraries of account groups
    """,
    "depends": [
        'fal_company_in_account_group',
        'l10n_id',
    ],
    'data': [
        'data/l10n_id_groups.xml',
        'data/account_account_template.xml',
    ],
    'images': [
        'static/description/account_groups_screenshot.png'
    ],
    'demo': [
    ],
    'price': 180.00,
    'currency': 'EUR',
    'application': False,
    'post_init_hook': 'post_init_hook',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
