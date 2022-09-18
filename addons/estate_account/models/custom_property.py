from odoo import models, Command

class InheritedModel(models.Model):
    _inherit = "estate.property"

    def action_sell(self):
        journal = self.env['account.move'].sudo().with_context(default_move_type='out_invoice')._get_default_journal()
        self.env["account.move"].sudo().create({
            'partner_id':self.buyer_id,
            'move_type':'out_invoice',
            'journal_id':journal.id,
            "invoice_line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": self.selling_price,
                }),
                Command.create({
                    "name": "Administative fee",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06,
                })
            ]
        })
        return super().action_sell()