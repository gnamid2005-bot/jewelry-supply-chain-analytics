"""Clean private jewelry supply chain Excel data into an analytical parquet file.

This module intentionally does not know any real company file names. Users pass a
local Excel file path under data/raw/ when running the command.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.config import DEFAULT_CLEANED_PARQUET, PROJECT_ROOT, RAW_DATA_DIR


COLUMN_MAPPING = {
    "年-月": "year_month",
    "中央模号": "sku_id",
    "工厂类型": "factory_type",
    "工厂": "factory",
    "管理大类": "product_category",
    "产品系列": "product_series",
    "工值单价": "labor_unit_price",
    "模号图片路径": "image_path",
    "SKU来源": "sku_source",
    "月度发单件数": "monthly_order_qty",
    "月度起货件数": "monthly_delivery_qty",
    "月度起货工值": "monthly_delivery_labor_value",
    "中模描述": "product_description",
}

NUMERIC_COLUMNS = [
    "labor_unit_price",
    "monthly_order_qty",
    "monthly_delivery_qty",
    "monthly_delivery_labor_value",
]


def resolve_raw_input_path(input_path: str | Path) -> Path:
    """Resolve and validate a user-provided Excel path under data/raw/."""
    path = Path(input_path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path

    resolved = path.resolve()
    raw_dir = RAW_DATA_DIR.resolve()

    if not resolved.is_relative_to(raw_dir):
        raise ValueError(f"Input file must be under {RAW_DATA_DIR}")

    if resolved.suffix.lower() not in {".xlsx", ".xls", ".xlsm"}:
        raise ValueError("Input file must be an Excel file with .xlsx, .xls, or .xlsm suffix")

    return resolved


def normalize_column_name(column: object) -> str:
    """Strip extra whitespace from a source column name."""
    return str(column).strip()


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename known Chinese source fields to English snake_case names."""
    cleaned = df.copy()
    cleaned.columns = [normalize_column_name(column) for column in cleaned.columns]
    return cleaned.rename(columns=COLUMN_MAPPING)


def parse_year_month(series: pd.Series) -> pd.Series:
    """Parse year-month values to month-start timestamps."""
    normalized = (
        series.astype("string")
        .str.strip()
        .str.replace("年", "-", regex=False)
        .str.replace("月", "", regex=False)
    )
    parsed = pd.to_datetime(normalized, errors="coerce")
    return parsed.dt.to_period("M").dt.to_timestamp()


def to_numeric(series: pd.Series) -> pd.Series:
    """Convert formatted numeric values to pandas numeric dtype."""
    normalized = (
        series.astype("string")
        .str.strip()
        .str.replace(",", "", regex=False)
        .str.replace("，", "", regex=False)
    )
    return pd.to_numeric(normalized, errors="coerce")


def clean_supply_chain_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned supply chain dataframe ready for analytics."""
    cleaned = standardize_columns(df)

    if "year_month" in cleaned.columns:
        cleaned["year_month"] = parse_year_month(cleaned["year_month"])

    for column in NUMERIC_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = to_numeric(cleaned[column])

    return cleaned


def build_cleaning_log(df: pd.DataFrame) -> dict[str, Any]:
    """Build a compact cleaning log with shape and missing-value diagnostics."""
    return {
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "columns": list(df.columns),
        "missing_values": {column: int(value) for column, value in df.isna().sum().items()},
    }


def clean_excel_file(input_path: str | Path, output_path: str | Path = DEFAULT_CLEANED_PARQUET) -> dict[str, Any]:
    """Read a private Excel file, clean it, write parquet, and return diagnostics."""
    source_path = resolve_raw_input_path(input_path)
    destination_path = Path(output_path)
    if not destination_path.is_absolute():
        destination_path = PROJECT_ROOT / destination_path

    raw_df = pd.read_excel(source_path)
    cleaned_df = clean_supply_chain_data(raw_df)

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_parquet(destination_path, index=False)

    log = build_cleaning_log(cleaned_df)
    log["input_path"] = str(source_path.relative_to(PROJECT_ROOT))
    log["output_path"] = str(destination_path.relative_to(PROJECT_ROOT))
    return log


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Clean private supply chain Excel data.")
    parser.add_argument(
        "--input",
        required=True,
        help="Excel path under data/raw/, for example data/raw/your_file.xlsx",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_CLEANED_PARQUET),
        help="Output parquet path. Defaults to data/processed/supply_chain_cleaned.parquet",
    )
    return parser.parse_args()


def main() -> None:
    """Run the cleaning command."""
    args = parse_args()
    log = clean_excel_file(args.input, args.output)
    print(json.dumps(log, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

