# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class EstatePropertyType(models.Model):
    _name = "estate.property.offer"
    _description = "Real estate property type"
    _order = "price desc"

    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)',
         'An offer price must be strictly positive.'),
    ]

    price = fields.Float()
    state = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if fields.Date.add(record.create_date, days=record.validity) != record.date_deadline:
                validity = record.date_deadline - record.create_date.date()
                record.validity = validity.days
    
    def action_accept_offer(self):
            if "accepted" in self.mapped("property_id.offer_ids.state"):
                raise UserError("An offer is already accepted.")
            else:
                self.state = "accepted"
                return self.property_id.write({
                    'selling_price':self.price,
                    'buyer_id':self.partner_id,
                    'state':'offer accepted',
                    })
    
    def action_refuse_offer(self):
            return self.write({'state':'refused'})
 