"""Privacy-safe sample data loader for the Streamlit dashboard."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from dashboard.i18n import t


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DATA_PATH = PROJECT_ROOT / "data" / "sample" / "anonymized_supply_chain_sample.csv"

NUMERIC_COLUMNS = [
    "labor_unit_price",
    "monthly_order_qty",
    "monthly_delivery_qty",
    "monthly_delivery_labor_value",
]


@st.cache_data(show_spinner=False)
def _read_sample_data(csv_path: str, modified_time_ns: int, file_size: int) -> pd.DataFrame:
    """Read anonymized sample data with file metadata included in the cache key."""
    _ = modified_time_ns, file_size
    df = pd.read_csv(csv_path)
    if "year_month" in df.columns:
        df["year_month"] = pd.to_datetime(df["year_month"], errors="coerce")

    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    return df


def load_sample_data() -> pd.DataFrame:
    """Load anonymized public sample data only from the repository sample CSV."""
    if not SAMPLE_DATA_PATH.exists():
        return pd.DataFrame()

    file_stat = SAMPLE_DATA_PATH.stat()
    return _read_sample_data(
        csv_path=str(SAMPLE_DATA_PATH),
        modified_time_ns=file_stat.st_mtime_ns,
        file_size=file_stat.st_size,
    )


def show_missing_sample_data_message(lang: str = "en") -> None:
    """Show setup instructions when the public sample CSV is not present."""
    st.info(t("missing_sample_info", lang))
    st.caption(t("privacy_caption", lang))
