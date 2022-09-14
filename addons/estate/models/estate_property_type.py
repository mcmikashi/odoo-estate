# -*- coding: utf-8 -*-

from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"
    _order = "sequence, name"

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
