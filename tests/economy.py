"""Generic inventory valuation and safe-sale helpers.

This module does not decide the main strategy.  It provides deterministic
accounting primitives used by route evaluation and the time-pressure fallback.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .constants import MAX_MARKET_ORDERS, SELL


def market_price(market: Mapping[str, Any], product: str, default: int = 0) -> int:
    """Read a product price from either a scalar or a price record."""

    record = market.get(product, default)
    if isinstance(record, Mapping):
        for key in ("sell", "price", "value"):
            if key in record:
                return int(record[key])
        return default
    try:
        return int(record)
    except (TypeError, ValueError):
        return default


def inventory_value(
    inventory: Mapping[str, int],
    market: Mapping[str, Any],
    reserves: Mapping[str, int] | None = None,
) -> int:
    """Estimate the immediate liquidation value after keeping reserves."""

    reserves = reserves or {}
    total = 0
    for product, raw_quantity in inventory.items():
        amount = max(0, int(raw_quantity) - int(reserves.get(product, 0)))
        total += amount * market_price(market, product)
    return total


def build_sale_orders(
    inventory: Mapping[str, int],
    reserves: Mapping[str, int] | None = None,
    *,
    excluded: Iterable[str] = (),
    already_selling: Iterable[str] = (),
    limit: int = MAX_MARKET_ORDERS,
) -> list[list[Any]]:
    """Create deterministic sale orders without consuming planned inputs."""

    reserves = reserves or {}
    blocked = set(excluded) | set(already_selling)
    orders: list[list[Any]] = []
    for product in sorted(inventory):
        if product in blocked:
            continue
        amount = max(0, int(inventory[product]) - int(reserves.get(product, 0)))
        if amount:
            orders.append([SELL, product, amount])
            if len(orders) >= max(0, limit):
                break
    return orders

