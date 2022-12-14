# -*- coding: utf-8 -*-
{
    "name": "estate",
    "summary": """Small app for sell house""",
    "description": """
        Long description of module's purpose
    """,
    "author": "Mickaël Anicette",
    "website": "https://mickaelanicette.000webhostapp.com/",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Real Estate/Brokerage",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base"],
    # always loaded
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_offer_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tags_views.xml",
        "views/estate_user_views.xml",
        "views/menu.xml",
        "views/templates.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
