# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PrintMultiInvoiceReport(models.TransientModel):
    _name = 'print.multi.invoice.report.wizard'
    _description = 'Print Posted Invoice Multi Reports'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")


    def print_invoice(self):
        account = self.env['account.move']
        move_ids = account.search(
            [
                ('invoice_date', '>=', self.start_date),
                ('invoice_date', '<=', self.end_date),
                ('state', '=', 'posted'),
            ])
        if move_ids:
            return self.env.ref('account.account_invoices').report_action(move_ids)
        else:
            raise ValidationError(_("No Records Found !!!"))