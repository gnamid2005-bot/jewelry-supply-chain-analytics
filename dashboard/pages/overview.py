"""Supply chain overview dashboard page."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src import metrics


def _format_number(value: float) -> str:
    """Format dashboard numbers with compact thousands separators."""
    return f"{value:,.0f}"


def render(df: pd.DataFrame) -> None:
    """Render the supply chain overview page."""
    st.title("Supply Chain Overview")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Order Quantity", _format_number(metrics.total_order_qty(df)))
    col2.metric("Total Delivery Quantity", _format_number(metrics.total_delivery_qty(df)))
    col3.metric("Delivery Labor Value", _format_number(metrics.delivery_labor_value(df)))
    col4.metric("Fulfillment Rate", f"{metrics.fulfillment_rate(df):.1%}")
    col5.metric("Active SKU Count", _format_number(metrics.active_sku_count(df)))

    summary = metrics.monthly_summary(df)
    if summary.empty:
        st.warning("Monthly charts require a `year_month` column.")
        return

    order_delivery = summary.melt(
        id_vars="year_month",
        value_vars=["monthly_order_qty", "monthly_delivery_qty"],
        var_name="Metric",
        value_name="Quantity",
    )
    order_delivery["Metric"] = order_delivery["Metric"].map(
        {
            "monthly_order_qty": "Order Quantity",
            "monthly_delivery_qty": "Delivery Quantity",
        }
    )

    st.plotly_chart(
        px.line(
            order_delivery,
            x="year_month",
            y="Quantity",
            color="Metric",
            markers=True,
            title="Monthly Order vs Delivery Quantity Trend",
        ),
        width="stretch",
    )

    left, right = st.columns(2)
    with left:
        st.plotly_chart(
            px.line(
                summary,
                x="year_month",
                y="monthly_delivery_labor_value",
                markers=True,
                title="Monthly Delivery Labor Value Trend",
            ),
            width="stretch",
        )

    with right:
        st.plotly_chart(
            px.line(
                summary,
                x="year_month",
                y="fulfillment_rate",
                markers=True,
                title="Monthly Fulfillment Rate Trend",
            ),
            width="stretch",
        )
