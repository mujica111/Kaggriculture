"""Tests for deterministic accounting and liquidation helpers."""

from __future__ import annotations

from src.economy import build_sale_orders, inventory_value, market_price


def test_market_price_accepts_scalar_and_record_formats() -> None:
    market = {
        "MILK": 120,
        "WOOL": {"sell": 250},
        "TOMATO": {"price": 80},
    }

    assert market_price(market, "MILK") == 120
    assert market_price(market, "WOOL") == 250
    assert market_price(market, "TOMATO") == 80
    assert market_price(market, "UNKNOWN") == 0


def test_inventory_value_keeps_required_reserves() -> None:
    value = inventory_value(
        {"MILK": 5, "WHEAT": 10},
        {"MILK": 100, "WHEAT": 20},
        {"WHEAT": 6},
    )

    assert value == 580


def test_sale_orders_are_stable_and_respect_limits() -> None:
    orders = build_sale_orders(
        {"WOOL": 2, "MILK": 5, "WHEAT": 8, "EGG": 4},
        {"MILK": 2, "WHEAT": 8},
        excluded={"EGG"},
        limit=2,
    )

    assert orders == [["SELL", "MILK", 3], ["SELL", "WOOL", 2]]


def test_sale_orders_do_not_duplicate_existing_product() -> None:
    orders = build_sale_orders(
        {"MILK": 5, "WOOL": 2},
        already_selling={"MILK"},
    )

    assert orders == [["SELL", "WOOL", 2]]

