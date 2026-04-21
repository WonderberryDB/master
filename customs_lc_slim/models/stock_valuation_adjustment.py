# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AdjustmentLines(models.Model):
    """
    Extends the existing valuation adjustment lines on a Landed Cost.
    These are the rows you see when you click 'Compute' on a Landed Cost —
    one row per product per cost line.

    We add:
      - customs_duty_rate  : editable %, pre-filled from the product
      - customs_duty_amount: computed = line_value × duty_rate
      - final_cost_adjusted: overrides the base field to include duty
    """
    _inherit = 'stock.valuation.adjustment.lines'

    customs_duty_rate = fields.Float(
        string='Duty %',
        digits=(5, 2),
        default=0.0,
        help="Customs duty rate for this line. Pre-filled from the product — "
             "edit here to override for this shipment only.",
    )
    customs_duty_amount = fields.Monetary(
        string='Duty Amt',
        compute='_compute_duty_amount',
        store=True,
        currency_field='currency_id',
        help="Duty amount = line value × duty %. "
             "This is added on top of the allocated landed cost.",
    )
    currency_id = fields.Many2one(
        related='cost_id.currency_id',
        string='Currency',
    )

    @api.depends('former_cost', 'customs_duty_rate')
    def _compute_duty_amount(self):
        for line in self:
            if line.customs_duty_rate > 0 and line.former_cost > 0:
                line.customs_duty_amount = line.former_cost * (line.customs_duty_rate / 100.0)
            else:
                line.customs_duty_amount = 0.0

    @api.onchange('product_id')
    def _onchange_product_id_duty(self):
        """Pre-fill duty rate from product when product changes."""
        if self.product_id and self.product_id.product_tmpl_id.is_dutiable:
            self.customs_duty_rate = self.product_id.product_tmpl_id.effective_duty_rate
        else:
            self.customs_duty_rate = 0.0

    def _get_final_cost(self):
        """
        Override: final cost = standard allocated cost + duty amount.
        Called by Odoo's valuation engine when posting journal entries.
        """
        self.ensure_one()
        base = super()._get_final_cost()
        return base + self.customs_duty_amount


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    total_customs_duty = fields.Monetary(
        string='Total Customs Duty',
        compute='_compute_total_customs_duty',
        currency_field='currency_id',
    )

    @api.depends('valuation_adjustment_lines.customs_duty_amount')
    def _compute_total_customs_duty(self):
        for lc in self:
            lc.total_customs_duty = sum(
                lc.valuation_adjustment_lines.mapped('customs_duty_amount')
            )

    def button_validate(self):
        """
        Before validating, auto-fill duty rates from products
        for any lines that haven't been manually set.
        """
        for lc in self:
            for line in lc.valuation_adjustment_lines:
                if line.customs_duty_rate == 0 and line.product_id:
                    tmpl = line.product_id.product_tmpl_id
                    if tmpl.is_dutiable and tmpl.effective_duty_rate > 0:
                        line.customs_duty_rate = tmpl.effective_duty_rate
        return super().button_validate()
