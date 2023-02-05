# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    from_so = fields.Boolean(string="From Sale", default=True)
    so_location_id = fields.Many2one('stock.location', string="Stock Location", domain="[('usage', '!=', 'transit')]")

    def update_mo_location(self):
        data = self.env['procurement.group'].read_group([('sale_id', 'in', self.ids)], ['ids:array_agg(id)'], ['sale_id'])
        for item in data:
            procurement_groups = self.env['procurement.group'].browse(item['ids'])
            prod_ids = procurement_groups.stock_move_ids.created_production_id.procurement_group_id.mrp_production_ids
            for prod_id in prod_ids:
                if prod_id:
                    prod_id.write({
                        'from_so': self.from_so,
                        'so_location_id': self.so_location_id.id
                    })
            prod_ids = procurement_groups.mrp_production_ids
            for prod_id in prod_ids:
                prod_id.write({
                    'from_so': self.from_so,
                    'so_location_id': self.so_location_id.id
                })  
    
    def write(self,vals):
        res = super().write(vals)
        self.update_mo_location()
        return res
