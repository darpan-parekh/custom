# -*- coding: utf-8 -*-

from odoo import models


class Location(models.Model):
    _inherit = 'stock.location'

    def name_get(self):
        result = []
        for location in self:
            name = location.name + '-' + location.usage
            result.append((location.id, name))
        return result
