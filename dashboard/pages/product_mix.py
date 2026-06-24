"""Product mix dashboard page."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.i18n import t
from src import metrics


def _avg_labor_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate average labor value per delivered unit by product category."""
    required = {"product_category", "monthly_delivery_labor_value", "monthly_delivery_qty"}
    if not required.issubset(df.columns):
        return pd.DataFrame(columns=["product_category", "avg_labor_value_per_unit"])

    grouped = (
        df.groupby("product_category", dropna=False)
        .agg(
            monthly_delivery_labor_value=("monthly_delivery_labor_value", "sum"),
            monthly_delivery_qty=("monthly_delivery_qty", "sum"),
        )
        .reset_index()
    )
    grouped["avg_labor_value_per_unit"] = (
        grouped["monthly_delivery_labor_value"] / grouped["monthly_delivery_qty"]
    ).fillna(0)
    return grouped.sort_values("avg_labor_value_per_unit", ascending=False)


def render(df: pd.DataFrame, lang: str = "en") -> None:
    """Render the product mix page."""
    st.title(t("product_mix_title", lang))

    left, right = st.columns(2)
    with left:
        category = metrics.product_category_contribution(df)
        st.plotly_chart(
            px.bar(
                category,
                x="product_category",
                y="monthly_delivery_labor_value",
                title=t("product_category_contribution", lang),
            ),
            width="stretch",
        )

    with right:
        series = metrics.product_series_contribution(df)
        st.plotly_chart(
            px.treemap(
                series,
                path=["product_series"],
                values="monthly_delivery_labor_value",
                title=t("product_series_contribution", lang),
            ),
            width="stretch",
        )

    left, right = st.columns(2)
    with left:
        if "sku_source" in df.columns:
            sku_source = df.groupby("sku_source", dropna=False).size().reset_index(name="sku_count")
            st.plotly_chart(
                px.pie(
                    sku_source,
                    names="sku_source",
                    values="sku_count",
                    title=t("sku_source_distribution", lang),
                ),
                width="stretch",
            )

    with right:
        avg_labor = _avg_labor_by_category(df)
        st.plotly_chart(
            px.bar(
                avg_labor,
                x="product_category",
                y="avg_labor_value_per_unit",
                title=t("avg_labor_by_category", lang),
            ),
            width="stretch",
        )
