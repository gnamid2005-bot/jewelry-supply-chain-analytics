"""SKU drilldown dashboard page."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def _sku_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return monthly metrics for one selected SKU."""
    if "year_month" not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby("year_month", dropna=False)
        .agg(
            monthly_order_qty=("monthly_order_qty", "sum"),
            monthly_delivery_qty=("monthly_delivery_qty", "sum"),
            monthly_delivery_labor_value=("monthly_delivery_labor_value", "sum"),
        )
        .reset_index()
    )


def render(df: pd.DataFrame) -> None:
    """Render the SKU drilldown page."""
    st.title("SKU Drilldown")

    if "sku_id" not in df.columns:
        st.warning("SKU drilldown requires a `sku_id` column.")
        return

    sku_options = sorted(df["sku_id"].dropna().astype(str).unique())
    selected_sku = st.selectbox("Select or search SKU", sku_options)
    sku_df = df[df["sku_id"].astype(str) == selected_sku]

    st.subheader(selected_sku)
    detail_columns = ["factory", "factory_type", "product_category", "product_series", "sku_source"]
    details = {
        column: ", ".join(sorted(sku_df[column].dropna().astype(str).unique()))
        for column in detail_columns
        if column in sku_df.columns
    }
    st.dataframe(pd.DataFrame([details]), width="stretch")

    monthly = _sku_monthly_summary(sku_df)
    if monthly.empty:
        st.warning("SKU trend requires a `year_month` column.")
        return

    trend = monthly.melt(
        id_vars="year_month",
        value_vars=["monthly_order_qty", "monthly_delivery_qty", "monthly_delivery_labor_value"],
        var_name="Metric",
        value_name="Value",
    )
    trend["Metric"] = trend["Metric"].map(
        {
            "monthly_order_qty": "Order Quantity",
            "monthly_delivery_qty": "Delivery Quantity",
            "monthly_delivery_labor_value": "Delivery Labor Value",
        }
    )

    st.plotly_chart(
        px.line(
            trend,
            x="year_month",
            y="Value",
            color="Metric",
            markers=True,
            title="Monthly Order, Delivery, and Labor Value Trend",
        ),
        width="stretch",
    )
