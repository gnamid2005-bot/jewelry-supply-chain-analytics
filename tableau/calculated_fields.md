# Tableau Calculated Fields

These calculated fields are designed for Tableau Public using `data/sample/anonymized_supply_chain_sample.csv`.

## Fulfillment Rate

```text
SUM([monthly_delivery_qty]) / SUM([monthly_order_qty])
```

Format as percentage. If needed, wrap with a zero-division guard:

```text
IF SUM([monthly_order_qty]) = 0 THEN 0
ELSE SUM([monthly_delivery_qty]) / SUM([monthly_order_qty])
END
```

## Delivery Gap

```text
SUM([monthly_order_qty]) - SUM([monthly_delivery_qty])
```

Positive values indicate order quantity greater than delivery quantity.

## Monthly Order Quantity

```text
SUM([monthly_order_qty])
```

Use with `year_month` in a monthly trend chart.

## Monthly Delivery Quantity

```text
SUM([monthly_delivery_qty])
```

Use with `year_month` in a monthly trend chart.

## Delivery Labor Value

```text
SUM([monthly_delivery_labor_value])
```

Use as the primary value metric for contribution and concentration views.

## Supplier Contribution

```text
SUM([monthly_delivery_labor_value]) / TOTAL(SUM([monthly_delivery_labor_value]))
```

Use in views where `factory` is on rows, columns, marks, or detail.

## Product Category Share

```text
SUM([monthly_delivery_labor_value]) / TOTAL(SUM([monthly_delivery_labor_value]))
```

Use in views where `product_category` is the main dimension.

## SKU Activity Count

```text
COUNTD(
    IF [monthly_order_qty] > 0 OR [monthly_delivery_qty] > 0
    THEN [sku_id]
    END
)
```

Use as a KPI card or trend metric.

## Average Labor Value per Unit

```text
IF SUM([monthly_delivery_qty]) = 0 THEN 0
ELSE SUM([monthly_delivery_labor_value]) / SUM([monthly_delivery_qty])
END
```

Use for product category or product series unit-value comparison.

## Supplier Concentration Proxy

Tableau Public can approximate supplier concentration with a squared contribution calculation:

```text
POWER(
    SUM([monthly_delivery_labor_value]) / TOTAL(SUM([monthly_delivery_labor_value])),
    2
)
```

Then sum the result across factories in the view:

```text
WINDOW_SUM([Supplier Contribution Squared])
```

This is a Tableau-friendly proxy for HHI-style supplier concentration. Use it as a directional portfolio metric rather than a formal risk model.

