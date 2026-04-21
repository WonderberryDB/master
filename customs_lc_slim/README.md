# Customs Duty on Landed Costs (slim)

Minimal Odoo module — no extra tabs, no buttons, no new screens.

## What it adds

**On the product (Purchase tab):**
- `Subject to Customs Duty` toggle
- `Customs Duty Rate (%)` — set once, reused on every shipment
- Inherits from product category if left at 0

**On the Landed Cost → Valuation Adjustments tab:**
- `Duty %` column — pre-filled from the product, **editable per shipment**
- `Duty Amt` column — computed automatically (`line value × duty %`)
- `Total Customs Duty` subtotal below the table

That's it. The duty amount is included in the final valuation when you Validate.

---

## Deploy on Odoo.sh

1. Drop `customs_lc_slim/` into your custom addons repo
2. Push → Odoo.sh rebuilds
3. Settings → Apps → search **Customs Duty** → Install

## Requirements
- Product categories must use **AVCO or FIFO** costing
- Inventory valuation: **Automated**
- Landed Costs feature enabled in Inventory → Configuration → Settings
