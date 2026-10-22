"""Interfaces for comparing complete strategy routes.

The public version deliberately avoids opponent IDs and replay-specific
fingerprints.  A route is selected only from feasibility and economic value
computed from the current observation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Protocol, Sequence


Action = dict[str, Any]
Observation = Mapping[str, Any]


class RouteBuilder(Protocol):
    def __call__(self, observation: Observation) -> Sequence[Action]: ...


@dataclass(frozen=True)
class RouteCandidate:
    name: str
    actions: Sequence[Action]
    projected_value: float
    feasible: bool = True
    risk_penalty: float = 0.0
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def utility(self) -> float:
        return float(self.projected_value) - max(0.0, float(self.risk_penalty))


def select_best_feasible(
    candidates: Sequence[RouteCandidate],
    *,
    incumbent_name: str | None = None,
) -> RouteCandidate | None:
    """Select by utility and retain the incumbent on an exact tie.

    Keeping the incumbent on ties avoids needless route changes and makes the
    result independent of candidate enumeration order.
    """

    valid = [candidate for candidate in candidates if candidate.feasible]
    if not valid:
        return None
    best_utility = max(candidate.utility for candidate in valid)
    tied = [candidate for candidate in valid if candidate.utility == best_utility]
    if incumbent_name is not None:
        for candidate in tied:
            if candidate.name == incumbent_name:
                return candidate
    return min(tied, key=lambda candidate: candidate.name)


def evaluate_routes(
    observation: Observation,
    builders: Mapping[str, RouteBuilder],
    value_fn: Callable[[Sequence[Action], Observation], float],
) -> list[RouteCandidate]:
    """Build independent candidates so one failed route cannot poison others."""

    candidates: list[RouteCandidate] = []
    for name, builder in builders.items():
        try:
            actions = list(builder(observation))
            candidates.append(
                RouteCandidate(
                    name=name,
                    actions=actions,
                    projected_value=value_fn(actions, observation),
                )
            )
        except (KeyError, TypeError, ValueError):
            candidates.append(
                RouteCandidate(name=name, actions=(), projected_value=0, feasible=False)
            )
    return candidates

