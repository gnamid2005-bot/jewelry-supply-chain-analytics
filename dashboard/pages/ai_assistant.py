"""Local rule-based AI insight assistant dashboard page."""

from __future__ import annotations

import json
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.i18n import option_label, t, translate_insight_value
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
    lang: str,
) -> tuple[str, pd.DataFrame]:
    """Build a lightweight context chart for the selected analysis type."""
    if analysis_type == "Executive Overview":
        summary = monthly_summary(df).sort_values("year_month")
        return t("monthly_order_delivery_trend", lang), summary

    if analysis_type == "Supplier Performance":
        return t("factory_contribution_share", lang), factory_contribution(df).head(15)

    if analysis_type == "Product Mix":
        return t("product_category_contribution", lang), product_category_contribution(df).head(15)

    if not selected_sku or "sku_id" not in df.columns:
        return t("sku_drilldown_title", lang), pd.DataFrame()

    sku_df = df[df["sku_id"].astype(str) == selected_sku]
    return f"{t('sku_drilldown_title', lang)}: {selected_sku}", monthly_summary(sku_df).sort_values("year_month")


def _render_context_chart(title: str, analysis_type: str, chart_data: pd.DataFrame, lang: str) -> None:
    """Render a context chart for the selected insight."""
    if chart_data.empty:
        st.info(t("select_sku_context", lang))
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
                "monthly_order_qty": t("order_quantity", lang),
                "monthly_delivery_qty": t("delivery_quantity", lang),
            }
        )
        fig = px.line(
            plot_df,
            x="year_month",
            y="Quantity",
            color="Metric",
            markers=True,
            title=title,
            labels={"Quantity": t("quantity", lang), "Metric": t("metric", lang)},
        )
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
        plot_df["Metric"] = plot_df["Metric"].map(
            {
                "monthly_order_qty": t("order_quantity", lang),
                "monthly_delivery_qty": t("delivery_quantity", lang),
                "monthly_delivery_labor_value": t("delivery_labor_value", lang),
            }
        )
        fig = px.line(
            plot_df,
            x="year_month",
            y="Value",
            color="Metric",
            markers=True,
            title=title,
            labels={"Value": t("value", lang), "Metric": t("metric", lang)},
        )

    st.plotly_chart(fig, width="stretch")


def _render_insight_section(title: str, content: Any, lang: str) -> None:
    """Render one standardized insight section."""
    st.markdown(f"**{title}**")
    content = translate_insight_value(content, lang)
    if isinstance(content, dict):
        for key, value in content.items():
            st.write(f"- {key}: {value}")
    elif isinstance(content, list):
        if not content:
            st.write(f"- {t('none_flagged', lang)}")
        for item in content:
            st.write(f"- {item}")
    else:
        st.write(content)


def render(df: pd.DataFrame, lang: str = "en") -> None:
    """Render the local rule-based AI insight assistant page."""
    st.title(t("ai_title", lang))
    st.caption(t("ai_caption", lang))

    controls = st.columns([1.2, 1.2, 1.0])
    analysis_type = controls[0].selectbox(
        t("analysis_type", lang),
        ANALYSIS_TYPES,
        format_func=lambda value: option_label(value, lang),
    )
    output_style = controls[1].selectbox(
        t("output_style", lang),
        OUTPUT_STYLES,
        format_func=lambda value: option_label(value, lang),
    )

    selected_sku: str | None = None
    if analysis_type == "SKU Drill-down" and "sku_id" in df.columns:
        sku_options = sorted(df["sku_id"].dropna().astype(str).unique())
        selected_sku = controls[2].selectbox(t("optional_selected_sku", lang), sku_options)
    else:
        controls[2].caption(t("sku_selector_caption", lang))

    insight = generate_general_ai_assistant_insight(
        df=df,
        analysis_type=analysis_type,
        selected_sku=selected_sku,
        output_style=output_style,
    )
    chart_title, chart_data = _chart_data_for_analysis(df, analysis_type, selected_sku, lang)

    _render_context_chart(chart_title, analysis_type, chart_data, lang)

    st.subheader(translate_insight_value(insight["title"], lang))
    _render_insight_section(t("executive_summary", lang), insight["executive_summary"], lang)
    _render_insight_section(t("key_metrics", lang), insight["key_metrics"], lang)
    _render_insight_section(t("trend_interpretation", lang), insight["trend_interpretation"], lang)
    _render_insight_section(t("top_contributors", lang), insight["top_contributors"], lang)
    _render_insight_section(t("potential_anomalies", lang), insight["potential_anomalies"], lang)
    _render_insight_section(t("suggested_business_actions", lang), insight["suggested_business_actions"], lang)
    _render_insight_section(t("data_privacy_note", lang), insight["data_privacy_note"], lang)

    with st.expander(t("aggregated_chart_json", lang)):
        st.code(json.dumps(_json_safe_records(chart_data), ensure_ascii=False, indent=2), language="json")

    with st.expander(t("future_prompt", lang)):
        st.code(
            build_page_prompt_template(
                analysis_type=analysis_type,
                output_style=output_style,
                selected_sku=selected_sku,
                insight=insight,
            ),
            language="text",
        )
