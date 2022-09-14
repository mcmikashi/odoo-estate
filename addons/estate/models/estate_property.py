# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class Estate(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'A property expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'A property selling price must be positive.')
    ]
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
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_offer_price = fields.Float(compute="_compute_best_offer_price")

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = self.living_area + self.garden_area
    
    @api.depends("offer_ids")
    def _compute_best_offer_price(self):
        for record in self:
            if record.offer_ids:
                record.best_offer_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''
    
    @api.constrains('expected_price','selling_price')
    def _check_price(self):
        for record in self:
            lowest_accepted_price = record.expected_price * 0.90
            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price,lowest_accepted_price, precision_digits=2) == -1:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")
    
    def action_sell(self):
        for record in self:
            if record.state == "cancel":
                raise UserError("You can't sell a property that is already canceled.")
            if not any(offer.state == 'accepted' for offer in record.offer_ids):
                raise UserError("You can't sell a property that doesn't have an accepted offer.")
        return self.write({"state": "sold"})
    
    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("You can't cancel a property that is already sold.")
        return self.write({"state": "canceled"})
