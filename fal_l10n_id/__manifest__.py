# -*- coding: utf-8 -*-
{
    'name': 'Indonesian - Accounting',
    'version': '13.0.1.0.0',
    'license': 'OPL-1',
    'summary': 'Provides the list of Indonesian account templates and tax templates',
    'category': 'Localization',
    'author': "CLuedoo",
    'website': "https://www.cluedoo.com",
    'support': 'cluedoo@falinwa.com',
    'description': """
        Indonesian Odoo localisation
        ==============================

        - standard Indonesian chart of accounts
    """,
    'depends': ['fal_account_group_id'],
    'data': [
        'data/l10n_id_chart_data.xml',
        'data/account_account_template.xml',
        'data/account_chart_template_data.xml',
        'data/account_account_tag.xml',
        'data/account_tax_template.xml',
        'data/res.country.state.csv',
    ],
    'images': [
        'static/description/l10n_id_screenshot.png'
    ],
    'demo': [
    ],
    'price': 360.00,
    'currency': 'EUR',
    'application': False,
}
