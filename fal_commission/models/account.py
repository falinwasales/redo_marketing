from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    fal_salesperson = fields.Many2one(
        'res.users', string='Sales Person',
        compute='_get_salesperson', store=True)

    fal_salesmember = fields.Many2many(
        'res.users', string='Sales Member',
        related="fal_salesperson.fal_member_ids")

    @api.depends('invoice_ids', 'invoice_ids.invoice_user_id')
    def _get_salesperson(self):
        for payment in self:
            user = False
            for invoice in payment.invoice_ids:
                user = invoice.invoice_user_id.id
            payment.fal_salesperson = user

    fal_commission_amount = fields.Float(
        compute='_get_commission_amount',
        string='Commision Amount', store=True)

    @api.depends(
        'payment_date',
        'fal_salesperson',
        'amount',
        'fal_salesmember',
        'fal_salesperson.fal_commission_rule',
        'fal_salesperson.fal_commission_rule.percentage',
    )
    def _get_commission_amount(self):
        payment_obj = self.env['account.payment']
        for payment in self:
            pay_date_month = payment.payment_date.month
            payments = payment_obj.search([('fal_salesperson', 'in', payment.fal_salesmember.ids)])
            payments_by_month = payments.filtered(lambda a: a.payment_date.month == pay_date_month)
            total_payment_month = sum(pay.amount for pay in payments_by_month)
            commission_amount = total_payment_month * payment.fal_salesperson.fal_commission_rule.percentage / 100
            payment.fal_commission_amount = commission_amount
