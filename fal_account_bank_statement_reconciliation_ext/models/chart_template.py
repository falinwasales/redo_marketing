# -*- coding: utf-8 -*-

from odoo.exceptions import AccessError
from odoo import api, fields, models, _
from odoo import SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
from odoo.http import request
from odoo.addons.account.models.account import TYPE_TAX_USE


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    def _prepare_reconcile_model_vals(self, company, account_reconcile_model, acc_template_ref, tax_template_ref):
        """ This method generates a dictionary of all the values for the account.reconcile.model that will be created.
        """
        self.ensure_one()
        records = super(AccountChartTemplate, self)._prepare_reconcile_model_vals(company, account_reconcile_model, acc_template_ref, tax_template_ref)
        records['product_id'] = account_reconcile_model.product_id
        records['second_product_id'] = account_reconcile_model.second_product_id
        return records


class AccountReconcileModelTemplate(models.Model):
    _name = "account.reconcile.model.template"
    _description = 'Reconcile Model Template'

    # ===== Write-Off =====
    # First part fields.
    product_id = fields.Many2one('product.product', string='Product', ondelete='cascade')

    # Second part fields.
    second_product_id = fields.Many2one('product.product', string='Product', ondelete='cascade')
