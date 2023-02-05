# -*- coding: utf-8 -*-

from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    from_so = fields.Boolean(copy=False, string="From Sale", default=False)
    so_location_id = fields.Many2one('stock.location', string="Stock Location")

    @api.model
    def create(self,vals):
        res = super().create(vals)
        #  Add from SO and location data while creating new manufacturing order
        if res.move_dest_ids:
            for move_id in res.move_dest_ids:
                if move_id.group_id and move_id.group_id.sale_id:
                    res.write({
                        'from_so': move_id.group_id.sale_id.from_so,
                        'so_location_id': move_id.group_id.sale_id.so_location_id.id})
        return res
