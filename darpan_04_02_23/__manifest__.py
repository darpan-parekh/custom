# -*- coding: utf-8 -*-

{
    'name' : 'Manufacturing Record',
    'version' : '1.1',
    'summary': 'Linking Manufacturing Location and Sale Location',
    'sequence': 10,
    'description': """
Linking Manufacturing Location and Sale 
=======================================
    """,
    'category': 'Sale/Sale',
    'depends' : ['sale_management', 'mrp', 'purchase'],
    'data': [
        'views/mrp_producttion_view.xml',
        'views/sale_view.xml',
        ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
