from collections import defaultdict

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('user_id')
    def _get_cust_access(self):
        for order in self:
            partner = order.env['res.partner'].search([('x_studio_redo_user_access', '=', order.user_id.id)])
            order.fal_partner_ids = partner
            product_tmpl = order.env['product.template'].search([('x_studio_redo_user_access', '=', order.user_id.id)])
            product_product = order.env['product.product'].search([('product_tmpl_id', 'in', product_tmpl.ids)])
            order.fal_product_ids = product_product

    fal_partner_ids = fields.Many2many("res.partner", string='Redo Customer Access', compute='_get_cust_access', readonly=True, copy=False)
    fal_product_ids = fields.Many2many("product.product", string='Redo Product Access', compute='_get_cust_access', readonly=True, copy=False)
    user_id = fields.Many2one(readonly=lambda self:False if self.user.x_studio_employee_status == 'Staff' else True)
    partner_id = fields.Many2one(domain="['&', ('id', 'in', fal_partner_ids), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    partner_invoice_id = fields.Many2one(domain="['&', ('id', 'in', fal_partner_ids), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    partner_shipping_id = fields.Many2one(domain="['&', ('id', 'in', fal_partner_ids), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",)

    def action_confirm(self):
        filtered = self.order_line.filtered(lambda x: x.fal_sale_check)
        if filtered:
            msg = ''
            for line in filtered:
                msg =''.join([msg, line.product_id.display_name, '  ', str(line.qty_available_today),'\n'])
            raise UserError(_('There are product that is not available.\n\n'
                    + msg + '\nPlease update the quantity or make procurement'))
        else:
            super(SaleOrder, self).action_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    fal_sale_check = fields.Boolean('Is Product Available', default=False, compute='_computesalechek')

    @api.depends('product_id', 'customer_lead', 'product_uom_qty', 'product_uom', 'order_id.warehouse_id', 'order_id.commitment_date', 'fal_sale_check')
    def _computesalechek(self):
        for line in self:
            if line.product_id.type == 'product':
                if line.qty_available_today < line.product_uom_qty:
                    line.fal_sale_check = True
                else:
                    line.fal_sale_check = False
            else:
                line.fal_sale_check = False
