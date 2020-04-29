# -*- coding: utf-8 -*-
# © 2013 Nicolas Bessi (Camptocamp SA)
from odoo import api, SUPERUSER_ID
import logging


_logger = logging.getLogger(__name__)


def _install_insert_group(env):
    chart = env.ref('l10n_id.l10n_id_chart')
    for acc_template in env['account.account.template'].search([('chart_template_id', '=', chart.id)]):
        digits = chart.code_digits
        code_main = len(acc_template.code)
        code = acc_template.code
        if code_main > 0 and code_main <= digits:
            code_acc = str(code) + (str('0'))
            for acc in env['account.account'].search([('code', '=', code_acc)]):
                if acc:
                    acc.write({
                        'group_id': acc_template.group_id.id
                    })


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _install_insert_group(env)
