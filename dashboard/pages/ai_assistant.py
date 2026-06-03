"""Local rule-based AI insight assistant dashboard page."""

from __future__ import annotations

import json

import pandas as pd
import plotly.express as px
import streamlit as st

from src.ai_insight import build_prompt_template, generate_mock_insight
from src.anomaly import detect_anomalies
from src.metrics import factory_contribution, monthly_summary, product_series_contribution


CHART_OPTIONS = {
    "Monthly Fulfillment Rate": "monthly_fulfillment_rate",
    "Monthly Delivery Labor Value": "monthly_delivery_labor_value",
    "Factory Contribution Share": "factory_contribution_share",
    "Product Series Contribution": "product_series_contribution",
}


def _build_chart_data(df: pd.DataFrame, chart_key: str) -> tuple[str, pd.DataFrame, dict[str, str]]:
    """Create aggregated chart data for the selected insight view."""
    if chart_key == "monthly_fulfillment_rate":
        title = "Monthly Fulfillment Rate"
        data = monthly_summary(df)[["year_month", "fulfillment_rate", "delivery_gap"]]
        definitions = {
            "fulfillment_rate": "Delivery quantity divided by order quantity.",
            "delivery_gap": "Order quantity minus delivery quantity.",
        }
    elif chart_key == "monthly_delivery_labor_value":
        title = "Monthly Delivery Labor Value"
        data = monthly_summary(df)[["year_month", "monthly_delivery_labor_value"]]
        definitions = {
            "monthly_delivery_labor_value": "Total delivered labor value by month.",
        }
    elif chart_key == "factory_contribution_share":
        title = "Factory Contribution Share"
        data = factory_contribution(df)[["factory", "monthly_delivery_labor_value", "share"]]
        definitions = {
            "share": "Factory delivery labor value divided by total delivery labor value.",
        }
    else:
        title = "Product Series Contribution"
        data = product_series_contribution(df)[["product_series", "monthly_delivery_labor_value", "share"]]
        definitions = {
            "share": "Product series delivery labor value divided by total delivery labor value.",
        }
    return title, data, definitions


def _render_chart(title: str, chart_key: str, chart_data: pd.DataFrame) -> None:
    """Render the selected chart for context."""
    if chart_data.empty:
        st.warning("Not enough data to build this insight view.")
        return

    if chart_key == "monthly_fulfillment_rate":
        fig = px.line(chart_data, x="year_month", y="fulfillment_rate", markers=True, title=title)
    elif chart_key == "monthly_delivery_labor_value":
        fig = px.line(chart_data, x="year_month", y="monthly_delivery_labor_value", markers=True, title=title)
    elif chart_key == "factory_contribution_share":
        fig = px.bar(chart_data.head(15), x="factory", y="share", title=title)
    else:
        fig = px.bar(chart_data.head(15), x="product_series", y="share", title=title)

    st.plotly_chart(fig, width="stretch")


def render(df: pd.DataFrame) -> None:
    """Render the local rule-based AI insight assistant page."""
    st.title("AI Insight Assistant")
    st.caption("Mock/local rule-based version. No OpenAI API, paid API, raw data, or processed private data is used.")

    chart_label = st.selectbox("Choose chart type", list(CHART_OPTIONS.keys()))
    chart_key = CHART_OPTIONS[chart_label]
    title, chart_data, metric_definitions = _build_chart_data(df, chart_key)
    anomalies = detect_anomalies(df)

    _render_chart(title, chart_key, chart_data)

    chart_json = chart_data.copy()
    if "year_month" in chart_json.columns:
        chart_json["year_month"] = chart_json["year_month"].astype(str)
    chart_records = chart_json.to_dict(orient="records")

    filters = {"chart_type": chart_label, "data_source": "data/sample/anonymized_supply_chain_sample.csv"}
    insight = generate_mock_insight(
        chart_title=title,
        metric_definitions=metric_definitions,
        filters=filters,
        aggregated_data=chart_records,
        anomaly_flags=anomalies,
    )

    st.subheader("Mock AI Insight")
    st.markdown(f"**Main trend:** {insight['main_trend']}")
    st.markdown("**Anomalies:**")
    for item in insight["anomalies"]:
        st.write(f"- {item}")
    st.markdown(f"**Possible business meaning:** {insight['possible_business_meaning']}")
    st.markdown("**Recommended follow-up dimensions:**")
    for item in insight["recommended_follow_up_dimensions"]:
        st.write(f"- {item}")
    st.markdown(f"**Executive summary:** {insight['executive_summary']}")

    with st.expander("Aggregated chart_data JSON"):
        st.code(json.dumps(chart_records, ensure_ascii=False, indent=2, default=str), language="json")

    with st.expander("Future LLM prompt template"):
        st.code(
            build_prompt_template(
                chart_title=title,
                metric_definitions=metric_definitions,
                filters=filters,
                aggregated_data=chart_records,
                anomaly_flags=anomalies,
            ),
            language="text",
        )
