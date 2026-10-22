"""Last-resort behavior when the full planner cannot safely finish in time.

The fallback first preserves an already completed plan.  It never switches to
an unrelated whole-game agent, and only adds sales that do not consume inputs
reserved by the remainder of today's schedule.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from .constants import MAX_MARKET_ORDERS, PROTECTED_INPUTS, SELL
from .economy import build_sale_orders
from .scheduler import latest_completed_plan
from .state import GameClock, PlayerSnapshot


Action = dict[str, Any]


def completed_plan_fallback(
    observation: Mapping[str, Any],
    plans: Sequence[Mapping[str, Any]],
) -> Action | None:
    """Use today's completed action and safely liquidate unreserved inventory."""

    clock = GameClock.from_observation(observation)
    player = PlayerSnapshot.from_observation(observation)
    plan = latest_completed_plan(plans, clock.day)
    if plan is None:
        return None

    action = plan.action_at(clock.hour, player.hand_count)
    reserved = plan.reserved_pickups_after(clock.hour)
    market = action.setdefault("market", [])
    already_selling = {
        order[1]
        for order in market
        if isinstance(order, list) and len(order) > 1 and order[0] == SELL
    }
    room = max(0, MAX_MARKET_ORDERS - len(market))
    market.extend(
        build_sale_orders(
            player.shed,
            reserved,
            excluded=PROTECTED_INPUTS,
            already_selling=already_selling,
            limit=room,
        )
    )
    return action


def minimal_legal_action(observation: Mapping[str, Any]) -> Action:
    """Return a shape-compatible no-op when no completed plan is available."""

    player = PlayerSnapshot.from_observation(observation)
    return {
        "farmer": None,
        "hands": [None] * player.hand_count,
        "market": [],
    }


def guarded_fallback(
    observation: Mapping[str, Any],
    plans: Sequence[Mapping[str, Any]],
) -> Action:
    """Choose the safest locally available fallback action."""

    return completed_plan_fallback(observation, plans) or minimal_legal_action(observation)

