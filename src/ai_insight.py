"""Mock local insight generator for dashboard storytelling.

The functions in this module do not call external APIs. They prepare the shape
of a future LLM workflow while keeping the zero-budget version deterministic.
"""

from __future__ import annotations

import json
from typing import Any


def _count_anomalies(anomaly_flags: dict[str, list[dict[str, Any]]]) -> int:
    """Return the total number of anomaly records."""
    return sum(len(records) for records in anomaly_flags.values())


def _metric_names(metric_definitions: dict[str, str]) -> str:
    """Return a readable metric list."""
    if not metric_definitions:
        return "selected supply chain metrics"
    return ", ".join(metric_definitions)


def generate_mock_insight(
    chart_title: str,
    metric_definitions: dict[str, str],
    filters: dict[str, Any],
    aggregated_data: list[dict[str, Any]],
    anomaly_flags: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    """Generate deterministic local insights from aggregated chart data and flags."""
    row_count = len(aggregated_data)
    metric_text = _metric_names(metric_definitions)
    anomaly_count = _count_anomalies(anomaly_flags)

    if row_count == 0:
        main_trend = "No aggregated records are available for the selected chart."
    else:
        main_trend = f"{chart_title} is summarized across {row_count} aggregated records using {metric_text}."

    anomaly_lines: list[str] = []
    for category, records in anomaly_flags.items():
        if records:
            anomaly_lines.append(f"{category}: {len(records)} flagged record(s)")
    if not anomaly_lines:
        anomaly_lines.append("No rule-based anomalies were detected with the current thresholds.")

    possible_business_meaning = (
        "The flagged patterns may indicate fulfillment timing differences, demand changes, "
        "capacity pressure, product mix shifts, or supplier concentration risk."
    )

    recommended_follow_up_dimensions = [
        "factory",
        "factory_type",
        "product_category",
        "product_series",
        "sku_source",
        "year_month",
    ]

    executive_summary = (
        f"For {filters.get('chart_type', chart_title)}, the local assistant found "
        f"{anomaly_count} anomaly record(s). Review the recommended dimensions before "
        "turning this into an executive action item."
    )

    return {
        "main_trend": main_trend,
        "anomalies": anomaly_lines,
        "possible_business_meaning": possible_business_meaning,
        "recommended_follow_up_dimensions": recommended_follow_up_dimensions,
        "executive_summary": executive_summary,
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
    }
    return (
        "You are a supply chain analytics assistant. Use only the JSON context below. "
        "Do not invent raw data, supplier names, or confidential details.\n\n"
        "Return:\n"
        "1. Main trend\n"
        "2. Anomalies\n"
        "3. Possible business meaning\n"
        "4. Recommended follow-up dimensions\n"
        "5. Executive summary\n\n"
        f"Context JSON:\n{json.dumps(payload, ensure_ascii=False, indent=2, default=str)}"
    )

