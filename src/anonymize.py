"""Create privacy-safe sample data from the cleaned analytical parquet file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.config import DEFAULT_ANONYMIZED_SAMPLE_CSV, DEFAULT_CLEANED_PARQUET, PROJECT_ROOT


SENSITIVE_COLUMNS = ["image_path", "product_description"]
SCALABLE_COLUMNS = ["labor_unit_price", "monthly_delivery_labor_value"]


def _build_mapping(values: pd.Series, prefix: str, width: int) -> dict[Any, str]:
    """Build a stable anonymization mapping for non-null values."""
    unique_values = sorted(values.dropna().astype(str).unique())
    return {value: f"{prefix}_{index:0{width}d}" for index, value in enumerate(unique_values, start=1)}


def anonymize_supply_chain_data(
    df: pd.DataFrame,
    max_rows: int = 10_000,
    scale_factor: float = 1.0,
) -> pd.DataFrame:
    """Return an anonymized sample dataframe safe for public demos."""
    if max_rows <= 0:
        raise ValueError("max_rows must be greater than 0")

    anonymized = df.head(max_rows).copy()

    if "factory" in anonymized.columns:
        factory_mapping = _build_mapping(anonymized["factory"], "Factory", 3)
        anonymized["factory"] = anonymized["factory"].astype("string").map(factory_mapping)

    if "sku_id" in anonymized.columns:
        sku_mapping = _build_mapping(anonymized["sku_id"], "SKU", 6)
        anonymized["sku_id"] = anonymized["sku_id"].astype("string").map(sku_mapping)

    for column in SCALABLE_COLUMNS:
        if column in anonymized.columns:
            anonymized[column] = pd.to_numeric(anonymized[column], errors="coerce") * scale_factor

    columns_to_drop = [column for column in SENSITIVE_COLUMNS if column in anonymized.columns]
    if columns_to_drop:
        anonymized = anonymized.drop(columns=columns_to_drop)

    return anonymized


def anonymize_parquet_file(
    input_path: str | Path = DEFAULT_CLEANED_PARQUET,
    output_path: str | Path = DEFAULT_ANONYMIZED_SAMPLE_CSV,
    max_rows: int = 10_000,
    scale_factor: float = 1.0,
) -> dict[str, Any]:
    """Read cleaned parquet, write anonymized sample CSV, and return diagnostics."""
    source_path = Path(input_path)
    destination_path = Path(output_path)
    if not source_path.is_absolute():
        source_path = PROJECT_ROOT / source_path
    if not destination_path.is_absolute():
        destination_path = PROJECT_ROOT / destination_path

    df = pd.read_parquet(source_path)
    anonymized = anonymize_supply_chain_data(df, max_rows=max_rows, scale_factor=scale_factor)

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    anonymized.to_csv(destination_path, index=False)

    return {
        "input_path": str(source_path.relative_to(PROJECT_ROOT)),
        "output_path": str(destination_path.relative_to(PROJECT_ROOT)),
        "source_rows": int(len(df)),
        "sample_rows": int(len(anonymized)),
        "sample_columns": list(anonymized.columns),
        "scale_factor": scale_factor,
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Create anonymized public sample data.")
    parser.add_argument(
        "--input",
        default=str(DEFAULT_CLEANED_PARQUET),
        help="Cleaned parquet path. Defaults to data/processed/supply_chain_cleaned.parquet",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_ANONYMIZED_SAMPLE_CSV),
        help="Output sample CSV path. Defaults to data/sample/anonymized_supply_chain_sample.csv",
    )
    parser.add_argument("--max-rows", type=int, default=10_000, help="Maximum public sample rows.")
    parser.add_argument(
        "--scale-factor",
        type=float,
        default=1.0,
        help="Uniform scaling factor for labor value fields.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the anonymization command."""
    args = parse_args()
    log = anonymize_parquet_file(
        input_path=args.input,
        output_path=args.output,
        max_rows=args.max_rows,
        scale_factor=args.scale_factor,
    )
    print(json.dumps(log, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

