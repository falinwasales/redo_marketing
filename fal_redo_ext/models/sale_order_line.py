from collections import defaultdict

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

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
                if line.qty_available_today <= line.product_uom_qty:
                    line.fal_sale_check = True
                else:
                    line.fal_sale_check = False
            else:
                line.fal_sale_check = False
