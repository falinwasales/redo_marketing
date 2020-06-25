from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'


    fal_commission_rule = fields.Many2one('fal.commission.rule', string='Commission Rule')
    fal_member_ids = fields.Many2many(
        'res.users', string='Member',
        compute='_get_member')

    def _get_member(self):
        for payment in self:
            team_obj = self.env['crm.team']
            users = []
            teams = team_obj.search([('user_id', '=', payment.id)])
            if teams:
                    team_members = teams
                    while team_members:
                        for team in team_members:
                            for member in team.member_ids:
                                if member.id not in users:
                                    users.append(member.id)
                            team_members = team_obj.search([('user_id', 'in', team.member_ids.ids)])
                            if not team_members:
                                team_members = False
            payment.fal_member_ids = [(6, 0, users)]
