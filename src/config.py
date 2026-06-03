"""Project-level paths and default output locations."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample"

DEFAULT_CLEANED_PARQUET = PROCESSED_DATA_DIR / "supply_chain_cleaned.parquet"
DEFAULT_ANONYMIZED_SAMPLE_CSV = SAMPLE_DATA_DIR / "anonymized_supply_chain_sample.csv"

