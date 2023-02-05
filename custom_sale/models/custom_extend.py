
from odoo import fields, models

class Custom_Extend(models.Model):
    _inherit="sale.order"

    bank_acc_no=fields.Char(string='Bank Acc no.')

