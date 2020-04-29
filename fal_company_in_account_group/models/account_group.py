from odoo import fields, models, api


class AccountGroup(models.Model):
    _inherit = 'account.group'

    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company)
