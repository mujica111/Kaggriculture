"""Shared pytest configuration for the public test suite."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def make_observation(
    *,
    step: int = 0,
    cash: int = 1_000,
    shed: dict[str, int] | None = None,
    hand_count: int = 2,
) -> dict:
    """Create a minimal observation accepted by the support modules."""

    return {
        "step": step,
        "player": 0,
        "farms": [{"hands": [{} for _ in range(hand_count)], "cash": cash}],
        "private": {"cash": cash, "shed": shed or {}},
    }

