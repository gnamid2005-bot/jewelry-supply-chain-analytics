# Privacy Notice

This repository is designed for a public portfolio project. It must not expose real company, internship, supplier, product, or operational data.

## Data Handling Rules

- Raw Excel files are never uploaded to GitHub.
- Real factory names are anonymized to values such as `Factory_001`.
- Factory type values are generalized to public categories such as `In-house`, `External`, `Partner`, `Unknown`, or `Other`.
- Real SKU identifiers are anonymized to values such as `SKU_000001`.
- Product categories are generalized to public categories such as `Gem-set Jewelry`, `K-Gold & Platinum`, `Gold Jewelry`, `Fixed-price Gold`, `Unknown`, or `Other`.
- Product series values are anonymized to values such as `Series_001`.
- SKU source values are generalized to public categories such as `Internal Design`, `External Purchase`, `Customer Order`, `Unknown`, or `Other`.
- `image_path` values are removed from public demo data.
- Labor value metrics may be scaled by a consistent ratio before publication.
- Public demos use anonymized sample data only.
- API keys, credentials, `.env`, and `.env.*` files are never uploaded.

## Public Demo Scope

The public version should preserve the analytical structure of the supply chain problem while removing sensitive values. Sample data may show realistic patterns, such as seasonality, factory mix, fulfillment gaps, and product series contribution, but it must not allow reconstruction of real company operations.

## Private Data Scope

Private raw data can be used locally for development and validation only. It should remain under ignored paths such as `data/raw/` and must not be committed, pushed, or included in screenshots.
