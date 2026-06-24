"""Supply chain overview dashboard page."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.i18n import t
from src import metrics


def _format_number(value: float) -> str:
    """Format dashboard numbers with compact thousands separators."""
    return f"{value:,.0f}"


def render(df: pd.DataFrame, lang: str = "en") -> None:
    """Render the supply chain overview page."""
    st.title(t("overview_title", lang))

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(t("total_order_qty", lang), _format_number(metrics.total_order_qty(df)))
    col2.metric(t("total_delivery_qty", lang), _format_number(metrics.total_delivery_qty(df)))
    col3.metric(t("delivery_labor_value", lang), _format_number(metrics.delivery_labor_value(df)))
    col4.metric(t("fulfillment_rate", lang), f"{metrics.fulfillment_rate(df):.1%}")
    col5.metric(t("active_sku_count", lang), _format_number(metrics.active_sku_count(df)))

    summary = metrics.monthly_summary(df)
    if summary.empty:
        st.warning(t("monthly_column_warning", lang))
        return

    order_delivery = summary.melt(
        id_vars="year_month",
        value_vars=["monthly_order_qty", "monthly_delivery_qty"],
        var_name="Metric",
        value_name="Quantity",
    )
    order_delivery["Metric"] = order_delivery["Metric"].map(
        {
            "monthly_order_qty": t("order_quantity", lang),
            "monthly_delivery_qty": t("delivery_quantity", lang),
        }
    )

    st.plotly_chart(
        px.line(
            order_delivery,
            x="year_month",
            y="Quantity",
            color="Metric",
            markers=True,
            title=t("monthly_order_delivery_trend", lang),
            labels={"Quantity": t("quantity", lang), "Metric": t("metric", lang)},
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
                title=t("monthly_labor_value_trend", lang),
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
                title=t("monthly_fulfillment_trend", lang),
            ),
            width="stretch",
        )
