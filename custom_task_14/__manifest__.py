# -*- coding: utf-8 -*-

{
    'name' : 'Invoice Report',
    'version' : '1.1',
    'summary': 'Invoices & Payments Report',
    'sequence': 10,
    'description': """e
Invoicing & Payments Report Customisation
=========================================
The specific and easy-to-use Invoicing system in Odoo allows you to keep track of your accounting, even when you are not an accountant. It provides an easy way to follow up on your vendors and customers.

You could use this simplified accounting in case you work with an (external) account to keep your books, and you still want to keep track of payments. This module also offers you an easy method of registering payments, without having to encode complete abstracts of account.
    """,
    'category': 'Accounting/Accounting',
    'depends' : ['account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/print_multi_invoice_view.xml',
        ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
