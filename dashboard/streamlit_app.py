"""Main Streamlit entry point for the supply chain analytics dashboard."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dashboard.components.data_loader import load_sample_data, show_missing_sample_data_message
from dashboard.i18n import language_selector, option_label, t
from dashboard.pages import ai_assistant, overview, product_mix, sku_drilldown, suppliers


PAGES = {
    "Supply Chain Overview": overview.render,
    "Supplier Performance": suppliers.render,
    "Product Mix": product_mix.render,
    "SKU Drilldown": sku_drilldown.render,
    "AI Insight Assistant": ai_assistant.render,
}


def main() -> None:
    """Render the Streamlit dashboard shell and selected page."""
    st.set_page_config(
        page_title="Jewelry Supply Chain Analytics",
        page_icon="J",
        layout="wide",
    )

    lang = language_selector()
    st.sidebar.title(t("sidebar_title", lang))
    selected_page = st.sidebar.radio(
        t("dashboard_page", lang),
        list(PAGES.keys()),
        format_func=lambda page: option_label(page, lang),
    )
    st.sidebar.caption(t("data_source_caption", lang))

    df = load_sample_data()
    if df.empty:
        st.title(t("app_title", lang))
        show_missing_sample_data_message(lang)
        return

    PAGES[selected_page](df, lang)


if __name__ == "__main__":
    main()
