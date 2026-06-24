"""Supplier performance dashboard page."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.i18n import t
from src import metrics


def _safe_group_sum(df: pd.DataFrame, group_column: str, metric_column: str) -> pd.DataFrame:
    """Aggregate one metric by one dimension when both columns exist."""
    if group_column not in df.columns or metric_column not in df.columns:
        return pd.DataFrame(columns=[group_column, metric_column])
    return (
        df.groupby(group_column, dropna=False)[metric_column]
        .sum()
        .reset_index()
        .sort_values(metric_column, ascending=False)
    )


def render(df: pd.DataFrame, lang: str = "en") -> None:
    """Render the supplier performance page."""
    st.title(t("suppliers_title", lang))

    top5_share = metrics.supplier_top5_share(df)
    hhi = metrics.supplier_hhi(df)
    kpi1, kpi2 = st.columns(2)
    kpi1.metric(t("supplier_top5_share", lang), f"{top5_share:.1%}")
    kpi2.metric(t("supplier_hhi", lang), f"{hhi:.3f}")

    left, right = st.columns(2)
    with left:
        factory_type = _safe_group_sum(df, "factory_type", "monthly_delivery_labor_value")
        st.plotly_chart(
            px.bar(
                factory_type,
                x="factory_type",
                y="monthly_delivery_labor_value",
                title=t("factory_type_comparison", lang),
            ),
            width="stretch",
        )

    with right:
        factory_top10 = metrics.factory_contribution(df).head(10)
        st.plotly_chart(
            px.bar(
                factory_top10,
                x="factory",
                y="monthly_delivery_labor_value",
                title=t("top10_factories", lang),
            ),
            width="stretch",
        )

    contribution = metrics.factory_contribution(df)
    st.plotly_chart(
        px.treemap(
            contribution,
            path=["factory"],
            values="monthly_delivery_labor_value",
            title=t("factory_contribution_share", lang),
        ),
        width="stretch",
    )

    supplier_table = contribution.copy()
    if "monthly_order_qty" in df.columns and "monthly_delivery_qty" in df.columns:
        supplier_volume = (
            df.groupby("factory", dropna=False)
            .agg(
                monthly_order_qty=("monthly_order_qty", "sum"),
                monthly_delivery_qty=("monthly_delivery_qty", "sum"),
            )
            .reset_index()
        )
        supplier_table = supplier_table.merge(supplier_volume, on="factory", how="left")
        supplier_table["fulfillment_rate"] = (
            supplier_table["monthly_delivery_qty"] / supplier_table["monthly_order_qty"]
        ).fillna(0)

    st.subheader(t("sortable_supplier_table", lang))
    st.dataframe(supplier_table, width="stretch")
