from odoo import fields, models


class CustomWizardLine(models.TransientModel):
    _name = "custom.wizard.line"
    _description = "custom wizard line"

    product_name = fields.Many2one('product.product', string='product name')
    product_qty = fields.Integer(string='Quantity')
    product_data = fields.Many2one('custom.wizard', string='product data')

    # def name_get(self):
    #     result = []
    #     print("\n\n\n\n\n\n///////////////////////////////// self ",self)
    #     for records in self:
    #         name = records.id + ', ' + records.product_name
    #         result.append((records.id, name))
    #     return result