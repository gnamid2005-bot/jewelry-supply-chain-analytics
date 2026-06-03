# KPI Definitions

These KPI definitions describe the first public dashboard version. All calculations must run on anonymized sample data or locally held private data that is never committed.

| KPI | 业务含义 | Formula | 适合图表 | 适合页面 |
| --- | --- | --- | --- | --- |
| Total Order Quantity | 衡量指定期间内的发单总规模。 | `sum(monthly_order_qty)` | KPI card, line chart, stacked bar | Executive Overview, Monthly Trend |
| Total Delivery Quantity | 衡量指定期间内的起货总规模。 | `sum(monthly_delivery_qty)` | KPI card, line chart, bar chart | Executive Overview, Monthly Trend |
| Delivery Labor Value | 衡量已起货产品对应的总工值贡献。 | `sum(monthly_delivery_labor_value)` | KPI card, line chart, treemap | Executive Overview, Product Series |
| Fulfillment Rate | 衡量起货对发单的满足程度。 | `sum(monthly_delivery_qty) / sum(monthly_order_qty)` | KPI card, line chart, gauge, heatmap | Executive Overview, Factory Performance |
| Delivery Gap | 衡量发单与起货之间的数量缺口。 | `sum(monthly_order_qty) - sum(monthly_delivery_qty)` | Bar chart, waterfall, variance table | Monthly Trend, Factory Performance |
| Factory Contribution Share | 衡量各工厂对起货量或工值的贡献占比。 | `factory_metric / total_metric`, where metric is delivery quantity or labor value | Stacked bar, treemap, donut chart | Factory Performance |
| In-house vs External Share | 比较内部工厂与外部工厂的供应贡献结构。 | `sum(metric by factory_type) / sum(metric)` | Stacked area, donut chart, segmented bar | Factory Performance, Sourcing Mix |
| Active SKU Count | 衡量期间内有发单或起货记录的活跃 SKU 数量。 | `count_distinct(sku_id where monthly_order_qty > 0 or monthly_delivery_qty > 0)` | KPI card, line chart, histogram | SKU Analysis |
| Product Series Contribution | 衡量产品系列对起货量和工值的贡献。 | `sum(metric by product_series) / sum(metric)` | Treemap, stacked bar, Pareto chart | Product Series |
| Average Labor Value per Unit | 衡量单位起货件数对应的平均工值。 | `sum(monthly_delivery_labor_value) / sum(monthly_delivery_qty)` | KPI card, line chart, box plot | Executive Overview, Product Series |
| Supplier Top 5 Share | 衡量前五大供应工厂的集中度。 | `sum(metric for top 5 factories) / sum(metric)` | KPI card, Pareto chart, ranked bar | Supplier Concentration |
| Supplier HHI | 衡量供应商集中度和依赖风险。 | `sum((factory_metric / total_metric)^2)` | KPI card, trend line, risk table | Supplier Concentration, Risk View |

Recommended metric choices:

- Use `monthly_delivery_qty` for volume contribution.
- Use `monthly_delivery_labor_value` for value contribution.
- Show both when the business question involves capacity and value mix.

