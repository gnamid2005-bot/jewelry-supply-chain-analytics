"""Reusable KPI calculations for jewelry supply chain analytics."""

from __future__ import annotations

import pandas as pd


def _sum(df: pd.DataFrame, column: str) -> float:
    """Return a numeric sum with missing values ignored."""
    if column not in df.columns:
        return 0.0
    return float(_numeric_series(df, column).sum())


def _numeric_series(df: pd.DataFrame, column: str) -> pd.Series:
    """Return one column as numeric values, defaulting missing columns to zero."""
    if column not in df.columns:
        return pd.Series(0, index=df.index, dtype="float64")
    return pd.to_numeric(df[column], errors="coerce").fillna(0)


def _safe_divide(numerator: float, denominator: float) -> float:
    """Divide two numbers and return 0.0 when the denominator is empty."""
    if denominator == 0:
        return 0.0
    return float(numerator / denominator)


def total_order_qty(df: pd.DataFrame) -> float:
    """Return total monthly order quantity."""
    return _sum(df, "monthly_order_qty")


def total_delivery_qty(df: pd.DataFrame) -> float:
    """Return total monthly delivery quantity."""
    return _sum(df, "monthly_delivery_qty")


def delivery_labor_value(df: pd.DataFrame) -> float:
    """Return total monthly delivery labor value."""
    return _sum(df, "monthly_delivery_labor_value")


def fulfillment_rate(df: pd.DataFrame) -> float:
    """Return delivery quantity divided by order quantity."""
    return _safe_divide(total_delivery_qty(df), total_order_qty(df))


def delivery_gap(df: pd.DataFrame) -> float:
    """Return order quantity minus delivery quantity."""
    return total_order_qty(df) - total_delivery_qty(df)


def active_sku_count(df: pd.DataFrame) -> int:
    """Return count of SKUs with order or delivery activity."""
    if "sku_id" not in df.columns:
        return 0

    order_qty = _numeric_series(df, "monthly_order_qty")
    delivery_qty = _numeric_series(df, "monthly_delivery_qty")
    active = df.loc[(order_qty > 0) | (delivery_qty > 0), "sku_id"]
    return int(active.nunique(dropna=True))


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return KPI summary grouped by reporting month."""
    if "year_month" not in df.columns:
        return pd.DataFrame()

    grouped = (
        df.groupby("year_month", dropna=False)
        .agg(
            monthly_order_qty=("monthly_order_qty", "sum"),
            monthly_delivery_qty=("monthly_delivery_qty", "sum"),
            monthly_delivery_labor_value=("monthly_delivery_labor_value", "sum"),
            active_sku_count=("sku_id", "nunique"),
        )
        .reset_index()
    )
    grouped["fulfillment_rate"] = grouped["monthly_delivery_qty"] / grouped["monthly_order_qty"]
    grouped["fulfillment_rate"] = grouped["fulfillment_rate"].fillna(0)
    grouped["delivery_gap"] = grouped["monthly_order_qty"] - grouped["monthly_delivery_qty"]
    grouped["avg_labor_value_per_unit"] = grouped["monthly_delivery_labor_value"] / grouped[
        "monthly_delivery_qty"
    ]
    grouped["avg_labor_value_per_unit"] = grouped["avg_labor_value_per_unit"].fillna(0)
    return grouped


def _contribution(df: pd.DataFrame, group_column: str, metric_column: str) -> pd.DataFrame:
    """Return metric contribution by one dimension."""
    if group_column not in df.columns or metric_column not in df.columns:
        return pd.DataFrame(columns=[group_column, metric_column, "share"])

    grouped = (
        df.groupby(group_column, dropna=False)[metric_column]
        .sum()
        .reset_index()
        .sort_values(metric_column, ascending=False)
    )
    total = float(grouped[metric_column].sum())
    grouped["share"] = grouped[metric_column].apply(lambda value: _safe_divide(float(value), total))
    return grouped


def factory_contribution(
    df: pd.DataFrame,
    metric_column: str = "monthly_delivery_labor_value",
) -> pd.DataFrame:
    """Return factory contribution by the selected metric."""
    return _contribution(df, "factory", metric_column)


def product_category_contribution(
    df: pd.DataFrame,
    metric_column: str = "monthly_delivery_labor_value",
) -> pd.DataFrame:
    """Return product category contribution by the selected metric."""
    return _contribution(df, "product_category", metric_column)


def product_series_contribution(
    df: pd.DataFrame,
    metric_column: str = "monthly_delivery_labor_value",
) -> pd.DataFrame:
    """Return product series contribution by the selected metric."""
    return _contribution(df, "product_series", metric_column)


def avg_labor_value_per_unit(df: pd.DataFrame) -> float:
    """Return average delivery labor value per delivered unit."""
    return _safe_divide(delivery_labor_value(df), total_delivery_qty(df))


def supplier_top5_share(
    df: pd.DataFrame,
    metric_column: str = "monthly_delivery_labor_value",
) -> float:
    """Return the share contributed by the top five factories."""
    contribution = factory_contribution(df, metric_column=metric_column)
    if contribution.empty:
        return 0.0
    return float(contribution.head(5)["share"].sum())


def supplier_hhi(
    df: pd.DataFrame,
    metric_column: str = "monthly_delivery_labor_value",
) -> float:
    """Return Herfindahl-Hirschman Index for supplier concentration."""
    contribution = factory_contribution(df, metric_column=metric_column)
    if contribution.empty:
        return 0.0
    return float((contribution["share"] ** 2).sum())
