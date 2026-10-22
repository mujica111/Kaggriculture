"""Tests for the completed-plan and minimum-action fallbacks."""

from __future__ import annotations

from conftest import make_observation
from src.fallback import completed_plan_fallback, guarded_fallback


def empty_actions() -> list[dict]:
    return [{"farmer": None, "hands": [], "market": []} for _ in range(24)]


def test_fallback_keeps_inputs_needed_later_today() -> None:
    actions = empty_actions()
    actions[6]["farmer"] = ["PICKUP", "MILK", 3]
    plans = [{"day": 0, "actions": actions}]
    observation = make_observation(step=4, shed={"MILK": 5, "WOOL": 2})

    action = completed_plan_fallback(observation, plans)

    assert action is not None
    assert ["SELL", "MILK", 2] in action["market"]
    assert ["SELL", "WOOL", 2] in action["market"]


def test_fallback_does_not_sell_protected_inputs() -> None:
    plans = [{"day": 0, "actions": empty_actions()}]
    observation = make_observation(
        step=4,
        shed={"WHEAT": 20, "FERTILIZER": 10, "MILK": 2},
    )

    action = completed_plan_fallback(observation, plans)

    assert action is not None
    assert action["market"] == [["SELL", "MILK", 2]]


def test_missing_plan_returns_a_shape_compatible_noop() -> None:
    observation = make_observation(step=48, hand_count=3)

    action = guarded_fallback(observation, plans=[])

    assert action == {"farmer": None, "hands": [None, None, None], "market": []}

