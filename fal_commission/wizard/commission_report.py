# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FalCommision(models.TransientModel):
    _name = 'fal.commission.report.wizard'

    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    user_ids = fields.Many2many('res.users', string='Sales Person')
    invoice_ids = fields.Many2many('account.move', string='Invoices')

    @api.onchange('user_id')
    def _onchange_user_id(self):
        self.user_ids = [(6, 0, [self.user_id.id])]

    @api.onchange('user_ids')
    def _onchange_user_ids(self):
        invoice_obj = self.env['account.move'].search([
            ('invoice_user_id', 'in', self.user_ids.ids),
            ('invoice_payment_state', '=', 'paid'),
            ('type', '=', 'out_invoice'),
        ])
        self.invoice_ids = [(6, 0, invoice_obj.ids)]
