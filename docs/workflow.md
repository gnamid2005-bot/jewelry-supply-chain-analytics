# Project Workflow

This project separates private local processing from the public portfolio demo.

## Data Flow

```text
Private raw Excel file
        |
        | stays local under data/raw/
        v
python -m src.clean --input data/raw/your_file.xlsx
        |
        | writes local-only cleaned parquet
        v
data/processed/supply_chain_cleaned.parquet
        |
        | anonymize and generalize public fields
        v
python -m src.anonymize --max-rows 10000 --scale-factor 1.0
        |
        | reviewed public demo dataset
        v
data/sample/anonymized_supply_chain_sample.csv
        |
        | committed to GitHub and deployed
        v
Streamlit dashboard and Streamlit Cloud
```

## Commit Boundary

Only anonymized sample data is committed. The public repository may include:

- source code,
- documentation,
- screenshots based on anonymized sample data,
- `data/sample/anonymized_supply_chain_sample.csv`.

The public repository must not include:

- raw Excel files,
- files under `data/raw/` except `.gitkeep`,
- full private processed files under `data/processed/` except `.gitkeep`,
- real supplier names,
- real SKU identifiers,
- product image paths,
- raw product descriptions,
- mapping tables from real values to anonymized values,
- `.env`, API keys, credentials, or secrets.

## Public Demo Rules

The deployed Streamlit dashboard reads only `data/sample/anonymized_supply_chain_sample.csv`. It does not read `data/raw/` or `data/processed/`.

The AI Insight Assistant is a local rule-based analytics module. It uses in-memory dashboard aggregations from `data/sample/anonymized_supply_chain_sample.csv` and does not call paid APIs, external LLMs, raw data, or processed private data.

It currently generates structured insights for:

- Executive Overview,
- Supplier Performance,
- Product Mix,
- SKU Drill-down.

The assistant is privacy-safe and zero-budget because it works only with anonymized sample-data summaries. It does not expose real supplier names, real SKU identifiers, raw product descriptions, product image paths, internal labels, or mapping tables.
