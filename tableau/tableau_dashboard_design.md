# Tableau Dashboard Design

This Tableau Public design uses only `data/sample/anonymized_supply_chain_sample.csv`. The data is anonymized and generalized for public demo use.

## Page 1: Executive Overview

### Business Question

How is the supply chain performing overall by month, and are order, delivery, labor value, and fulfillment trends moving in a healthy direction?

### Charts to Build

- Monthly Order vs Delivery Quantity line chart
- Monthly Delivery Labor Value line chart
- Monthly Fulfillment Rate line chart
- Delivery Gap bar chart by month

### Fields to Use

- `year_month`
- `monthly_order_qty`
- `monthly_delivery_qty`
- `monthly_delivery_labor_value`
- calculated `Fulfillment Rate`
- calculated `Delivery Gap`
- `active SKU count`

### Filters

- `year_month`
- `factory_type`
- `product_category`
- `product_series`
- `sku_source`

### KPI Cards

- Total Order Quantity
- Total Delivery Quantity
- Delivery Labor Value
- Fulfillment Rate
- Active SKU Count

### Recommended Layout

- Top row: five KPI cards.
- Middle row: wide Monthly Order vs Delivery Quantity trend.
- Bottom row: Delivery Labor Value trend on the left and Fulfillment Rate trend on the right.
- Optional side panel: global filters.

### Interpretation Notes

- Fulfillment rate below target may indicate delivery capacity pressure or delayed fulfillment.
- Delivery quantity above order quantity can happen when prior-month backlog is delivered.
- Rising delivery labor value with flat delivery quantity may indicate product mix shifting toward higher-value work.

## Page 2: Supplier Performance

### Business Question

Which anonymized factories contribute the most delivery labor value, and is supplier concentration creating dependency risk?

### Charts to Build

- Factory Type comparison bar chart
- Top 10 factories by delivery labor value
- Factory contribution share treemap
- Supplier concentration proxy view
- Sortable supplier table

### Fields to Use

- `factory`
- `factory_type`
- `monthly_order_qty`
- `monthly_delivery_qty`
- `monthly_delivery_labor_value`
- calculated `Supplier Contribution`
- calculated `Fulfillment Rate`
- calculated `Supplier Concentration Proxy`

### Filters

- `year_month`
- `factory_type`
- `product_category`
- `product_series`
- `sku_source`

### KPI Cards

- Supplier Top 5 Share
- Supplier Concentration Proxy
- Delivery Labor Value
- Total Delivery Quantity

### Recommended Layout

- Top row: supplier concentration KPI cards.
- Left: Factory Type comparison.
- Right: Top 10 factories by delivery labor value.
- Bottom: Factory contribution treemap and sortable supplier table.

### Interpretation Notes

- A high top-five supplier share suggests delivery value is concentrated among a small number of factories.
- Compare factory type and factory contribution together to understand whether concentration is coming from in-house or external capacity.
- The supplier table should support sorting by labor value, delivery quantity, fulfillment rate, and contribution share.

## Page 3: Product Mix Analysis

### Business Question

Which product categories, product series, and SKU sources drive delivery value and unit economics?

### Charts to Build

- Product Category contribution bar chart
- Product Series contribution treemap or ranked bar chart
- SKU Source distribution donut or bar chart
- Average Labor Value per Unit by Product Category

### Fields to Use

- `product_category`
- `product_series`
- `sku_source`
- `monthly_delivery_qty`
- `monthly_delivery_labor_value`
- `labor_unit_price`
- calculated `Product Category Share`
- calculated `Average Labor Value per Unit`

### Filters

- `year_month`
- `factory_type`
- `factory`
- `product_category`
- `sku_source`

### KPI Cards

- Delivery Labor Value
- Total Delivery Quantity
- Average Labor Value per Unit
- Active SKU Count

### Recommended Layout

- Top row: product mix KPI cards.
- Middle left: Product Category contribution.
- Middle right: SKU Source distribution.
- Bottom: Product Series contribution and Average Labor Value per Unit by category.

### Interpretation Notes

- A category with high delivery value but low delivery quantity may represent higher labor intensity or higher-value products.
- SKU source distribution helps separate internal design, external purchase, customer order, and other public categories.
- Use product series only as anonymized labels such as `Series_001`.

## Page 4: SKU Drill-down

### Business Question

For a selected anonymized SKU, how do order quantity, delivery quantity, delivery labor value, and related dimensions change over time?

### Charts to Build

- SKU selector/search filter
- Monthly Order vs Delivery Quantity line chart for selected SKU
- Monthly Delivery Labor Value trend for selected SKU
- SKU attribute summary table
- Related factory and product context table

### Fields to Use

- `sku_id`
- `year_month`
- `factory`
- `factory_type`
- `product_category`
- `product_series`
- `sku_source`
- `monthly_order_qty`
- `monthly_delivery_qty`
- `monthly_delivery_labor_value`
- calculated `Fulfillment Rate`
- calculated `Delivery Gap`

### Filters

- `sku_id`
- `year_month`
- `factory_type`
- `factory`
- `product_category`
- `product_series`
- `sku_source`

### KPI Cards

- Selected SKU Order Quantity
- Selected SKU Delivery Quantity
- Selected SKU Delivery Labor Value
- Selected SKU Fulfillment Rate

### Recommended Layout

- Top: search/filter control for `sku_id`.
- First row: selected SKU KPI cards.
- Middle: monthly trend chart for order, delivery, and delivery labor value.
- Bottom: related factory, factory type, product category, product series, and SKU source table.

### Interpretation Notes

- Use SKU drill-down after identifying a monthly gap, high-value category, or supplier concentration pattern.
- Because SKU identifiers are anonymized, focus on operational patterns rather than real product identity.
- Do not add product images or raw product descriptions to Tableau Public.

