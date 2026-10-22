"""Tests for daily-plan copying and future input reservations."""

from __future__ import annotations

import pytest

from src.scheduler import DailyPlan, latest_completed_plan


def empty_actions() -> list[dict]:
    return [{"farmer": None, "hands": [], "market": []} for _ in range(24)]


def test_plan_requires_exactly_one_day() -> None:
    with pytest.raises(ValueError):
        DailyPlan(day=0, actions=[])


def test_action_is_copied_and_trimmed_to_available_workers() -> None:
    actions = empty_actions()
    actions[3]["hands"] = [["MOVE", 1], ["MOVE", 2], ["MOVE", 3]]
    plan = DailyPlan(day=0, actions=actions)

    action = plan.action_at(3, hand_count=2)
    action["hands"][0][1] = 99

    assert len(action["hands"]) == 2
    assert plan.actions[3]["hands"][0] == ["MOVE", 1]


def test_future_pickups_are_reserved() -> None:
    actions = empty_actions()
    actions[5]["farmer"] = ["PICKUP", "WHEAT", 3]
    actions[7]["hands"] = [["PICKUP", "FERTILIZER", 2]]
    plan = DailyPlan(day=0, actions=actions)

    assert plan.reserved_pickups_after(3) == {"WHEAT": 3, "FERTILIZER": 2}


def test_yesterdays_plan_is_never_replayed() -> None:
    plans = [{"day": 2, "actions": empty_actions()}]

    assert latest_completed_plan(plans, day=3) is None
    assert latest_completed_plan(plans, day=2) is not None

