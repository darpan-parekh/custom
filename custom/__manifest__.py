{
    'name': "Customer Management",
    'website': "https://google.com",
    'sequence': 1,
    'summary': "Managing customer details",
    'author': "customer",
    'version': '1.0',
    'category': '',
    'description':
        """
hello i am darpan 
=================
i created this line
___________________
i hope u like it.
hii
hello
    
    * hii
    * hello
    * damn yaah    
    """,
    'depends': ['base', 'sale', 'account', 'stock', 'crm', 'purchase', 'product'],
    'data': [
        'security/ir.model.access.csv',
        # 'views/sale_order_view.xml',
        'views/custom_invoice_view.xml',
        'views/user_commission.xml',
        'wizard/custom_wizard.xml',
        'wizard/custom_wizard_line.xml',
        'report/sale_order_report.xml',
        'data/product_data.xml',
        'data/send_mail_template.xml',

    ],
    'demo': [],
    'installable': True
}
