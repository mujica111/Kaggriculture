"""Small, side-effect-free helpers for reading Kaggriculture observations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .constants import TOTAL_STEPS, TURNS_PER_DAY


Inventory = Mapping[str, int]
Observation = Mapping[str, Any]


@dataclass(frozen=True)
class GameClock:
    """Decoded position in the 30-day game."""

    step: int
    day: int
    hour: int
    steps_left: int

    @classmethod
    def from_observation(cls, observation: Observation) -> "GameClock":
        step = int(observation.get("step", 0))
        day, hour = divmod(step, TURNS_PER_DAY)
        return cls(
            step=step,
            day=day,
            hour=hour,
            steps_left=max(0, TOTAL_STEPS - step - 1),
        )


@dataclass(frozen=True)
class PlayerSnapshot:
    """The public and private state needed by generic support modules."""

    seat: int
    cash: int
    shed: Inventory
    hand_count: int

    @classmethod
    def from_observation(cls, observation: Observation) -> "PlayerSnapshot":
        seat = int(observation.get("player", 0))
        farms = observation.get("farms", [])
        farm = farms[seat] if 0 <= seat < len(farms) else {}
        private = observation.get("private", {})
        shed = private.get("shed", {})
        return cls(
            seat=seat,
            cash=int(private.get("cash", farm.get("cash", 0))),
            shed=shed if isinstance(shed, Mapping) else {},
            hand_count=len(farm.get("hands", [])),
        )


def quantity(inventory: Inventory, product: str) -> int:
    """Return a non-negative inventory quantity."""

    return max(0, int(inventory.get(product, 0)))


def is_valid_observation(observation: Observation) -> bool:
    """Perform the minimum structural validation needed before planning."""

    return (
        isinstance(observation, Mapping)
        and isinstance(observation.get("step", 0), int)
        and isinstance(observation.get("farms", []), list)
        and isinstance(observation.get("private", {}), Mapping)
    )

