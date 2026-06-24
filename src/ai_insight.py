"""Local rule-based insight generator for supply chain dashboard storytelling.

This module does not call external APIs or language models. It turns aggregated
anonymized sample data into deterministic, business-style insight sections.
"""

from __future__ import annotations

import json
from typing import Any, Literal

import pandas as pd

from src import metrics
from src.anomaly import detect_anomalies


OutputStyle = Literal["concise", "detailed", "action-oriented"]
Insight = dict[str, Any]

PRIVACY_NOTE = (
    "Insights are generated locally from anonymized sample data only. No raw company data, "
    "real supplier names, real SKU identifiers, product images, raw descriptions, mapping tables, "
    "or paid APIs are used."
)


def _fmt_number(value: float) -> str:
    """Format a numeric metric for display."""
    return f"{value:,.0f}"


def _fmt_pct(value: float) -> str:
    """Format a ratio as a percentage."""
    return f"{value:.1%}"


def _safe_divide(numerator: float, denominator: float) -> float:
    """Divide two numbers with zero-denominator protection."""
    if denominator == 0:
        return 0.0
    return float(numerator / denominator)


def _month_label(value: object) -> str:
    """Return a readable month label."""
    if pd.isna(value):
        return "Unknown month"
    timestamp = pd.to_datetime(value, errors="coerce")
    if pd.isna(timestamp):
        return str(value)
    return timestamp.strftime("%Y-%m")


def _series_trend(values: pd.Series) -> str:
    """Classify a numeric time series as improving, declining, volatile, or stable."""
    clean = pd.to_numeric(values, errors="coerce").dropna()
    if len(clean) < 2:
        return "stable"

    pct_changes = clean.pct_change().replace([float("inf"), -float("inf")], pd.NA).dropna()
    if not pct_changes.empty and pct_changes.abs().mean() >= 0.25:
        return "volatile"

    first = float(clean.iloc[0])
    last = float(clean.iloc[-1])
    baseline = abs(first) if first else 1.0
    change = (last - first) / baseline
    if change >= 0.10:
        return "improving"
    if change <= -0.10:
        return "declining"
    return "stable"


def _limit(items: list[str], style: OutputStyle) -> list[str]:
    """Limit insight bullet count based on requested output style."""
    if style == "concise":
        return items[:3]
    if style == "action-oriented":
        return items[:5]
    return items


def _top_records(
    df: pd.DataFrame,
    group_column: str,
    metric_column: str,
    limit: int = 5,
) -> pd.DataFrame:
    """Return top grouped records by one metric."""
    if group_column not in df.columns or metric_column not in df.columns:
        return pd.DataFrame(columns=[group_column, metric_column])
    return (
        df.groupby(group_column, dropna=False)[metric_column]
        .sum()
        .reset_index()
        .sort_values(metric_column, ascending=False)
        .head(limit)
    )


def _base_insight(
    title: str,
    executive_summary: str,
    key_metrics: dict[str, str],
    trend_interpretation: list[str],
    top_contributors: list[str],
    potential_anomalies: list[str],
    suggested_business_actions: list[str],
    output_style: OutputStyle,
    supporting_data: dict[str, Any] | None = None,
) -> Insight:
    """Build the common insight response shape."""
    return {
        "title": title,
        "executive_summary": executive_summary,
        "key_metrics": key_metrics,
        "trend_interpretation": _limit(trend_interpretation, output_style),
        "top_contributors": _limit(top_contributors, output_style),
        "potential_anomalies": _limit(potential_anomalies, output_style),
        "suggested_business_actions": _limit(suggested_business_actions, output_style),
        "data_privacy_note": PRIVACY_NOTE,
        "supporting_data": supporting_data or {},
    }


def generate_overview_insight(df: pd.DataFrame, output_style: OutputStyle = "concise") -> Insight:
    """Generate overview-level supply chain insights."""
    total_order = metrics.total_order_qty(df)
    total_delivery = metrics.total_delivery_qty(df)
    fulfillment = metrics.fulfillment_rate(df)
    gap = metrics.delivery_gap(df)
    active_skus = metrics.active_sku_count(df)
    monthly = metrics.monthly_summary(df).sort_values("year_month")

    best_month = worst_month = None
    delivery_trend = "stable"
    if not monthly.empty:
        best_month = monthly.loc[monthly["fulfillment_rate"].idxmax()]
        worst_month = monthly.loc[monthly["fulfillment_rate"].idxmin()]
        delivery_trend = _series_trend(monthly["monthly_delivery_qty"])

    trend_lines = [
        f"Delivery trend appears {delivery_trend} based on monthly delivery quantity movement.",
        f"Total delivery covers {_fmt_pct(fulfillment)} of total order quantity.",
    ]
    if best_month is not None:
        trend_lines.append(
            f"Best fulfillment month is {_month_label(best_month['year_month'])} at "
            f"{_fmt_pct(float(best_month['fulfillment_rate']))}."
        )
    if worst_month is not None:
        trend_lines.append(
            f"Weakest fulfillment month is {_month_label(worst_month['year_month'])} at "
            f"{_fmt_pct(float(worst_month['fulfillment_rate']))}."
        )

    anomalies = []
    if fulfillment < 0.95:
        anomalies.append("Overall fulfillment rate is below the 95% rule-based threshold.")
    if fulfillment > 1.05:
        anomalies.append("Overall fulfillment rate is above 105%, suggesting backlog delivery or timing effects.")
    if gap > 0:
        anomalies.append(f"Delivery gap is positive at {_fmt_number(gap)}, meaning orders exceed deliveries.")
    if delivery_trend == "volatile":
        anomalies.append("Monthly delivery quantity is volatile and should be reviewed by supplier and product mix.")
    if not anomalies:
        anomalies.append("No major overview-level anomaly is flagged by the current local rules.")

    actions = [
        "Review months with the weakest fulfillment rate before drilling into suppliers.",
        "Compare supplier contribution and product mix for months with large delivery gaps.",
        "Use SKU drill-down for high-volume SKUs when delivery trend becomes volatile.",
        "Track whether delivery labor value changes are volume-driven or mix-driven.",
    ]

    return _base_insight(
        title="Executive Overview Insight",
        executive_summary=(
            f"The sample dataset shows {_fmt_number(total_order)} ordered units and "
            f"{_fmt_number(total_delivery)} delivered units, with a fulfillment rate of {_fmt_pct(fulfillment)}."
        ),
        key_metrics={
            "Total Order Quantity": _fmt_number(total_order),
            "Total Delivery Quantity": _fmt_number(total_delivery),
            "Fulfillment Rate": _fmt_pct(fulfillment),
            "Delivery Gap": _fmt_number(gap),
            "Active SKU Count": _fmt_number(active_skus),
        },
        trend_interpretation=trend_lines,
        top_contributors=[
            "Use Supplier Performance to identify factories driving delivery value.",
            "Use Product Mix to identify categories and series driving value.",
        ],
        potential_anomalies=anomalies,
        suggested_business_actions=actions,
        output_style=output_style,
        supporting_data={"monthly_summary": monthly.head(50).to_dict(orient="records")},
    )


def generate_supplier_insight(df: pd.DataFrame, output_style: OutputStyle = "concise") -> Insight:
    """Generate supplier performance insights."""
    supplier = (
        df.groupby("factory", dropna=False)
        .agg(
            monthly_order_qty=("monthly_order_qty", "sum"),
            monthly_delivery_qty=("monthly_delivery_qty", "sum"),
            monthly_delivery_labor_value=("monthly_delivery_labor_value", "sum"),
        )
        .reset_index()
    )
    supplier["delivery_gap"] = supplier["monthly_order_qty"] - supplier["monthly_delivery_qty"]
    supplier["fulfillment_rate"] = supplier.apply(
        lambda row: _safe_divide(row["monthly_delivery_qty"], row["monthly_order_qty"]),
        axis=1,
    )
    supplier = supplier.sort_values("monthly_delivery_labor_value", ascending=False)

    top_by_delivery = supplier.sort_values("monthly_delivery_qty", ascending=False).head(5)
    high_gap = supplier.sort_values("delivery_gap", ascending=False).head(5)
    top5_share = metrics.supplier_top5_share(df)
    hhi = metrics.supplier_hhi(df)
    concentration_message = (
        "Supplier dependency appears concentrated."
        if top5_share >= 0.70 or hhi >= 0.25
        else "Supplier dependency appears diversified under the current thresholds."
    )

    top_contributors = [
        f"{row.factory}: {_fmt_number(row.monthly_delivery_qty)} delivered units"
        for row in top_by_delivery.itertuples(index=False)
    ]
    gap_lines = [
        f"{row.factory}: delivery gap {_fmt_number(row.delivery_gap)}"
        for row in high_gap.itertuples(index=False)
        if row.delivery_gap > 0
    ]
    anomalies = gap_lines or ["No supplier has a positive delivery gap in the top gap scan."]
    if top5_share >= 0.70:
        anomalies.append(f"Top five suppliers contribute {_fmt_pct(top5_share)}, indicating concentration risk.")
    if hhi >= 0.25:
        anomalies.append(f"Supplier HHI is {hhi:.3f}, above the concentration watch threshold.")

    actions = [
        "Review high-gap suppliers by month to separate timing effects from capacity issues.",
        "Compare in-house and external supplier types for concentration exposure.",
        "Create a follow-up view for suppliers with high labor value and low fulfillment.",
        "Consider backup capacity planning if top suppliers dominate delivery value.",
    ]

    return _base_insight(
        title="Supplier Performance Insight",
        executive_summary=(
            f"{concentration_message} Top five supplier share is {_fmt_pct(top5_share)} and HHI is {hhi:.3f}."
        ),
        key_metrics={
            "Supplier Top 5 Share": _fmt_pct(top5_share),
            "Supplier HHI": f"{hhi:.3f}",
            "Supplier Count": _fmt_number(float(supplier["factory"].nunique())),
        },
        trend_interpretation=[
            "Supplier contribution is evaluated by delivery quantity and delivery labor value.",
            concentration_message,
        ],
        top_contributors=top_contributors,
        potential_anomalies=anomalies,
        suggested_business_actions=actions,
        output_style=output_style,
        supporting_data={"supplier_summary": supplier.head(50).to_dict(orient="records")},
    )


def generate_product_mix_insight(df: pd.DataFrame, output_style: OutputStyle = "concise") -> Insight:
    """Generate product mix insights."""
    category = metrics.product_category_contribution(df).rename(
        columns={"monthly_delivery_labor_value": "delivery_labor_value"}
    )
    series = metrics.product_series_contribution(df).rename(
        columns={"monthly_delivery_labor_value": "delivery_labor_value"}
    )
    source = _top_records(df, "sku_source", "monthly_delivery_labor_value", limit=10).rename(
        columns={"monthly_delivery_labor_value": "delivery_labor_value"}
    )

    category_perf = (
        df.groupby("product_category", dropna=False)
        .agg(
            monthly_order_qty=("monthly_order_qty", "sum"),
            monthly_delivery_qty=("monthly_delivery_qty", "sum"),
            monthly_delivery_labor_value=("monthly_delivery_labor_value", "sum"),
        )
        .reset_index()
    )
    category_perf["fulfillment_rate"] = category_perf.apply(
        lambda row: _safe_divide(row["monthly_delivery_qty"], row["monthly_order_qty"]),
        axis=1,
    )
    category_perf = category_perf.sort_values("monthly_delivery_labor_value", ascending=False)

    dominant_category = category.iloc[0] if not category.empty else None
    dominant_series = series.iloc[0] if not series.empty else None
    dominant_source = source.iloc[0] if not source.empty else None

    concentration = float(category["share"].head(3).sum()) if not category.empty else 0.0
    anomalies = []
    if concentration >= 0.75:
        anomalies.append(f"Top three product categories contribute {_fmt_pct(concentration)} of delivery value.")
    low_fulfillment = category_perf[category_perf["fulfillment_rate"] < 0.95].head(3)
    for row in low_fulfillment.itertuples(index=False):
        anomalies.append(
            f"{row.product_category} fulfillment is {_fmt_pct(float(row.fulfillment_rate))}, below 95%."
        )
    if not anomalies:
        anomalies.append("No major product-mix anomaly is flagged by the current local rules.")

    top_contributors = []
    if dominant_category is not None:
        top_contributors.append(
            f"Dominant category: {dominant_category.product_category} at {_fmt_pct(float(dominant_category.share))}."
        )
    if dominant_series is not None:
        top_contributors.append(
            f"Top anonymized series: {dominant_series.product_series} at {_fmt_pct(float(dominant_series.share))}."
        )
    if dominant_source is not None:
        top_contributors.append(
            f"Leading SKU source by labor value: {dominant_source.sku_source}."
        )

    actions = [
        "Review whether high-value categories also have strong fulfillment performance.",
        "Compare SKU source mix to see whether demand is driven by internal design, external purchase, or customer order.",
        "Use SKU drill-down for top product series when category concentration is high.",
        "Monitor categories with low fulfillment and high labor value first.",
    ]

    return _base_insight(
        title="Product Mix Insight",
        executive_summary=(
            "Product mix analysis highlights which generalized categories, anonymized series, "
            "and SKU sources drive delivery labor value."
        ),
        key_metrics={
            "Top 3 Category Share": _fmt_pct(concentration),
            "Category Count": _fmt_number(float(category_perf["product_category"].nunique())),
            "Series Count": _fmt_number(float(df["product_series"].nunique())) if "product_series" in df else "0",
        },
        trend_interpretation=[
            "Category-level fulfillment should be read together with labor value contribution.",
            "A dominant product mix may improve focus but can also increase exposure to category-specific disruptions.",
        ],
        top_contributors=top_contributors,
        potential_anomalies=anomalies,
        suggested_business_actions=actions,
        output_style=output_style,
        supporting_data={
            "category_summary": category_perf.head(50).to_dict(orient="records"),
            "source_summary": source.head(20).to_dict(orient="records"),
        },
    )


def generate_sku_drilldown_insight(
    df: pd.DataFrame,
    selected_sku: str | None,
    output_style: OutputStyle = "concise",
) -> Insight:
    """Generate SKU-level drill-down insights for one anonymized SKU."""
    if not selected_sku or "sku_id" not in df.columns:
        return _base_insight(
            title="SKU Drill-down Insight",
            executive_summary="Select an anonymized SKU to generate SKU-level insights.",
            key_metrics={},
            trend_interpretation=["No SKU has been selected."],
            top_contributors=[],
            potential_anomalies=[],
            suggested_business_actions=["Choose a SKU from the dropdown to inspect monthly performance."],
            output_style=output_style,
        )

    sku_df = df[df["sku_id"].astype(str) == str(selected_sku)].copy()
    if sku_df.empty:
        return _base_insight(
            title="SKU Drill-down Insight",
            executive_summary=f"No records found for {selected_sku}.",
            key_metrics={},
            trend_interpretation=[],
            top_contributors=[],
            potential_anomalies=[],
            suggested_business_actions=["Select another anonymized SKU."],
            output_style=output_style,
        )

    monthly = metrics.monthly_summary(sku_df).sort_values("year_month")
    fulfillment = metrics.fulfillment_rate(sku_df)
    gap = metrics.delivery_gap(sku_df)
    trend = _series_trend(monthly["monthly_delivery_qty"]) if not monthly.empty else "stable"

    anomalies = []
    if not monthly.empty:
        mean_delivery = monthly["monthly_delivery_qty"].mean()
        std_delivery = monthly["monthly_delivery_qty"].std()
        if pd.notna(std_delivery) and std_delivery > 0:
            high = monthly[monthly["monthly_delivery_qty"] > mean_delivery + std_delivery]
            low = monthly[monthly["monthly_delivery_qty"] < max(mean_delivery - std_delivery, 0)]
            anomalies.extend(
                f"Unusually high delivery in {_month_label(row.year_month)}: {_fmt_number(row.monthly_delivery_qty)}"
                for row in high.itertuples(index=False)
            )
            anomalies.extend(
                f"Unusually low delivery in {_month_label(row.year_month)}: {_fmt_number(row.monthly_delivery_qty)}"
                for row in low.itertuples(index=False)
            )
    if fulfillment < 0.95:
        anomalies.append(f"Selected SKU fulfillment is {_fmt_pct(fulfillment)}, below 95%.")
    if not anomalies:
        anomalies.append("No major SKU-level anomaly is flagged by the current local rules.")

    attribute_columns = ["factory", "factory_type", "product_category", "product_series", "sku_source"]
    attributes = {
        column: sorted(sku_df[column].dropna().astype(str).unique())[:5]
        for column in attribute_columns
        if column in sku_df.columns
    }

    actions = [
        "Compare this SKU against its product category and supplier context.",
        "Review months with unusually high or low delivery before making planning assumptions.",
        "Check whether gaps are concentrated in specific factories or factory types.",
    ]

    return _base_insight(
        title="SKU Drill-down Insight",
        executive_summary=(
            f"{selected_sku} appears {trend}, with fulfillment rate {_fmt_pct(fulfillment)} "
            f"and delivery gap {_fmt_number(gap)}."
        ),
        key_metrics={
            "Selected SKU": str(selected_sku),
            "Order Quantity": _fmt_number(metrics.total_order_qty(sku_df)),
            "Delivery Quantity": _fmt_number(metrics.total_delivery_qty(sku_df)),
            "Delivery Labor Value": _fmt_number(metrics.delivery_labor_value(sku_df)),
            "Fulfillment Rate": _fmt_pct(fulfillment),
            "Delivery Gap": _fmt_number(gap),
        },
        trend_interpretation=[
            f"Monthly delivery pattern appears {trend}.",
            "Read SKU movement together with related supplier, category, series, and source attributes.",
        ],
        top_contributors=[
            f"{column}: {', '.join(values)}" for column, values in attributes.items()
        ],
        potential_anomalies=anomalies,
        suggested_business_actions=actions,
        output_style=output_style,
        supporting_data={"sku_monthly_summary": monthly.head(50).to_dict(orient="records")},
    )


def generate_general_ai_assistant_insight(
    df: pd.DataFrame,
    analysis_type: str,
    selected_sku: str | None = None,
    output_style: OutputStyle = "concise",
) -> Insight:
    """Route an analysis request to the matching local insight generator."""
    if analysis_type == "Executive Overview":
        return generate_overview_insight(df, output_style=output_style)
    if analysis_type == "Supplier Performance":
        return generate_supplier_insight(df, output_style=output_style)
    if analysis_type == "Product Mix":
        return generate_product_mix_insight(df, output_style=output_style)
    if analysis_type == "SKU Drill-down":
        return generate_sku_drilldown_insight(df, selected_sku=selected_sku, output_style=output_style)
    return generate_overview_insight(df, output_style=output_style)


def generate_mock_insight(
    chart_title: str,
    metric_definitions: dict[str, str],
    filters: dict[str, Any],
    aggregated_data: list[dict[str, Any]],
    anomaly_flags: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    """Preserve the older chart-level API with a stronger deterministic response."""
    anomaly_count = sum(len(records) for records in anomaly_flags.values())
    return {
        "title": chart_title,
        "executive_summary": (
            f"{chart_title} uses {len(aggregated_data)} aggregated record(s) and "
            f"{len(metric_definitions)} metric definition(s)."
        ),
        "key_metrics": {name: definition for name, definition in metric_definitions.items()},
        "trend_interpretation": [
            "This chart-level insight is generated locally from pre-aggregated dashboard data."
        ],
        "top_contributors": ["Review the top records in the chart data table."],
        "potential_anomalies": [f"Rule-based anomaly records detected: {anomaly_count}."],
        "suggested_business_actions": [
            "Use the page-level AI Assistant options for richer executive, supplier, product, or SKU analysis."
        ],
        "data_privacy_note": PRIVACY_NOTE,
        "filters": filters,
    }


def build_prompt_template(
    chart_title: str,
    metric_definitions: dict[str, str],
    filters: dict[str, Any],
    aggregated_data: list[dict[str, Any]],
    anomaly_flags: dict[str, list[dict[str, Any]]],
) -> str:
    """Build a future LLM prompt template without calling any model."""
    payload = {
        "chart_title": chart_title,
        "metric_definitions": metric_definitions,
        "filters": filters,
        "aggregated_data": aggregated_data[:50],
        "anomaly_flags": anomaly_flags,
        "privacy_rule": PRIVACY_NOTE,
    }
    return (
        "Future optional LLM prompt template. Do not send private data, mapping tables, raw descriptions, "
        "product image paths, real supplier names, or real SKU identifiers.\n\n"
        "Return these sections:\n"
        "1. Executive summary\n"
        "2. Key metrics\n"
        "3. Trend interpretation\n"
        "4. Top contributors\n"
        "5. Potential anomalies\n"
        "6. Suggested business actions\n"
        "7. Data privacy note\n\n"
        f"Context JSON:\n{json.dumps(payload, ensure_ascii=False, indent=2, default=str)}"
    )


def build_page_prompt_template(
    analysis_type: str,
    output_style: OutputStyle,
    selected_sku: str | None,
    insight: Insight,
) -> str:
    """Build a future page-level LLM prompt template without calling any model."""
    payload = {
        "analysis_type": analysis_type,
        "output_style": output_style,
        "selected_sku": selected_sku,
        "local_rule_based_insight": insight,
        "privacy_rule": PRIVACY_NOTE,
    }
    return (
        "Future optional LLM prompt template for a privacy-safe public demo. "
        "Use only anonymized sample-data summaries. Never infer real companies, suppliers, SKUs, "
        "product images, descriptions, or mapping tables.\n\n"
        f"Context JSON:\n{json.dumps(payload, ensure_ascii=False, indent=2, default=str)}"
    )
