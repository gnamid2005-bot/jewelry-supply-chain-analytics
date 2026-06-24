"""Lightweight multilingual UI helpers for the Streamlit dashboard."""

from __future__ import annotations

from typing import Any

import streamlit as st


LANGUAGES = {
    "en": "English",
    "zh_hans": "简体中文",
    "zh_hant": "繁體中文",
}

ANALYSIS_TYPE_VALUES = {
    "Executive Overview": {
        "en": "Executive Overview",
        "zh_hans": "供应链总览",
        "zh_hant": "供應鏈總覽",
    },
    "Supplier Performance": {
        "en": "Supplier Performance",
        "zh_hans": "供应商表现",
        "zh_hant": "供應商表現",
    },
    "Product Mix": {
        "en": "Product Mix",
        "zh_hans": "产品结构",
        "zh_hant": "產品結構",
    },
    "SKU Drill-down": {
        "en": "SKU Drill-down",
        "zh_hans": "SKU 下钻",
        "zh_hant": "SKU 下鑽",
    },
}

PAGE_VALUES = {
    "Supply Chain Overview": {
        "en": "Supply Chain Overview",
        "zh_hans": "供应链总览",
        "zh_hant": "供應鏈總覽",
    },
    "Supplier Performance": {
        "en": "Supplier Performance",
        "zh_hans": "供应商表现",
        "zh_hant": "供應商表現",
    },
    "Product Mix": {
        "en": "Product Mix",
        "zh_hans": "产品结构",
        "zh_hant": "產品結構",
    },
    "SKU Drilldown": {
        "en": "SKU Drilldown",
        "zh_hans": "SKU 下钻",
        "zh_hant": "SKU 下鑽",
    },
    "AI Insight Assistant": {
        "en": "AI Insight Assistant",
        "zh_hans": "AI 洞察助手",
        "zh_hant": "AI 洞察助手",
    },
}

OUTPUT_STYLE_VALUES = {
    "concise": {"en": "concise", "zh_hans": "简洁", "zh_hant": "簡潔"},
    "detailed": {"en": "detailed", "zh_hans": "详细", "zh_hant": "詳細"},
    "action-oriented": {"en": "action-oriented", "zh_hans": "行动导向", "zh_hant": "行動導向"},
}

TEXTS: dict[str, dict[str, str]] = {
    "app_title": {
        "en": "Jewelry Supply Chain Analytics",
        "zh_hans": "珠宝供应链数据分析",
        "zh_hant": "珠寶供應鏈數據分析",
    },
    "sidebar_title": {"en": "Jewelry Supply Chain", "zh_hans": "珠宝供应链", "zh_hant": "珠寶供應鏈"},
    "language": {"en": "Language", "zh_hans": "语言", "zh_hant": "語言"},
    "dashboard_page": {"en": "Dashboard page", "zh_hans": "仪表板页面", "zh_hant": "儀表板頁面"},
    "data_source_caption": {
        "en": "Data source: anonymized public sample CSV only.",
        "zh_hans": "数据来源：仅使用公开脱敏样例 CSV。",
        "zh_hant": "資料來源：僅使用公開去識別化樣例 CSV。",
    },
    "missing_sample_info": {
        "en": "No anonymized sample data found yet. Generate it locally with `python -m src.anonymize --max-rows 10000 --scale-factor 1.0`, then rerun the app.",
        "zh_hans": "尚未找到脱敏样例数据。请先在本地运行 `python -m src.anonymize --max-rows 10000 --scale-factor 1.0`，然后重新启动应用。",
        "zh_hant": "尚未找到去識別化樣例資料。請先在本地執行 `python -m src.anonymize --max-rows 10000 --scale-factor 1.0`，然後重新啟動應用。",
    },
    "privacy_caption": {
        "en": "The dashboard intentionally does not read `data/raw/` or `data/processed/`.",
        "zh_hans": "此仪表板不会读取 `data/raw/` 或 `data/processed/`。",
        "zh_hant": "此儀表板不會讀取 `data/raw/` 或 `data/processed/`。",
    },
    "overview_title": {"en": "Supply Chain Overview", "zh_hans": "供应链总览", "zh_hant": "供應鏈總覽"},
    "suppliers_title": {"en": "Supplier Performance", "zh_hans": "供应商表现", "zh_hant": "供應商表現"},
    "product_mix_title": {"en": "Product Mix", "zh_hans": "产品结构", "zh_hant": "產品結構"},
    "sku_drilldown_title": {"en": "SKU Drilldown", "zh_hans": "SKU 下钻", "zh_hant": "SKU 下鑽"},
    "ai_title": {"en": "AI Insight Assistant", "zh_hans": "AI 洞察助手", "zh_hant": "AI 洞察助手"},
    "total_order_qty": {"en": "Total Order Quantity", "zh_hans": "总发单件数", "zh_hant": "總發單件數"},
    "total_delivery_qty": {"en": "Total Delivery Quantity", "zh_hans": "总起货件数", "zh_hant": "總起貨件數"},
    "delivery_labor_value": {"en": "Delivery Labor Value", "zh_hans": "起货工值", "zh_hant": "起貨工值"},
    "fulfillment_rate": {"en": "Fulfillment Rate", "zh_hans": "履约率", "zh_hant": "履約率"},
    "active_sku_count": {"en": "Active SKU Count", "zh_hans": "活跃 SKU 数", "zh_hant": "活躍 SKU 數"},
    "monthly_column_warning": {
        "en": "Monthly charts require a `year_month` column.",
        "zh_hans": "月度图表需要 `year_month` 字段。",
        "zh_hant": "月度圖表需要 `year_month` 欄位。",
    },
    "monthly_order_delivery_trend": {
        "en": "Monthly Order vs Delivery Quantity Trend",
        "zh_hans": "月度发单 vs 起货件数趋势",
        "zh_hant": "月度發單 vs 起貨件數趨勢",
    },
    "monthly_labor_value_trend": {
        "en": "Monthly Delivery Labor Value Trend",
        "zh_hans": "月度起货工值趋势",
        "zh_hant": "月度起貨工值趨勢",
    },
    "monthly_fulfillment_trend": {
        "en": "Monthly Fulfillment Rate Trend",
        "zh_hans": "月度履约率趋势",
        "zh_hant": "月度履約率趨勢",
    },
    "order_quantity": {"en": "Order Quantity", "zh_hans": "发单件数", "zh_hant": "發單件數"},
    "delivery_quantity": {"en": "Delivery Quantity", "zh_hans": "起货件数", "zh_hant": "起貨件數"},
    "quantity": {"en": "Quantity", "zh_hans": "件数", "zh_hant": "件數"},
    "metric": {"en": "Metric", "zh_hans": "指标", "zh_hant": "指標"},
    "value": {"en": "Value", "zh_hans": "数值", "zh_hant": "數值"},
    "supplier_top5_share": {"en": "Supplier Top 5 Share", "zh_hans": "前五供应商占比", "zh_hant": "前五供應商占比"},
    "supplier_hhi": {"en": "Supplier HHI", "zh_hans": "供应商 HHI", "zh_hant": "供應商 HHI"},
    "factory_type_comparison": {"en": "Factory Type Comparison", "zh_hans": "工厂类型对比", "zh_hant": "工廠類型對比"},
    "top10_factories": {
        "en": "Top 10 Factories by Delivery Labor Value",
        "zh_hans": "按起货工值排名的前 10 工厂",
        "zh_hant": "按起貨工值排名的前 10 工廠",
    },
    "factory_contribution_share": {"en": "Factory Contribution Share", "zh_hans": "工厂贡献占比", "zh_hant": "工廠貢獻占比"},
    "sortable_supplier_table": {"en": "Sortable Supplier Table", "zh_hans": "可排序供应商表", "zh_hant": "可排序供應商表"},
    "product_category_contribution": {"en": "Product Category Contribution", "zh_hans": "产品大类贡献", "zh_hant": "產品大類貢獻"},
    "product_series_contribution": {"en": "Product Series Contribution", "zh_hans": "产品系列贡献", "zh_hant": "產品系列貢獻"},
    "sku_source_distribution": {"en": "SKU Source Distribution", "zh_hans": "SKU 来源分布", "zh_hant": "SKU 來源分布"},
    "avg_labor_by_category": {
        "en": "Average Labor Value per Unit by Category",
        "zh_hans": "各产品大类单位平均工值",
        "zh_hant": "各產品大類單位平均工值",
    },
    "sku_required_warning": {"en": "SKU drilldown requires a `sku_id` column.", "zh_hans": "SKU 下钻需要 `sku_id` 字段。", "zh_hant": "SKU 下鑽需要 `sku_id` 欄位。"},
    "select_sku": {"en": "Select or search SKU", "zh_hans": "选择或搜索 SKU", "zh_hant": "選擇或搜尋 SKU"},
    "sku_trend_warning": {"en": "SKU trend requires a `year_month` column.", "zh_hans": "SKU 趋势需要 `year_month` 字段。", "zh_hant": "SKU 趨勢需要 `year_month` 欄位。"},
    "sku_monthly_trend": {
        "en": "Monthly Order, Delivery, and Labor Value Trend",
        "zh_hans": "月度发单、起货与工值趋势",
        "zh_hant": "月度發單、起貨與工值趨勢",
    },
    "ai_caption": {
        "en": "Local rule-based analytics assistant. It uses anonymized sample data only and does not call paid APIs, external LLMs, raw data, or processed private data.",
        "zh_hans": "本地规则型分析助手。仅使用脱敏样例数据，不调用付费 API、外部 LLM、原始数据或私有 processed 数据。",
        "zh_hant": "本地規則型分析助手。僅使用去識別化樣例資料，不呼叫付費 API、外部 LLM、原始資料或私有 processed 資料。",
    },
    "analysis_type": {"en": "Analysis type", "zh_hans": "分析类型", "zh_hant": "分析類型"},
    "output_style": {"en": "Output style", "zh_hans": "输出风格", "zh_hant": "輸出風格"},
    "optional_selected_sku": {"en": "Optional selected SKU", "zh_hans": "可选 SKU", "zh_hant": "可選 SKU"},
    "sku_selector_caption": {"en": "SKU selector appears for SKU Drill-down.", "zh_hans": "选择 SKU 下钻时会显示 SKU 选择器。", "zh_hant": "選擇 SKU 下鑽時會顯示 SKU 選擇器。"},
    "select_sku_context": {"en": "Select an anonymized SKU to render the SKU context chart.", "zh_hans": "请选择一个脱敏 SKU 以显示 SKU 上下文图表。", "zh_hant": "請選擇一個去識別化 SKU 以顯示 SKU 脈絡圖表。"},
    "executive_summary": {"en": "Executive summary", "zh_hans": "管理层摘要", "zh_hant": "管理層摘要"},
    "key_metrics": {"en": "Key metrics", "zh_hans": "关键指标", "zh_hant": "關鍵指標"},
    "trend_interpretation": {"en": "Trend interpretation", "zh_hans": "趋势解读", "zh_hant": "趨勢解讀"},
    "top_contributors": {"en": "Top contributors", "zh_hans": "主要贡献项", "zh_hant": "主要貢獻項"},
    "potential_anomalies": {"en": "Potential anomalies", "zh_hans": "潜在异常", "zh_hant": "潛在異常"},
    "suggested_business_actions": {"en": "Suggested business actions", "zh_hans": "建议业务行动", "zh_hant": "建議業務行動"},
    "data_privacy_note": {"en": "Data privacy note", "zh_hans": "数据隐私说明", "zh_hant": "資料隱私說明"},
    "none_flagged": {"en": "None flagged.", "zh_hans": "未发现明显异常。", "zh_hant": "未發現明顯異常。"},
    "aggregated_chart_json": {"en": "Aggregated chart data JSON", "zh_hans": "聚合图表数据 JSON", "zh_hant": "聚合圖表資料 JSON"},
    "future_prompt": {"en": "Future optional LLM prompt template", "zh_hans": "未来可选 LLM 提示词模板", "zh_hant": "未來可選 LLM 提示詞範本"},
}

INSIGHT_REPLACEMENTS = {
    "zh_hans": {
        "Executive Overview Insight": "供应链总览洞察",
        "Supplier Performance Insight": "供应商表现洞察",
        "Product Mix Insight": "产品结构洞察",
        "SKU Drill-down Insight": "SKU 下钻洞察",
        "Total Order Quantity": "总发单件数",
        "Total Delivery Quantity": "总起货件数",
        "Fulfillment Rate": "履约率",
        "Delivery Gap": "交付缺口",
        "Active SKU Count": "活跃 SKU 数",
        "Delivery Labor Value": "起货工值",
        "Supplier Top 5 Share": "前五供应商占比",
        "Supplier HHI": "供应商 HHI",
        "Supplier Count": "供应商数量",
        "Top 3 Category Share": "前三产品大类占比",
        "Category Count": "产品大类数量",
        "Series Count": "产品系列数量",
        "Selected SKU": "所选 SKU",
        "Order Quantity": "发单件数",
        "Delivery Quantity": "起货件数",
        "Insights are generated locally from anonymized sample data only. No raw company data, real supplier names, real SKU identifiers, product images, raw descriptions, mapping tables, or paid APIs are used.": "洞察内容仅基于本地脱敏样例数据生成。不使用原始公司数据、真实供应商名称、真实 SKU 标识、产品图片、原始描述、映射表或付费 API。",
        "No major overview-level anomaly is flagged by the current local rules.": "当前本地规则未发现明显总览层面异常。",
        "No supplier has a positive delivery gap in the top gap scan.": "在交付缺口扫描中，未发现主要供应商存在正向缺口。",
        "No major product-mix anomaly is flagged by the current local rules.": "当前本地规则未发现明显产品结构异常。",
        "No major SKU-level anomaly is flagged by the current local rules.": "当前本地规则未发现明显 SKU 层面异常。",
        "Delivery trend appears": "起货趋势看起来",
        "based on monthly delivery quantity movement.": "，判断依据为月度起货件数变化。",
        "Total delivery covers": "总起货覆盖",
        "of total order quantity.": "的总发单件数。",
        "Best fulfillment month is": "履约率最佳月份为",
        "Weakest fulfillment month is": "履约率最弱月份为",
        "Top five supplier share is": "前五供应商占比为",
        "and HHI is": "，HHI 为",
        "Supplier dependency appears concentrated.": "供应商依赖度看起来较集中。",
        "Supplier dependency appears diversified under the current thresholds.": "在当前阈值下，供应商依赖度看起来较分散。",
        "Review months with the weakest fulfillment rate before drilling into suppliers.": "优先查看履约率最弱的月份，再下钻到供应商。",
        "Compare supplier contribution and product mix for months with large delivery gaps.": "对交付缺口较大的月份，对比供应商贡献和产品结构。",
        "Use SKU drill-down for high-volume SKUs when delivery trend becomes volatile.": "当起货趋势波动较大时，对高量 SKU 进行下钻。",
        "Review high-gap suppliers by month to separate timing effects from capacity issues.": "按月份查看高缺口供应商，区分时间差与产能问题。",
        "Compare in-house and external supplier types for concentration exposure.": "对比自营与外部供应类型的集中度风险。",
        "Review whether high-value categories also have strong fulfillment performance.": "检查高价值产品大类是否也具备较强履约表现。",
        "Use SKU drill-down for top product series when category concentration is high.": "当产品大类集中度较高时，对头部产品系列进行 SKU 下钻。",
    },
    "zh_hant": {
        "Executive Overview Insight": "供應鏈總覽洞察",
        "Supplier Performance Insight": "供應商表現洞察",
        "Product Mix Insight": "產品結構洞察",
        "SKU Drill-down Insight": "SKU 下鑽洞察",
        "Total Order Quantity": "總發單件數",
        "Total Delivery Quantity": "總起貨件數",
        "Fulfillment Rate": "履約率",
        "Delivery Gap": "交付缺口",
        "Active SKU Count": "活躍 SKU 數",
        "Delivery Labor Value": "起貨工值",
        "Supplier Top 5 Share": "前五供應商占比",
        "Supplier HHI": "供應商 HHI",
        "Supplier Count": "供應商數量",
        "Top 3 Category Share": "前三產品大類占比",
        "Category Count": "產品大類數量",
        "Series Count": "產品系列數量",
        "Selected SKU": "所選 SKU",
        "Order Quantity": "發單件數",
        "Delivery Quantity": "起貨件數",
        "Insights are generated locally from anonymized sample data only. No raw company data, real supplier names, real SKU identifiers, product images, raw descriptions, mapping tables, or paid APIs are used.": "洞察內容僅基於本地去識別化樣例資料生成。不使用原始公司資料、真實供應商名稱、真實 SKU 標識、產品圖片、原始描述、映射表或付費 API。",
        "No major overview-level anomaly is flagged by the current local rules.": "目前本地規則未發現明顯總覽層面異常。",
        "No supplier has a positive delivery gap in the top gap scan.": "在交付缺口掃描中，未發現主要供應商存在正向缺口。",
        "No major product-mix anomaly is flagged by the current local rules.": "目前本地規則未發現明顯產品結構異常。",
        "No major SKU-level anomaly is flagged by the current local rules.": "目前本地規則未發現明顯 SKU 層面異常。",
        "Delivery trend appears": "起貨趨勢看起來",
        "based on monthly delivery quantity movement.": "，判斷依據為月度起貨件數變化。",
        "Total delivery covers": "總起貨覆蓋",
        "of total order quantity.": "的總發單件數。",
        "Best fulfillment month is": "履約率最佳月份為",
        "Weakest fulfillment month is": "履約率最弱月份為",
        "Top five supplier share is": "前五供應商占比為",
        "and HHI is": "，HHI 為",
        "Supplier dependency appears concentrated.": "供應商依賴度看起來較集中。",
        "Supplier dependency appears diversified under the current thresholds.": "在目前閾值下，供應商依賴度看起來較分散。",
        "Review months with the weakest fulfillment rate before drilling into suppliers.": "優先查看履約率最弱的月份，再下鑽到供應商。",
        "Compare supplier contribution and product mix for months with large delivery gaps.": "對交付缺口較大的月份，對比供應商貢獻和產品結構。",
        "Use SKU drill-down for high-volume SKUs when delivery trend becomes volatile.": "當起貨趨勢波動較大時，對高量 SKU 進行下鑽。",
        "Review high-gap suppliers by month to separate timing effects from capacity issues.": "按月份查看高缺口供應商，區分時間差與產能問題。",
        "Compare in-house and external supplier types for concentration exposure.": "對比自營與外部供應類型的集中度風險。",
        "Review whether high-value categories also have strong fulfillment performance.": "檢查高價值產品大類是否也具備較強履約表現。",
        "Use SKU drill-down for top product series when category concentration is high.": "當產品大類集中度較高時，對頭部產品系列進行 SKU 下鑽。",
    },
}


def language_selector() -> str:
    """Render a Streamlit sidebar language selector and return the language code."""
    labels = list(LANGUAGES.values())
    current = st.session_state.get("language", "en")
    current_index = list(LANGUAGES).index(current) if current in LANGUAGES else 0
    selected_label = st.sidebar.selectbox(
        TEXTS["language"][current],
        labels,
        index=current_index,
        key="language_selector",
    )
    selected = next(code for code, label in LANGUAGES.items() if label == selected_label)
    st.session_state["language"] = selected
    return selected


def t(key: str, lang: str = "en") -> str:
    """Translate one UI key."""
    return TEXTS.get(key, {}).get(lang, TEXTS.get(key, {}).get("en", key))


def option_label(value: str, lang: str = "en") -> str:
    """Translate a known option value while preserving its internal value."""
    if value in PAGE_VALUES:
        return PAGE_VALUES[value].get(lang, value)
    if value in ANALYSIS_TYPE_VALUES:
        return ANALYSIS_TYPE_VALUES[value].get(lang, value)
    if value in OUTPUT_STYLE_VALUES:
        return OUTPUT_STYLE_VALUES[value].get(lang, value)
    return value


def translate_insight_value(value: Any, lang: str = "en") -> Any:
    """Translate insight headings and common sentence patterns without changing data labels."""
    if lang == "en":
        return value
    if isinstance(value, dict):
        return {translate_insight_value(k, lang): translate_insight_value(v, lang) for k, v in value.items()}
    if isinstance(value, list):
        return [translate_insight_value(item, lang) for item in value]
    if not isinstance(value, str):
        return value

    translated = value
    for source, target in INSIGHT_REPLACEMENTS.get(lang, {}).items():
        translated = translated.replace(source, target)
    return translated
