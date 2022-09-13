# -*- coding: utf-8 -*-

from odoo import models, fields


class Estate(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    def _default_date_availability(self):
        return fields.Date.add(fields.Date.today(), months=3)



    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: self._default_date_availability()
    )
    active = fields.Boolean(default=True)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('west', 'West'), ('east', 'East'), ('south', 'South')],
    )
    state = fields.Selection(
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled','Canceled')],
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type")
    saleman_id = fields.Many2one("res.users",copy=False,default=lambda self : self.env.user)
    buyer_id = fields.Many2one("res.partner")
    tag_ids = fields.Many2many("estate.property.tags", string="Tags")
