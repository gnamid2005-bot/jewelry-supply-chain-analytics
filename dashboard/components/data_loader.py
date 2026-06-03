"""Privacy-safe sample data loader for the Streamlit dashboard."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DATA_PATH = PROJECT_ROOT / "data" / "sample" / "anonymized_supply_chain_sample.csv"

NUMERIC_COLUMNS = [
    "labor_unit_price",
    "monthly_order_qty",
    "monthly_delivery_qty",
    "monthly_delivery_labor_value",
]


@st.cache_data(show_spinner=False)
def load_sample_data() -> pd.DataFrame:
    """Load anonymized public sample data only."""
    if not SAMPLE_DATA_PATH.exists():
        return pd.DataFrame()

    df = pd.read_csv(SAMPLE_DATA_PATH)
    if "year_month" in df.columns:
        df["year_month"] = pd.to_datetime(df["year_month"], errors="coerce")

    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    return df


def show_missing_sample_data_message() -> None:
    """Show setup instructions when the public sample CSV is not present."""
    st.info(
        "No anonymized sample data found yet. Generate it locally with "
        "`python -m src.anonymize --max-rows 10000 --scale-factor 1.0`, then rerun the app."
    )
    st.caption("The dashboard intentionally does not read `data/raw/` or `data/processed/`.")

