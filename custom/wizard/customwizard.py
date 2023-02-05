import xlwt
import base64
import pytz
from datetime import *
from io import BytesIO
from odoo.exceptions import UserError
from odoo import models, fields, api

from odoo.tools.misc import xlwt


class CustomWizard(models.TransientModel):
    _name = "custom.wizard"
    _description = 'Custom wizard'

    product_details = fields.One2many('custom.wizard.line', 'product_data', string='Sale_details')

    def product_send_btn(self):
        active_record_id = self.env['sale.order'].browse(self._context.get('active_id'))
        # for current form view id
        # sale.order id returned
        print("//////////////////////////////---------------------------- active id ", active_record_id)
        print("//////////////////////////////////-*--*-*-*-*-*-*-*--*", self._context)

        for line in self.product_details:
            print("\n\n////////////////////////////=----------------------------------- line ", line.product_name)
            print("\n\n////////////////////////////=----------------------------------- line ", line.product_name.id)
            product_sale_line = self.env['sale.order.line'].create({
                'order_id': active_record_id.id,
                'product_id': line.product_name.id,
                'product_uom_qty': line.product_qty
            })
            print("/////////////////////////////////////////////////// hiiii")
            print("////////////////////////-------------------------------------", product_sale_line)


#######  vehicle repair > work order > in progress.....
# after draft checking

# stock_picking_ids_1 = self.env['stock.picking'].search([('work_order_id', '=', self.id)])
# flag = 0
# for rec in stock_picking_ids_1:
#     print('after stock ids....', rec)
#     print('after stock ids....', rec.state)
#     if rec.state == 'assigned':
#         flag = 1
#     else:
#         flag = 0
# if flag == 1:
#     self.status = 'progress'
# else:
#     raise ValidationError(_("All Stocks Are Not Ready."))


class InvoiceRecords(models.TransientModel):
    _name = 'invoice.records'
    _description = 'invoice.records'

    report_type = fields.Selection([('pdf', 'PDF'), ('xls', 'Excel')], string='Report Type', default='pdf')
    data = fields.Binary(string='Data')
    file_name = fields.Char(string='File Name', default='Student Excel Report')

    def print_records(self):
        print("action called......\n" * 5)
        active_record_ids = self.env['account.move'].browse(self._context.get('active_ids')).ids
        print("-------------------   selected ids.... -------------", active_record_ids)
        print("-------------------  selected ids type.... -------------", type(active_record_ids))
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {'record_ids': active_record_ids},
            'res_model': 'invoice.records',
            'view_id': self.env.ref('custom.invoice_print_records').id,
            'target': 'new',
        }

    def mail_report(self):
        print("method called.....\n" * 5)
        active_record_ids = self.env.context.get('record_ids')
        print("-------------------  from wizard selected ids.... -------------", active_record_ids)
        print("-------------------  from wizard selected ids type.... -------------", type(active_record_ids))
        search_records = self.env['account.move'].browse(active_record_ids)
        print("---------------- froom wizard..... search ids ", search_records)
        print("---------------- froom wizard..... search ids ", type(search_records))
        mail_template_id = self.env.ref('custom.mail_invoice_report')
        if self.report_type == 'pdf':
            print("report pdf.....\n" * 5)
            template_id = self.env.ref('account.account_invoices')
            pdf = template_id._render_qweb_pdf(search_records.ids)
            # print("\n\n\n pdf--->", pdf)
            # print("\n\n\n pdf[0]--->", pdf[0])
            values = base64.b64encode(pdf[0])
            print("vals executed...")
            attachment_id = self.env['ir.attachment'].sudo().create(
                {'datas': values, 'name': 'invoice_report.pdf'})
            print("attachment_ids.....")
            mail_template_id.attachment_ids = attachment_id
            mail_template_id.send_mail(self.id, raise_exception=False, force_send=True)
            print("mail sent.....")

        elif self.report_type == 'xls':
            print("report excel.....\n" * 5)
            workbook = xlwt.Workbook()
            stylePC = xlwt.XFStyle()
            worksheet = workbook.add_sheet('Invoice Records')
            bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            stylePC.alignment = alignment
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment_num = xlwt.Alignment()
            alignment_num.horz = xlwt.Alignment.HORZ_RIGHT
            horz_style = xlwt.XFStyle()
            horz_style.alignment = alignment_num
            align_num = xlwt.Alignment()
            align_num.horz = xlwt.Alignment.HORZ_RIGHT
            horz_style_pc = xlwt.XFStyle()
            horz_style_pc.alignment = alignment_num
            style1 = horz_style
            font = xlwt.Font()
            font1 = xlwt.Font()
            borders = xlwt.Borders()
            borders.bottom = xlwt.Borders.THIN
            font.bold = True
            font1.bold = True
            font.height = 500
            stylePC.font = font
            style1.font = font1
            stylePC.alignment = alignment
            pattern = xlwt.Pattern()
            pattern1 = xlwt.Pattern()
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN
            pattern1.pattern = xlwt.Pattern.SOLID_PATTERN
            pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
            pattern1.pattern_fore_colour = xlwt.Style.colour_map['gray25']
            stylePC.pattern = pattern
            style1.pattern = pattern
            worksheet.write_merge(0, 1, 2, 5, 'Invoice Records', style=stylePC)
            worksheet.col(2).width = 5600

            row = 5
            list1 = ['Id', 'Name', 'Invoice Date', 'Journal_id']
            list2 = ['Product', 'Label', 'Quantity', 'Price', 'Discount', 'Subtotal']
            for i in search_records:
                worksheet.col(1).width = 5000
                worksheet.write(row, 1, list1[0], style1)
                worksheet.col(2).width = 5000
                worksheet.write(row, 2, list1[1], style1)
                worksheet.col(3).width = 5000
                worksheet.write(row, 3, list1[2], style1)
                worksheet.col(4).width = 5000
                worksheet.write(row, 4, list1[3], style1)
                row = row + 1
                print("active records......", active_record_ids)

                worksheet.write(row, 1, i.partner_id.id)
                worksheet.write(row, 2, i.partner_id.name)
                worksheet.write(row, 3, i.invoice_date)
                worksheet.write(row, 4, i.journal_id.id)
                row = row + 1
                print("invoice date ......", i.invoice_date)
                print("invoice mde now invoice line....")

                # worksheet.write_merge(row,row,2,4, 'Invoice Report')

                worksheet.col(1).width = 5000
                worksheet.write(row, 1, list2[0], style1)
                worksheet.col(2).width = 5000
                worksheet.write(row, 2, list2[1], style1)
                worksheet.col(3).width = 5000
                worksheet.write(row, 3, list2[2], style1)
                worksheet.col(4).width = 5000
                worksheet.write(row, 4, list2[3], style1)
                worksheet.col(5).width = 5000
                worksheet.write(row, 5, list2[4], style1)
                worksheet.col(6).width = 5000
                worksheet.write(row, 6, list2[5], style1)
                row = row + 1
                print('///// label added....')
                print("invoice line is ....", i.invoice_line_ids)

                worksheet.write(row, 1, i.invoice_line_ids.product_id.id)
                worksheet.write(row, 2, i.invoice_line_ids.name)
                worksheet.write(row, 3, i.invoice_line_ids.quantity)
                worksheet.write(row, 4, i.invoice_line_ids.price_unit)
                worksheet.write(row, 5, i.invoice_line_ids.discount)
                worksheet.write(row, 6, i.invoice_line_ids.price_subtotal)
                row = row + 3
                print("no of rows....", row)
                print("no of rows.... prints row")
                worksheet.write(row, 5, 'Creater:', style1)
                worksheet.write(row, 6, i.invoice_user_id.name, style1)
                row = row + 3
            tz = pytz.timezone('Asia/Kolkata')
            file_data = BytesIO()
            workbook.save(file_data)
            self.write({
                'data': base64.encodebytes(file_data.getvalue()),
                'file_name': 'Invoice Report - %s' % (datetime.now(tz).strftime('%Y-%m-%d %I:%M:%S')),
            })

            attachment_id = self.env['ir.attachment'].sudo().create(
                {'datas': self.data, 'name': self.file_name})
            print("attachment_ids.....")
            mail_template_id.attachment_ids = attachment_id
            mail_template_id.send_mail(self.id, raise_exception=False, force_send=True)
            print("mail sent.....")

    def print_report(self):
        active_record_ids = self.env.context.get('record_ids')
        print("-------------------  from wizard print button selected ids.... -------------", active_record_ids)
        print("-------------------  from wizard  print button  selected ids type.... -------------",
              type(active_record_ids))
        search_records = self.env['account.move'].browse(active_record_ids)
        print("---------------- froom wizard..... search ids ", search_records)
        print("---------------- froom wizard..... search ids ", type(search_records))
        if self.report_type == 'pdf':
            print("report pdf from print button.....\n" * 5)
            template_id = self.env.ref('account.account_invoices')
            pdf = template_id._render_qweb_pdf(search_records.ids)
            # print("\n\n\n pdf--->", pdf)
            # print("\n\n\n pdf[0]--->", pdf[0])
            values = base64.b64encode(pdf[0])
            print("vals executed...")
            attachment_id = self.env['ir.attachment'].sudo().create(
                {'datas': values, 'name': 'invoice_report.pdf'})
            print("attachment_ids.....", attachment_id)
            return self.env.ref('account.account_invoices').report_action(search_records.ids)
        else:
            print("report excel.....\n" * 5)
            workbook = xlwt.Workbook()
            stylePC = xlwt.XFStyle()
            worksheet = workbook.add_sheet('Invoice Records')
            bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            stylePC.alignment = alignment
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment_num = xlwt.Alignment()
            alignment_num.horz = xlwt.Alignment.HORZ_RIGHT
            horz_style = xlwt.XFStyle()
            horz_style.alignment = alignment_num
            align_num = xlwt.Alignment()
            align_num.horz = xlwt.Alignment.HORZ_RIGHT
            horz_style_pc = xlwt.XFStyle()
            horz_style_pc.alignment = alignment_num
            style1 = horz_style
            font = xlwt.Font()
            font1 = xlwt.Font()
            borders = xlwt.Borders()
            borders.bottom = xlwt.Borders.THIN
            font.bold = True
            font1.bold = True
            font.height = 500
            stylePC.font = font
            style1.font = font1
            stylePC.alignment = alignment
            pattern = xlwt.Pattern()
            pattern1 = xlwt.Pattern()
            pattern.pattern = xlwt.Pattern.SOLID_PATTERN
            pattern1.pattern = xlwt.Pattern.SOLID_PATTERN
            pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
            pattern1.pattern_fore_colour = xlwt.Style.colour_map['gray25']
            stylePC.pattern = pattern
            style1.pattern = pattern
            worksheet.write_merge(0, 1, 2, 5, 'Invoice Records', style=stylePC)
            worksheet.col(2).width = 5600

            row = 5
            list1 = ['Id', 'Name', 'Invoice Date', 'Journal_id']
            list2 = ['Product', 'Label', 'Quantity', 'Price', 'Discount', 'Subtotal']
            for i in search_records:
                worksheet.col(1).width = 5000
                worksheet.write(row, 1, list1[0], style1)
                worksheet.col(2).width = 5000
                worksheet.write(row, 2, list1[1], style1)
                worksheet.col(3).width = 5000
                worksheet.write(row, 3, list1[2], style1)
                worksheet.col(4).width = 5000
                worksheet.write(row, 4, list1[3], style1)
                row = row + 1
                print("active records......", active_record_ids)

                worksheet.write(row, 1, i.partner_id.id)
                worksheet.write(row, 2, i.partner_id.name)
                worksheet.write(row, 3, i.invoice_date)
                worksheet.write(row, 4, i.journal_id.id)
                row = row + 1
                print("invoice date ......", i.invoice_date)
                print("invoice mde now invoice line....")

                # worksheet.write_merge(row,row,2,4, 'Invoice Report')

                worksheet.col(1).width = 5000
                worksheet.write(row, 1, list2[0], style1)
                worksheet.col(2).width = 5000
                worksheet.write(row, 2, list2[1], style1)
                worksheet.col(3).width = 5000
                worksheet.write(row, 3, list2[2], style1)
                worksheet.col(4).width = 5000
                worksheet.write(row, 4, list2[3], style1)
                worksheet.col(5).width = 5000
                worksheet.write(row, 5, list2[4], style1)
                worksheet.col(6).width = 5000
                worksheet.write(row, 6, list2[5], style1)
                row = row + 1
                print('///// label added....')
                print("invoice line is ....", i.invoice_line_ids)
                for j in i.invoice_line_ids:
                    worksheet.write(row, 1, j.product_id.id)
                    worksheet.write(row, 2, j.name)
                    worksheet.write(row, 3, j.quantity)
                    worksheet.write(row, 4, j.price_unit)
                    worksheet.write(row, 5, j.discount)
                    worksheet.write(row, 6, j.price_subtotal)
                    row = row + 1
                row = row + 1
                print("no of rows....", row)
                print("no of rows.... prints row")

                worksheet.write(row, 4, 'Creater:', style1)
                worksheet.write(row, 5, i.invoice_user_id.name)
                row = row + 3
            file_data = BytesIO()
            workbook.save(file_data)
            print("data is...." * 5)
            self.data = base64.encodebytes(file_data.getvalue())
            print("data printed...." * 5, "now file name")
            print("data file is...." * 5)
            # print("data is....", self.data)
            return {
                'type': 'ir.actions.act_url',
                'url': '/web/content/invoice.records/%s/data/Invoice_report.xls?download=true' % (self.id),
                'target': 'self',
                'name': 'Invoice_report'
            }

            # action = self.env["ir.actions.act_window"]._for_xml_id("sale.sale_order_action_view_quotation_form")
            # # if len(product_details > 0):
            # #     for line in product_details:
            # action['context'] = {
            #     "product_id": self.product_name,
            #     'product_uom_qty': self.product_qty
            # }
            # return action
