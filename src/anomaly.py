"""Simple local anomaly detection for public sample dashboard insights."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.metrics import factory_contribution, monthly_summary


def _as_records(df: pd.DataFrame, limit: int = 10) -> list[dict[str, Any]]:
    """Convert a dataframe to JSON-friendly records."""
    converted = df.head(limit).copy()
    for column in converted.columns:
        if pd.api.types.is_datetime64_any_dtype(converted[column]):
            converted[column] = converted[column].astype(str)
    return converted.to_dict(orient="records")


def detect_fulfillment_rate_anomalies(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Flag monthly fulfillment rates above 1.05 or below 0.95."""
    summary = monthly_summary(df)
    if summary.empty or "fulfillment_rate" not in summary.columns:
        return []

    high = summary[summary["fulfillment_rate"] > 1.05].assign(
        anomaly_type="fulfillment_rate_above_1_05"
    )
    low = summary[summary["fulfillment_rate"] < 0.95].assign(
        anomaly_type="fulfillment_rate_below_0_95"
    )
    return _as_records(pd.concat([high, low], ignore_index=True))


def detect_labor_value_mom_anomalies(df: pd.DataFrame, threshold: float = 0.30) -> list[dict[str, Any]]:
    """Flag large month-over-month changes in delivery labor value."""
    summary = monthly_summary(df)
    if summary.empty or "monthly_delivery_labor_value" not in summary.columns:
        return []

    summary = summary.sort_values("year_month").copy()
    summary["labor_value_mom_change"] = summary["monthly_delivery_labor_value"].pct_change()
    flagged = summary[summary["labor_value_mom_change"].abs() > threshold].assign(
        anomaly_type="delivery_labor_value_large_mom_change"
    )
    return _as_records(flagged)


def detect_factory_share_anomalies(df: pd.DataFrame, threshold: float = 0.35) -> list[dict[str, Any]]:
    """Flag factories with unusually high contribution share."""
    contribution = factory_contribution(df)
    if contribution.empty or "share" not in contribution.columns:
        return []

    flagged = contribution[contribution["share"] > threshold].assign(
        anomaly_type="factory_contribution_share_high"
    )
    return _as_records(flagged)


def detect_anomalies(df: pd.DataFrame) -> dict[str, list[dict[str, Any]]]:
    """Run all local anomaly checks for the dashboard sample dataset."""
    return {
        "fulfillment_rate": detect_fulfillment_rate_anomalies(df),
        "delivery_labor_value_mom": detect_labor_value_mom_anomalies(df),
        "factory_contribution_share": detect_factory_share_anomalies(df),
    }

