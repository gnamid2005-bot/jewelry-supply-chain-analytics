"""Unit tests for supply chain KPI metrics using synthetic data only."""

import math

import pandas as pd

from src.metrics import (
    active_sku_count,
    delivery_gap,
    fulfillment_rate,
    supplier_hhi,
    supplier_top5_share,
)


def _synthetic_supply_chain_df() -> pd.DataFrame:
    """Create a tiny non-sensitive dataframe for KPI tests."""
    return pd.DataFrame(
        {
            "sku_id": ["SKU_A", "SKU_B", "SKU_C", "SKU_D", "SKU_E", "SKU_F"],
            "factory": ["F1", "F2", "F3", "F4", "F5", "F6"],
            "monthly_order_qty": [100, 50, 30, 20, 0, 10],
            "monthly_delivery_qty": [80, 50, 30, 20, 5, 0],
            "monthly_delivery_labor_value": [400.0, 300.0, 150.0, 100.0, 50.0, 0.0],
        }
    )


def test_fulfillment_rate() -> None:
    """Fulfillment rate is total delivery quantity divided by total order quantity."""
    df = _synthetic_supply_chain_df()

    assert math.isclose(fulfillment_rate(df), 185 / 210)


def test_delivery_gap() -> None:
    """Delivery gap is total order quantity minus total delivery quantity."""
    df = _synthetic_supply_chain_df()

    assert delivery_gap(df) == 25


def test_active_sku_count() -> None:
    """Active SKU count includes SKUs with either order or delivery activity."""
    df = _synthetic_supply_chain_df()

    assert active_sku_count(df) == 6


def test_supplier_top5_share() -> None:
    """Top five supplier share uses delivery labor value concentration."""
    df = _synthetic_supply_chain_df()

    assert math.isclose(supplier_top5_share(df), 1.0)


def test_supplier_hhi() -> None:
    """Supplier HHI is the sum of squared supplier contribution shares."""
    df = _synthetic_supply_chain_df()
    expected = (0.4**2) + (0.3**2) + (0.15**2) + (0.1**2) + (0.05**2) + (0.0**2)

    assert math.isclose(supplier_hhi(df), expected)
