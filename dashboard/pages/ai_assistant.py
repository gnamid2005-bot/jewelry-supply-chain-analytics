"""Local rule-based AI insight assistant dashboard page."""

from __future__ import annotations

import json
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st

from src.ai_insight import (
    build_page_prompt_template,
    generate_general_ai_assistant_insight,
)
from src.metrics import factory_contribution, monthly_summary, product_category_contribution


ANALYSIS_TYPES = [
    "Executive Overview",
    "Supplier Performance",
    "Product Mix",
    "SKU Drill-down",
]

OUTPUT_STYLES = ["concise", "detailed", "action-oriented"]


def _json_safe_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Convert a dataframe to JSON-safe chart records."""
    converted = df.copy()
    for column in converted.columns:
        if pd.api.types.is_datetime64_any_dtype(converted[column]):
            converted[column] = converted[column].astype(str)
    return converted.to_dict(orient="records")


def _chart_data_for_analysis(
    df: pd.DataFrame,
    analysis_type: str,
    selected_sku: str | None,
) -> tuple[str, pd.DataFrame]:
    """Build a lightweight context chart for the selected analysis type."""
    if analysis_type == "Executive Overview":
        summary = monthly_summary(df).sort_values("year_month")
        return "Monthly Order vs Delivery Quantity", summary

    if analysis_type == "Supplier Performance":
        return "Factory Contribution Share", factory_contribution(df).head(15)

    if analysis_type == "Product Mix":
        return "Product Category Contribution", product_category_contribution(df).head(15)

    if not selected_sku or "sku_id" not in df.columns:
        return "SKU Drill-down", pd.DataFrame()

    sku_df = df[df["sku_id"].astype(str) == selected_sku]
    return f"SKU Drill-down: {selected_sku}", monthly_summary(sku_df).sort_values("year_month")


def _render_context_chart(title: str, analysis_type: str, chart_data: pd.DataFrame) -> None:
    """Render a context chart for the selected insight."""
    if chart_data.empty:
        st.info("Select an anonymized SKU to render the SKU context chart.")
        return

    if analysis_type == "Executive Overview":
        plot_df = chart_data.melt(
            id_vars="year_month",
            value_vars=["monthly_order_qty", "monthly_delivery_qty"],
            var_name="Metric",
            value_name="Quantity",
        )
        plot_df["Metric"] = plot_df["Metric"].map(
            {
                "monthly_order_qty": "Order Quantity",
                "monthly_delivery_qty": "Delivery Quantity",
            }
        )
        fig = px.line(plot_df, x="year_month", y="Quantity", color="Metric", markers=True, title=title)
    elif analysis_type == "Supplier Performance":
        fig = px.bar(chart_data, x="factory", y="share", title=title)
    elif analysis_type == "Product Mix":
        fig = px.bar(chart_data, x="product_category", y="monthly_delivery_labor_value", title=title)
    else:
        plot_df = chart_data.melt(
            id_vars="year_month",
            value_vars=["monthly_order_qty", "monthly_delivery_qty", "monthly_delivery_labor_value"],
            var_name="Metric",
            value_name="Value",
        )
        fig = px.line(plot_df, x="year_month", y="Value", color="Metric", markers=True, title=title)

    st.plotly_chart(fig, width="stretch")


def _render_insight_section(title: str, content: Any) -> None:
    """Render one standardized insight section."""
    st.markdown(f"**{title}**")
    if isinstance(content, dict):
        for key, value in content.items():
            st.write(f"- {key}: {value}")
    elif isinstance(content, list):
        if not content:
            st.write("- None flagged.")
        for item in content:
            st.write(f"- {item}")
    else:
        st.write(content)


def render(df: pd.DataFrame) -> None:
    """Render the local rule-based AI insight assistant page."""
    st.title("AI Insight Assistant")
    st.caption(
        "Local rule-based analytics assistant. It uses anonymized sample data only and does not call paid APIs, "
        "external LLMs, raw data, or processed private data."
    )

    controls = st.columns([1.2, 1.2, 1.0])
    analysis_type = controls[0].selectbox("Analysis type", ANALYSIS_TYPES)
    output_style = controls[1].selectbox("Output style", OUTPUT_STYLES)

    selected_sku: str | None = None
    if analysis_type == "SKU Drill-down" and "sku_id" in df.columns:
        sku_options = sorted(df["sku_id"].dropna().astype(str).unique())
        selected_sku = controls[2].selectbox("Optional selected SKU", sku_options)
    else:
        controls[2].caption("SKU selector appears for SKU Drill-down.")

    insight = generate_general_ai_assistant_insight(
        df=df,
        analysis_type=analysis_type,
        selected_sku=selected_sku,
        output_style=output_style,
    )
    chart_title, chart_data = _chart_data_for_analysis(df, analysis_type, selected_sku)

    _render_context_chart(chart_title, analysis_type, chart_data)

    st.subheader(insight["title"])
    _render_insight_section("Executive summary", insight["executive_summary"])
    _render_insight_section("Key metrics", insight["key_metrics"])
    _render_insight_section("Trend interpretation", insight["trend_interpretation"])
    _render_insight_section("Top contributors", insight["top_contributors"])
    _render_insight_section("Potential anomalies", insight["potential_anomalies"])
    _render_insight_section("Suggested business actions", insight["suggested_business_actions"])
    _render_insight_section("Data privacy note", insight["data_privacy_note"])

    with st.expander("Aggregated chart data JSON"):
        st.code(json.dumps(_json_safe_records(chart_data), ensure_ascii=False, indent=2), language="json")

    with st.expander("Future optional LLM prompt template"):
        st.code(
            build_page_prompt_template(
                analysis_type=analysis_type,
                output_style=output_style,
                selected_sku=selected_sku,
                insight=insight,
            ),
            language="text",
        )
