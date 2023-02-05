from odoo import fields, models, api, _


class AccountMove(models.Model):
    _inherit = "account.move"
    _rec_name = 'partner_id'

    custom_price = fields.Integer(string='Custom price')
    payment_mode = fields.Char(string='Custom payment mode')
    account_balance = fields.Char(string='Account Balance')
    account_branch = fields.Char(string='Account Branch')
    branch_city = fields.Char(string='Branch City')
    custom_city = fields.Char(string="Customer City")
    city_check = fields.Boolean(string=" Check For Same City")
    bool_hide = fields.Boolean()
    custom_name = fields.Many2one('res.partner', string='Customer Name')

    def check_city(self):
        self.custom_city = self.branch_city
        self.city_check = False
        self.bool_hide = True

    @api.model
    def default_get(self, fields):
        print("/////////////////-----------------------///// default fields ----> ", fields)
        res = super(AccountMove, self).default_get(fields)
        print("___________-----------------------////////////////////// res--->", res)
        return res


class AcocuntMoveLine(models.Model):
    _inherit = 'account.move.line'

    payment_amount = fields.Char(string='Payment Amount', help='this is payment field')
    account_name = fields.Char(string='Account Name')
    product_disc = fields.Float(string='Discount %', store=True)
    product_didc_type = fields.Selection([('fixed', 'Fixed Discount'), ('variable', 'Some % Discount')],
                                         string="Discount Type")

    # @api.model_create_multi
    # def create(self, vals_list):
    #     # OVERRIDE
    #     ACCOUNTING_FIELDS = ('debit', 'credit', 'amount_currency')
    #     BUSINESS_FIELDS = ('price_unit', 'quantity', 'discount', 'tax_ids')
    #
    #     for vals in vals_list:
    #         move = self.env['account.move'].browse(vals['move_id'])
    #         vals.setdefault('company_currency_id',
    #                         move.company_id.currency_id.id)  # important to bypass the ORM limitation where monetary fields are not rounded; more info in the commit message
    #
    #         # Ensure balance == amount_currency in case of missing currency or same currency as the one from the
    #         # company.
    #         currency_id = vals.get('currency_id') or move.company_id.currency_id.id
    #         if currency_id == move.company_id.currency_id.id:
    #             balance = vals.get('debit', 0.0) - vals.get('credit', 0.0)
    #             vals.update({
    #                 'currency_id': currency_id,
    #                 'amount_currency': balance,
    #             })
    #         else:
    #             vals['amount_currency'] = vals.get('amount_currency', 0.0)
    #
    #         if move.is_invoice(include_receipts=True):
    #             currency = move.currency_id
    #             partner = self.env['res.partner'].browse(vals.get('partner_id'))
    #             taxes = self.new({'tax_ids': vals.get('tax_ids', [])}).tax_ids
    #             tax_ids = set(taxes.ids)
    #             taxes = self.env['account.tax'].browse(tax_ids)
    #             if any(vals.get(field) for field in ACCOUNTING_FIELDS):
    #                 price_subtotal = self._get_price_total_and_subtotal_model(
    #                     vals.get('price_unit', 0.0),
    #                     vals.get('quantity', 0.0),
    #                     vals.get('discount', 0.0),
    #                     currency,
    #                     self.env['product.product'].browse(vals.get('product_id')),
    #                     partner,
    #                     taxes,
    #                     move.move_type,
    #                     vals.get('product_disc', 0.00),
    #                     vals.get('product_didc_type', ""),
    #                 ).get('price_subtotal', 0.0)
    #                 vals.update(self._get_fields_onchange_balance_model(
    #                     vals.get('quantity', 0.0),
    #                     vals.get('discount', 0.0),
    #                     vals['amount_currency'],
    #                     move.move_type,
    #                     currency,
    #                     taxes,
    #                     price_subtotal
    #                 ))
    #                 vals.update(self._get_price_total_and_subtotal_model(
    #                     vals.get('price_unit', 0.0),
    #                     vals.get('quantity', 0.0),
    #                     vals.get('discount', 0.0),
    #                     currency,
    #                     self.env['product.product'].browse(vals.get('product_id')),
    #                     partner,
    #                     taxes,
    #                     move.move_type,
    #                     vals.get('product_disc', 0.00),
    #                     vals.get('product_didc_type', ""),
    #                 ))
    #             elif any(vals.get(field) for field in BUSINESS_FIELDS):
    #                 vals.update(self._get_price_total_and_subtotal_model(
    #                     vals.get('price_unit', 0.0),
    #                     vals.get('quantity', 0.0),
    #                     vals.get('discount', 0.0),
    #                     currency,
    #                     self.env['product.product'].browse(vals.get('product_id')),
    #                     partner,
    #                     taxes,
    #                     move.move_type,
    #                 ))
    #                 vals.update(self._get_fields_onchange_subtotal_model(
    #                     vals['price_subtotal'],
    #                     move.move_type,
    #                     currency,
    #                     move.company_id,
    #                     move.date,
    #                 ))
    #
    #     lines = super(AcocuntMoveLine, self).create(vals_list)
    #     return lines

    @api.model
    def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes,
                                            move_type, product_disc=0.00, product_didc_type=""):
        print("/////////////////// unit price --->", price_unit, "///////////", type(price_unit))
        print("/////////////////// qty --->", quantity)
        print("/////////////////// disc --->", self.product_disc)
        print("/////////////////// disc --->", product_disc, "/////", type(product_disc))

        res = {}
        if product_didc_type == 'fixed' and price_unit >= product_disc:
            print("////////////// --------- hello --------- ////////////")
            line_discount_price_unit = price_unit - (product_disc)
            print("///////////////--------------------- hello after --------------///////////")
        elif product_didc_type == 'variable' and product_disc <= 100.00 and product_disc >= 0.00:
            print("/////////////////////--------------- hiii ----------/////////////")
            line_discount_price_unit = price_unit * (1 - (product_disc / 100.0))
            print("/////////////////////--------------- hiii after ----------/////////////")
        else:
            line_discount_price_unit = price_unit * (1 - (discount / 100.0))
        subtotal = quantity * line_discount_price_unit
        print("/////////////////////////// line disc ----> ", line_discount_price_unit)
        print("/////////////////////////// subtitoal ----> ", subtotal)
        if taxes:
            taxes_res = taxes._origin.compute_all(line_discount_price_unit,
                                                  quantity=quantity, currency=currency, product=product,
                                                  partner=partner, is_refund=move_type in ('out_refund', 'in_refund'))
            res['price_subtotal'] = taxes_res['total_excluded']
            res['price_total'] = taxes_res['total_included']
        else:
            res['price_total'] = res['price_subtotal'] = subtotal
        # In case of multi currency, round before it's use for computing debit credit
        if currency:
            res = {k: currency.round(v) for k, v in res.items()}
            print("\n\n")
        return res


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    customer_names = fields.Many2one('sale.order', string='Customer Name')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_buyers = fields.One2many('sale.order', 'sale_order_details', string='Total Product Buyers')
    product_rating = fields.Float(string="Ratings")
    product_name = fields.Char(string='Product Name')
    manufecture_add = fields.Char(string='Manufecture Address')

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     print("//////////////////////------------------------- seller_ids---> ", self.seller_ids)
    #     print("/////////////// hii dp")
    #     args = args or []
    #     domain = []
    #     if name:
    #         domain = [('name', operator, name)]
    #     return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
