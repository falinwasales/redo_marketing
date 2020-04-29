# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.tools import pycompat


class account_bank_statement_line(models.Model):
    _name = 'account.bank.statement.line'
    _inherit = 'account.bank.statement.line'

    product_id = fields.Many2one('product.product', 'Product')
    ref = fields.Char('Reference', size=64)

    def button_cancel_reconciliation(self):
        for line in self:
            if line.statement_id.state == 'confirm':
                line.statement_id.write({'state': 'open'})
        return super(account_bank_statement_line, self).button_cancel_reconciliation()

# end of account_bank_statement_line()


class account_bank_statement(models.Model):
    _inherit = 'account.bank.statement'

    fal_cash_in = fields.Monetary('Cash In', compute="_get_cash_in_out")
    fal_cash_out = fields.Monetary('Cash Out', compute="_get_cash_in_out")
    fal_description = fields.Text('Description')
    fal_remark = fields.Text('Remark')

    @api.depends('line_ids', 'line_ids.amount')
    def _get_cash_in_out(self):
        for statement in self:
            statement.fal_cash_in = sum(line.amount for line in statement.line_ids.filtered(lambda x: x.amount > 0))
            statement.fal_cash_out = sum(line.amount for line in statement.line_ids.filtered(lambda x: x.amount <= 0))

    @api.depends('balance_end_real', 'balance_start')
    def _margin_compute(self):
        for statement in self:
            statement.margin_compute = statement.balance_end_real - statement.balance_end

    margin_compute = fields.Monetary(
        compute='_margin_compute',
        string='Gap',
        readonly=True, store=True,
        help='Margin as calculated Ending balance minuse Computed Balance')

    def button_line_delete(self):
        for statement in self:
            if statement.move_line_ids:
                self.write({'move_line_ids': [(5, False, False)]})
            return True
