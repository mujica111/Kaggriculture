"""Daily-plan helpers shared by the main route and emergency fallback."""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .constants import PICKUP, TURNS_PER_DAY


Action = dict[str, Any]


@dataclass
class DailyPlan:
    day: int
    actions: list[Action]

    def __post_init__(self) -> None:
        if len(self.actions) != TURNS_PER_DAY:
            raise ValueError(f"a daily plan must contain {TURNS_PER_DAY} actions")

    def action_at(self, hour: int, hand_count: int) -> Action:
        """Return a defensive copy sized to the currently available workers."""

        if not 0 <= hour < TURNS_PER_DAY:
            raise IndexError("hour is outside the daily plan")
        action = copy.deepcopy(self.actions[hour])
        action["hands"] = list(action.get("hands", []))[: max(0, hand_count)]
        action.setdefault("market", [])
        return action

    def reserved_pickups_after(self, hour: int) -> dict[str, int]:
        """Count inputs that later actions in this plan still require."""

        reserved: dict[str, int] = {}
        for action in self.actions[hour + 1 :]:
            commands = [action.get("farmer"), *action.get("hands", [])]
            for command in commands:
                if not command or len(command) < 3 or command[0] != PICKUP:
                    continue
                product = str(command[1])
                reserved[product] = reserved.get(product, 0) + max(0, int(command[2]))
        return reserved


def latest_completed_plan(plans: Sequence[Mapping[str, Any]], day: int) -> DailyPlan | None:
    """Return today's completed plan; never replay yesterday's schedule."""

    if not plans:
        return None
    raw = plans[-1]
    if int(raw.get("day", -1)) != day:
        return None
    actions = raw.get("actions") or raw.get("plan")
    if not isinstance(actions, list) or len(actions) != TURNS_PER_DAY:
        return None
    return DailyPlan(day=day, actions=actions)

