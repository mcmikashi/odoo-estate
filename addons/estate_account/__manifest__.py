# -*- coding: utf-8 -*-
{
    'name': "estate_account",

    'summary': """
       Estate module with invoice""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Mickael Anicette",
    'website': "https://mickaelanicette.000webhostapp.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['estate', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
