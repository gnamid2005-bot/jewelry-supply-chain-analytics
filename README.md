# Jewelry Supply Chain Analytics with AI Insight Assistant

## Demo

- Live Streamlit Dashboard: [jewelry-supply-chain-analytics-btxw2gk2pqkzzqy7eqkapp.streamlit.app](https://jewelry-supply-chain-analytics-btxw2gk2pqkzzqy7eqkapp.streamlit.app)
- GitHub repository: public portfolio project for jewelry supply chain analytics, privacy-safe data processing, KPI reporting, and a Streamlit dashboard.
- Current demo data: anonymized sample data only.
- AI Insight Assistant: mock/local rule-based version, with no paid API calls.
- Raw company data is never uploaded to GitHub or Streamlit Cloud.

## Project Status

- Data pipeline completed.
- Anonymized sample data generated.
- Streamlit dashboard deployed.
- Tableau Public dashboard planned as next milestone.

An end-to-end supply chain analytics portfolio project for jewelry manufacturing and retail operations. The project will combine Python data processing, DuckDB analytics, an interactive Streamlit dashboard, Plotly visualizations, and a local rule-based AI insight assistant.

This public repository is intentionally built with anonymized sample data only. Raw company, internship, supplier, SKU, factory, and Excel files must never be committed. The public repository and live demo use anonymized sample data only. No proprietary company data, raw Excel files, real supplier names, real SKU identifiers, or confidential business information are included.

## Project Overview

The project analyzes monthly jewelry supply chain performance across SKU, factory type, factory, product category, product series, SKU source, order quantity, delivery quantity, and delivery labor value.

The goal is to turn operational data into a portfolio-ready analytics product that answers questions such as:

- Which product series drive the most delivery volume and labor value?
- How does fulfillment performance change by month?
- Which factories contribute the largest share of delivery?
- How concentrated is supplier dependency?
- How does in-house production compare with external sourcing?
- What insights can be generated automatically from dashboard filters?

## Business Context

Jewelry supply chains often involve high SKU complexity, mixed internal and external factory capacity, product series seasonality, and changing fulfillment pressure. A useful analytics workflow should connect operational metrics with business decisions:

- Monthly planning and delivery tracking
- SKU and product series portfolio review
- Factory contribution and sourcing mix analysis
- Supplier concentration risk monitoring
- Executive reporting with simple, repeatable KPI definitions

## Tech Stack

- Python for data processing and automation
- pandas and NumPy for tabular analytics
- DuckDB and PyArrow for local analytical storage
- openpyxl for local Excel ingestion when private files are available
- Streamlit for the public dashboard
- Plotly for interactive charts
- python-dotenv for local configuration only
- Jupyter and ipykernel for exploratory notebooks
- pytest for tests
- Ruff for linting

No paid APIs are required for the zero-budget version.

## Project Architecture

```text
Raw private Excel files
        |
        v
Local ingestion and cleaning scripts
        |
        v
Anonymized sample data and processed analytical tables
        |
        v
DuckDB / Parquet analytical layer
        |
        v
Streamlit dashboard + Plotly visualizations
        |
        v
Local rule-based AI Insight Assistant
```

## Dashboard Pages

The Streamlit dashboard reads only `data/sample/anonymized_supply_chain_sample.csv`.

- Supply Chain Overview: KPI cards, monthly order vs delivery trend, delivery labor value trend, fulfillment rate trend.
- Supplier Performance: factory type comparison, top factories, factory contribution share, supplier top 5 share, supplier HHI, sortable supplier table.
- Product Mix: product category contribution, product series contribution, SKU source distribution, average labor value per unit by category.
- SKU Drilldown: searchable SKU selection, monthly order/delivery/labor value trend, related factory and product attributes.
- AI Insight Assistant: local narrative insights generated from selected chart data and rule-based anomaly flags.

## Dashboard Preview

The deployed Streamlit dashboard uses anonymized sample data only. No raw company data is included.

### Executive Overview

![Executive Overview](assets/overview_dashboard.png)

### Supplier Performance

![Supplier Performance](assets/supplier_performance.png)

### Product Mix

![Product Mix](assets/product_mix.png)

### SKU Drill-down

![SKU Drill-down](assets/sku_drilldown.png)

### AI Insight Assistant

![AI Insight Assistant](assets/ai_insight_assistant.png)

The AI Insight Assistant is currently implemented as a mock/local rule-based module and does not call any paid API.

## AI Insight Assistant

The current version is mock/local and rule-based. It does not call the OpenAI API, local LLMs, paid APIs, raw data, or processed private data.

Current behavior:

- Read dashboard filter context and KPI outputs.
- Detect trend changes, delivery gaps, concentration risks, and high-contribution categories.
- Generate short business-readable insight bullets.
- Provide simple next-step prompts such as "review top gap factories" or "compare product series mix".
- Display a future LLM prompt template for portfolio storytelling.

Future versions may add optional OpenAI API or local LLM support, but only with local environment variables and never with committed API keys.

## Data Privacy Notice

This repository is safe for public GitHub use only when it contains anonymized sample data.

- Raw Excel files are not uploaded.
- Factory names are anonymized as `Factory_001`, `Factory_002`, and so on.
- SKU identifiers are anonymized as `SKU_000001`, `SKU_000002`, and so on.
- `image_path` values are removed from public data.
- Labor value metrics can be scaled by a consistent ratio.
- Public demos use anonymized sample data only.
- API keys, credentials, `.env`, and `.env.*` files are ignored and must not be committed.

See [docs/privacy_notice.md](docs/privacy_notice.md) for the detailed policy.

## Project Structure

```text
.
├── AGENTS.md
├── README.md
├── requirements.txt
├── assets/
├── dashboard/
│   ├── components/
│   └── pages/
├── data/
│   ├── dictionaries/
│   ├── processed/
│   ├── raw/
│   └── sample/
├── docs/
│   ├── data_dictionary.md
│   ├── kpi_definitions.md
│   └── privacy_notice.md
├── notebooks/
├── src/
└── tableau/
    └── screenshots/
```

## Roadmap

- Initialize repository safety rules and public project skeleton.
- Add anonymized sample data generator.
- Build reusable data cleaning and validation modules.
- Create DuckDB and Parquet analytical tables.
- Build Streamlit dashboard pages.
- Add local rule-based AI insight assistant.
- Add tests for KPI formulas and anonymization logic.
- Add Tableau screenshots or mockups for portfolio storytelling.
- Write a final case study with business insights and privacy-safe screenshots.

## How to Run

Place your private Excel file locally under `data/raw/`. Do not commit raw Excel files.

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Clean the private Excel file into a local parquet file:

```bash
python -m src.clean --input data/raw/your_file.xlsx
```

Create an anonymized public sample CSV:

```bash
python -m src.anonymize --max-rows 10000 --scale-factor 1.0
```

Commit only privacy-safe public data and code. In practice:

- Commit `data/sample/anonymized_supply_chain_sample.csv` after reviewing it.
- Do not commit files under `data/raw/`.
- Do not commit full processed private data such as `data/processed/supply_chain_cleaned.parquet`.
- Do not commit `.env`, API keys, credentials, or original Excel files.

Run the future Streamlit app:

```bash
streamlit run dashboard/streamlit_app.py
```

The dashboard uses only the anonymized sample CSV. If the sample file is missing, the app will show setup instructions instead of reading private folders.
