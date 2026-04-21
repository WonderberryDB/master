# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    customs_duty_rate = fields.Float(
        string='Customs Duty Rate (%)',
        digits=(5, 2),
        default=0.0,
        help="Default duty rate for all products in this category. "
             "Override on the individual product if needed.",
    )


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_dutiable = fields.Boolean(
        string='Subject to Customs Duty',
        default=False,
    )
    customs_duty_rate = fields.Float(
        string='Customs Duty Rate (%)',
        digits=(5, 2),
        default=0.0,
        help="Leave 0 to inherit from the product category.",
    )
    effective_duty_rate = fields.Float(
        string='Effective Duty Rate (%)',
        compute='_compute_effective_duty_rate',
        store=True,
        digits=(5, 2),
    )

    @api.depends('is_dutiable', 'customs_duty_rate', 'categ_id.customs_duty_rate')
    def _compute_effective_duty_rate(self):
        for t in self:
            if not t.is_dutiable:
                t.effective_duty_rate = 0.0
            elif t.customs_duty_rate > 0:
                t.effective_duty_rate = t.customs_duty_rate
            else:
                t.effective_duty_rate = t.categ_id.customs_duty_rate
