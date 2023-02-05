import json
from odoo.osv import expression
from odoo import fields, models, api
from lxml import etree
from datetime import date, timedelta
from datetime import datetime as dt


class SaleOrder(models.Model):
    _inherit = "sale.order"

    stock_names = fields.One2many('stock.picking', 'customer_names', string='Stock Names')
    # due_payment_date = fields.Date(string="Due Payment Date")
    # date_time_detail = fields.Datetime(string="Sale Date Time", default=lambda self: fields.Datetime.now())
    # order_desc = fields.Text(string="Order Description")
    # order_body = fields.Html(string="Html Body")
    # order_bin = fields.Binary(string="Binary Field")
    # order_image = fields.Image(string="Image Field")
    # order_bool = fields.Boolean(string="Boolean Field")
    order_select = fields.Selection([('placed', 'Placed'), ('cart', 'In Cart'), ('received', 'Received')],
                                    string="Select", default='placed')
    sale_order_details = fields.Many2one('product.template', string='Sale order Details')
    product_avg_disc = fields.Float(string='Product Avg Discount', compute="_compute_order_discount_avg", default=0.00)
    student_sale = fields.Many2one("custom.student", string="Student Sale")

    # # to set multiple default value on create button when new form is open or load 1st tym.
    # @api.model
    # def default_get(self, fields):
    #     print("///////////////----------------- fields--->", fields)  # returns all fields names
    #     res = super(SaleOrder, self).default_get(fields)
    #     if self.order_select not in res:
    #         self.order_select = 'cart'
    #     # print("//////////////////----------------------------- res _____", res)
    #     return res  # return dict of field name and default value if value is not null

    # to change field after its creation for specific user group.
    #  for full form acsess and control all fields for any specific group
    # if it is invisible or readonly in some user group, here it is possible
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):

        view = self.env['ir.ui.view'].browse(view_id)  # .sudo().browse(view_id)
        # print("\n\n////////////////////////---------------------- view -----> ",
        #       view)  # return ir.ui.view(id) for view id
        # print("\n\n/////////////////////////----------------------- view-id --->",
        #       view_id)  # return view id from ir.ui.view
        # print("\n\n/////////////////////////----------------------- view-type --->", view_type)  # return view type
        # print("\n\n/////////////////////////----------------------- toolbar --->", toolbar)  # return bool t/f
        # print("\n\n/////////////////////////----------------------- submenu --->", submenu)  # return bool t/f

        res = super(SaleOrder, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=False)
        # print("\n\n//////////////////////////------------------------- field view result ----> ", res)
        doc = etree.XML(res['arch'])
        update_field = doc.xpath("//field[@name='order_select']")
        if update_field:
            # print('////////////---------------------- updated field ------->>>> ', update_field[0])
            update_field = update_field[0]
            modifiers = json.loads(update_field.get("modifiers"))
            modifiers['readonly'] = True
            update_field.set("modifiers", json.dumps(modifiers))
            # update_field.set('readonly', '1')
            # update_field.set('invisible','1')
            # setup_modifiers(update_field, res['fields']['order_select'])
        res['arch'] = etree.tostring(doc)
        # print("\n\n\n /////////////////////////////////////////updated result -----> ", res)

        return res  # return whole xml page with fields,attributes,domain,form,modelqqqqqqq

    def _compute_order_discount_avg(self):
        order_line = self.order_line
        print(
            "////////////////////////////------------------------------/////////////////////----------------- order-line ",
            order_line)
        print(
            "////////////////////////////------------------------------/////////////////////----------------- order-id ",
            order_line.order_id)
        sum = 0
        if len(order_line) >= 1:
            for line in order_line:

                # print(
                #     "\n\n\n////////////////////////////------------------------------/////////////////////----------------- order-line ",
                #     line)
                # print(
                #     "////////////////////////////------------------------------/////////////////////----------------- order-id ",
                #     line.order_id)
                if line.product_didc_type == "fixed" and line.price_unit >= 1:
                    sum = sum + (line.product_disc * 100) / line.price_unit
                else:
                    sum = sum + line.product_disc
            self.product_avg_disc = sum / len(order_line)
        else:
            self.product_avg_disc = 0.00

    def action_custom_wizard(self):
        action = self.env["ir.actions.actions"]._for_xml_id("custom.custom_wizard_action")
        action['context'] = {
            # "default_sale_order_name": self.name,
            'default_sale_confirm_date': self.date_order
        }
        return action

    @api.model
    def create(self, vals):
        result = super(SaleOrder, self).create(vals)
        print("//////////////////////////------------------------------------", vals)
        #  search that id firse to modify data  and then put this write method
        # student = self.env['custom.student'].create({
        #     'name': vals['partner_id'].name,
        #     'qualification': "Bachelors"
        # })
        # print(
        #     '///////////////////////----------------------------------*******************************----------------- ',
        #     student)
        print(
            "///////////////////////////////////////___________________-------------------------------------------------------- create result ",
            result)
        return result

    @api.model
    def write(self, vals):
        result = super(SaleOrder, self).write(vals)

        #  search that id first to write data at which id?? so search id to modify  data  and then put this write method
        # print("//////////////////////////////////////////////// result ", result)
        # print("////////////////////////////----------------------------------------- values ", vals)
        active_record_id = self.env['custom.student'].search([('name', '=', self.partner_id.id)])
        # for current form view id
        # sale.order id returned
        # print("//////////////////////////////---------------------------- active id ", active_record_id,
        #       "\n////////////*-*-*--*-**-*---*-*-*-*-*-*--*-*-*-*-*-*--*-*-*-*-*-* ", self.partner_id.name)
        # student = active_record_id.write({
        #     'name': self.partner_id.name,
        #     'qualification': "Bachelors",
        #     # 'sale_order_details.order_select':
        # })
        # print('///////////////////////----------------------*********----------- ')
        # print("/////////////////////////----------------------------*--*-*-*-*-*-*-*-*-*-*-*-*-*-*", student)
        # print("/////////////////////////////////--------------------------------------------------------")
        return result

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        result = super(SaleOrder, self).copy(default)
        #     student = self.env['custom.student'].create({
        #                 'name': self.partner_id.name,
        #                 'roll_no': self.age,
        #                 'qualification': "Bachelors",
        #                 'dob': self.date_order,
        #             })
        print("//////////////----------------------*-*--*-*-*--*-*-*--*-*-*--*-*-* copy result ", result)
        return result

    @api.onchange('partner_id')
    def _change_date_days(self):
        # self.due_payment_date = date.today() + timedelta(self.partner_id.due_payment_date_days)
        # self.date_order = dt.now() + timedelta(self.partner_id.expiry_date_days)
        display = self.env['custom.student'].browse(self.partner_id.name)
        print("///////////////////////////////////----------------------------------------- browse display name",
              display)

        display_search = self.env['custom.student'].search([('name', '=', self.partner_id.name)])
        print("\n\n///////////////////////////////////----------------------------------------- search display name",
              display_search)
        if display_search:
            student = display_search.write({
                'name': self.partner_id.name,
                'qualification': "Bachelors",
                # 'sale_order_details.order_select':
            })
            # print('///////////////////////----------------------*********----------- ')
            print("/////////////////////////----------------------------*--*-*-*-*-*-*-*-*-*-*-*-*-*-*", student)
            # print("/////////////////////////////////--------------------------------------------------------")
    # return {
    #     'warning': {
    #         'title': 'Record matched',
    #         'message': display
    #     }
    # }


class ResPartner(models.Model):
    _inherit = 'res.partner'

    expiry_date_days = fields.Integer(string='Expiry Days')
    due_payment_date_days = fields.Integer(string='Due Payment Days')
    total_sale_price = fields.Float(string='Total Sell Price', compute='_compute_total_price')
    customer_relation_count = fields.Integer(compute='_compute_user_crm_details')

    def _compute_user_crm_details(self):
        #  for external search read excersise
        record = self.env['crm.lead'].search_read([('partner_id', '=', self.id)])
        # for line in record:
        print("\n\n//////////=-------- record ", record)

        # countinue
        total_count = self.env['crm.lead'].search_count([('partner_id', '=', self.id)])
        print("\n\n///////////////---------------- Total is ---->>>", total_count, "\n\n")
        self.customer_relation_count = total_count

        # or both working  (bottom code is from base)
        # all_partners = self.search([('id', 'child_of', self.ids)])
        # all_partners.read(['parent_id'])
        #
        # crm_groups = self.env['crm.lead'].read_group(
        #     domain=[('partner_id', 'in', all_partners.ids)],
        #     fields=['partner_id'], groupby=['partner_id']
        # )
        # partners = self.browse()
        # for group in crm_groups:
        #     partner = self.browse(group['partner_id'][0])
        #     while partner:
        #         if partner in self:
        #             partner.customer_relation_count += group['partner_id_count']
        #             partners |= partner
        #         partner = partner.parent_id
        # (self - partners).customer_relation_count = 0

    # @api.model
    # def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
    #     print("\n\n/////////////////////////----------------------- domain --->",
    #           domain)  # return view id from ir.ui.view
    #     print("\n\n/////////////////////////----------------------- fields --->", fields)  # return view type
    #     print("\n\n/////////////////////////----------------------- offset --->", offset)  # return bool t/f
    #     print("\n\n/////////////////////////----------------------- limit --->", limit)  # return bool t/f
    #     print("\n\n/////////////////////////----------------------- order --->", order)  # return bool t/f
    #
    #     res = super(ResPartner, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
    #     print("////////////////////////////////////=------------------------------- res partner result ---->", res)
    #     count = 0
    #     if res:
    #         print("\n\n//////////////////------------------------ 1st record only ", res[0], "\n\n"
    #                                                                                          "")
    #     for element in res:
    #         print("////////////////////------------------- id and dispaly_name ----> ", element.get('id'), " ",
    #               element.get('display_name'))
    #         count += 1
    #     print("//////////////////------------------ total record name ------>>>>>", count)
    #     return res


    @api.depends('sale_order_count')
    def _compute_total_price(self):
        total = self.env['sale.order'].search([('partner_id', '=', self.id)])
        total_price = 0.0
        if total:
            for lines in total:
                total_price += lines.amount_total
        self.total_sale_price = total_price


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # product_sale = fields.Char(string='Product Sale')
    # sale_order_status = fields.Char(string='Sale Order Status')
    product_disc = fields.Float(string='Discount %', store=True)
    product_didc_type = fields.Selection([('fixed', 'Fixed Discount'), ('variable', 'Some % Discount')],
                                         string="Discount Type")

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'product_disc': self.product_disc,
            'product_didc_type': self.product_didc_type,
            'analytic_account_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
        }
        if optional_values:
            res.update(optional_values)
        if self.display_type:
            res['account_id'] = False
        return res

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'product_didc_type', 'product_disc')
    def _compute_amount(self):
        # active_record_id = self.env['sale.order'].search([('name', '=', self.partner_id.id)])
        for line in self:
            if line.product_didc_type == 'variable':
                if line.product_disc >= 0.00 and line.product_disc <= 100.00:
                    price = line.price_unit * (1 - (line.product_disc or 0.0) / 100.0)
                else:
                    price = line.price_unit
                    line.product_disc = 0.00
            elif line.product_didc_type == 'fixed':
                if line.price_unit >= line.product_disc:
                    price = line.price_unit - (line.product_disc or 0.0)
                else:
                    price = line.price_unit
                    line.product_disc = 0.00
            else:
                price = line.price_unit
                line.product_disc = 0.00
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups(
                    'account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])
