# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date


class FalCommision(models.Model):
    _name = 'fal.commission'

    @api.model
    def _default_start_date(self):
        date = fields.date.today()
        first_day = date + relativedelta(day=1)
        return first_day

    @api.model
    def _default_end_date(self):
        date = fields.date.today()
        last_day = date + relativedelta(day=1, months=+1, days=-1)
        return last_day

    @api.onchange('date_start', 'user_id')
    def _onchange_date(self):
        res = {}
        payslip_name = _('Comission')
        self.name = '%s - %s - %s' % (payslip_name, self.user_id.name or '', format_date(self.env, self.date_start, date_format="MMMM y"))
        if self.date_start:
            date_start = self.date_start
            date = fields.Date.from_string(date_start)
            last_day = date + relativedelta(day=1, months=+1, days=-1)
            self.date_end = last_day
            return res

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        if any(self.filtered(lambda a: a.date_start > a.date_end)):
            raise ValidationError(_("The start date cannot be later than the end date."))

    name = fields.Char('Name', required=True)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, required=True)
    member_ids = fields.Many2many('res.users', string='Members')
    date_start = fields.Date('Date Start', default=_default_start_date)
    date_end = fields.Date('Date End', default=_default_end_date)
    payment_ids = fields.Many2many('account.payment', string='Payments', readonly=True)
    commission_amount = fields.Monetary('Commission Amount', currency_field='currency_id', readonly=True)
    total_payment_amount = fields.Monetary('Total Payment Amount', currency_field='currency_id', compute='_get_total_payment', store=True)
    fal_commission_rule = fields.Many2one('fal.commission.rule', string='Commission Rule', required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id')
    search_by = fields.Selection([
        ('user', 'User Only'),
        ('member', 'Members'),
        ('all', 'User and Members'),
    ], string="Search Payment By")

    @api.onchange('user_id')
    def _onchange_user_id(self):
        self.member_ids = [(6, 0, self.user_id.fal_member_ids.ids)]
        self.fal_commission_rule = self.user_id.fal_commission_rule.id
        return {'domain': {'member_ids': [('id', '=', self.user_id.fal_member_ids.ids)]}}

    @api.onchange('fal_commission_rule')
    def _onchange_commission_rule(self):
        self.search_by = self.user_id.fal_commission_rule.search_by

    def _get_payment(self, users):
        payment_obj = self.env['account.payment']
        for commission in self:
            payments = payment_obj.search([
                ('fal_salesperson', 'in', users.ids),
                ('payment_type', '=', 'inbound'),
                ('payment_date', '<=', commission.date_end),
                ('payment_date', '>=', commission.date_start)])
            return payments

    @api.depends('payment_ids')
    def _get_total_payment(self):
        payment_obj = self.env['account.payment']
        for commission in self:
            total_payment_amount = sum(pay.amount for pay in commission.payment_ids)
            self.total_payment_amount = total_payment_amount
            return total_payment_amount

    def _compute_commission(self, localdict):
        try:
            safe_eval(self.fal_commission_rule.amount_python_compute, localdict, mode='exec', nocopy=True)
            return localdict['result']
        except Exception as e:
            raise UserError(_('Wrong python Code'))

    def compute_commission(self):
        users = self.member_ids | self.user_id
        if self.search_by == 'user':
            users = self.user_id
        elif self.search_by == 'member':
            users = self.member_ids

        payments = self._get_payment(users)
        self.payment_ids = [(6, 0, payments.ids)]

        localdict = {
            **{
                'users': self.member_ids | users,
                'user': self.user_id,
                'members': self.member_ids,
                'percentage': self.fal_commission_rule.percentage,
                'target_amount': self.fal_commission_rule.target_amount,
                'total_payment': self.total_payment_amount,
                'commission': self,
                'result': 0.0,
            }
        }
        amount = 0.0
        if self.fal_commission_rule.rule_type == 'code':
            amount = self._compute_commission(localdict)
        else:
            amount = self.total_payment_amount * self.fal_commission_rule.percentage / 100

        if self.fal_commission_rule.target_amount and self.total_payment_amount < self.fal_commission_rule.target_amount:
            amount = 0.0

        self.commission_amount = amount


class FalCommisionRule(models.Model):
    _name = 'fal.commission.rule'

    name = fields.Char('Name', required=True)
    percentage = fields.Float(string="Percentage")
    target_amount = fields.Monetary(string="Target Amount", currency_field='currency_id')
    amount_python_compute = fields.Text(
        string='Python Code',
        default='''
                    # Available variables:
                    #----------------------
                    # user: sales person
                    # members: Members of sales person
                    # users: sales person + members
                    # total_payment: total amount of payment
                    # percentage: get value percentage from field
                    # target_amount: get value target_amount from field
                    # commission: object commission).

                    # Example:
                    # payment1 = commission._get_payment(user)
                    # payment2 = commission._get_payment(members)
                    # total_payment1 = sum(pay.amount for pay in payment1)
                    # total_payment2 = sum(pay.amount for pay in payment2)
                    # commission_user = total_payment1 * 3 / 100
                    # commission_members = total_payment2 * 2 / 100
                    # result = commission_user + commission_members

                    # explanation
                    # (commission._get_paymnet) function to get payment (user) variable to get payment from user(without member)
                    # total_payment1 and total_payment2, sum amount of payment
                    # commission_user and commission_members, formula to get commission
                    # result (final amount of commission)

                    # Note: returned value have to be set in the variable 'result'

                    result = total_payment * percentage / 100''',)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self: self.env.company)
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id)
    rule_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('code', 'Python Code'),
    ], default='percentage')
    search_by = fields.Selection([
        ('user', 'User Only'),
        ('member', 'Members'),
        ('all', 'User and Members'),
    ], default='all', string="Search Payment By")
