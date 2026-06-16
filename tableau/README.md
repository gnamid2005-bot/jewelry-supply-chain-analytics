# Tableau Public Dashboard Guide

This folder contains the design package for manually recreating the supply chain analytics dashboard in Tableau Public.

## Data Source

Use only:

```text
data/sample/anonymized_supply_chain_sample.csv
```

Do not use:

- `data/raw/`
- `data/processed/`
- raw Excel files
- real supplier names
- real SKU identifiers
- product image paths
- raw product descriptions
- mapping tables from real values to anonymized values

## Reproduction Steps

1. Open Tableau Public.
2. Connect to `data/sample/anonymized_supply_chain_sample.csv`.
3. Confirm field types:
   - `year_month`: Date or Date & Time
   - quantity fields: Number
   - labor value fields: Number
   - anonymized categories: String
4. Create the calculated fields listed in [calculated_fields.md](calculated_fields.md).
5. Build the four dashboard pages described in [tableau_dashboard_design.md](tableau_dashboard_design.md):
   - Executive Overview
   - Supplier Performance
   - Product Mix Analysis
   - SKU Drill-down
6. Use [storyboard.md](storyboard.md) to guide the dashboard narrative.
7. Publish to Tableau Public only after confirming the workbook uses anonymized sample data.

## Recommended Workbook Structure

- One worksheet per chart.
- One dashboard per page.
- One shared filter set for `year_month`, `factory_type`, `product_category`, `product_series`, and `sku_source`.
- Consistent colors for factory type and product category across pages.

## Portfolio Notes

Keep the tone professional and transparent:

- This is an independent student portfolio project.
- The project is inspired by internship experience.
- The public workbook uses anonymized and generalized sample data only.
- It is not a company production system.
- No paid APIs or confidential datasets are required.

