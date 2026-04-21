# -*- coding: utf-8 -*-
{
    'name': 'Customs Duty on Landed Costs',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Per-product duty % on landed cost valuation lines — inline, no extra tabs',
    'depends': ['stock_landed_costs'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/landed_cost_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
