from odoo import fields, models, api
from lxml import etree
from datetime import date, timedelta


class ResUsers(models.Model):
    _inherit = 'res.users'

    commission = fields.Float(string='User Commission')
    amount = fields.Float(string='Total Commission Earned', store=True, compute='_calculate_amount', default=0.00)
    past_amount = fields.Float(string='Past Amount')

    # user_invoice_line = fields.Many2one('account.move', string='User Invoice Line')

    @api.depends('commission', 'past_amount')
    def _calculate_amount(self):
        self.amount = 0.00
        # self.past_amount = 0.00
        # if self.id != 2:
        #     res = self.env['sale.order'].search([('user_id', '=', self.id)])
        #     sum = 0.00
        #     print("records is : ", res)
        #     for record in res:
        #         sum = sum + (self.commission * record.amount_total) / 100
        #         print("total is : ", record.amount_total)
        #         print("sum is : ", sum)
        #     self.amount = sum
        #     if self.past_amount != 0:
        #         self.amount = self.amount - self.past_amount
        #     self.past_amount = sum
        #     print("past amount ...............", self.past_amount)
        #     print("past amount ...............", self.amount)

    def pay_commission(self):
        self.ensure_one()
        journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
        print("///////*****--journal-******//////", journal)
        print("//////*****--ss--*****/////////", self.env.ref('custom.product_product_100'))
        ss = {
            'product_id': self.env.ref('custom.product_product_100').id,
            'name': self.env.ref('custom.product_product_100').name,
            'quantity': 1,
            'price_unit': self.amount,

        }
        print("//////*****--ss--*****/////////", ss)
        invoice = {
            'move_type': 'out_invoice',
            'journal_id': journal.id,
            'currency_id': self.env.company.currency_id.id,
            'partner_id': self.partner_id.id,
            'invoice_date': date.today(),
            'l10n_in_gst_treatment': 'regular',
            'invoice_line_ids': [(0, 0, ss)]
        }
        print("//////*****--invoice--*****/////////", invoice)
        a = self.env['account.move'].create(invoice)
        print("//////*****--a--*****/////////", a)
        # 'name': 'product test 1',

        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': a.id,
                'res_model': 'account.move',
                'view_id': self.env.ref('account.view_move_form').id, }

#   for work order lines
# @api.onchange('package_id')
#    def change_package_lines(self):
#        self.parts_ids = False
#        self.labor_ids = False
#        for rec in self.package_id.customer_parts_ids:
#            parts = {'product_id': rec.product_id,
#                     'quantity': rec.quantity,
#                     'price': rec.price}
#            self.parts_ids = [(0, 0, parts)]
#        for rec in self.package_id.customer_labor_ids:
#            labors = {'labor_id': rec.labor_id,
#                      'hours': rec.hours,
#                      'rate': rec.rate}
#            self.labor_ids = [(0, 0, labors)]
