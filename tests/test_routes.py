"""Tests for route feasibility, isolation and deterministic selection."""

from __future__ import annotations

from src.routes import RouteCandidate, evaluate_routes, select_best_feasible


def test_selects_highest_risk_adjusted_utility() -> None:
    candidates = [
        RouteCandidate("stable", (), projected_value=1_000, risk_penalty=50),
        RouteCandidate("growth", (), projected_value=1_200, risk_penalty=100),
        RouteCandidate("broken", (), projected_value=9_999, feasible=False),
    ]

    selected = select_best_feasible(candidates)

    assert selected is not None
    assert selected.name == "growth"


def test_incumbent_is_kept_on_an_exact_tie() -> None:
    candidates = [
        RouteCandidate("new", (), projected_value=1_000),
        RouteCandidate("current", (), projected_value=1_000),
    ]

    selected = select_best_feasible(candidates, incumbent_name="current")

    assert selected is not None
    assert selected.name == "current"


def test_failed_builder_does_not_break_other_candidates() -> None:
    def valid_builder(_observation):
        return [{"name": "valid"}]

    def invalid_builder(_observation):
        raise ValueError("route is infeasible")

    candidates = evaluate_routes(
        {},
        {"valid": valid_builder, "invalid": invalid_builder},
        lambda actions, _observation: float(len(actions)),
    )

    by_name = {candidate.name: candidate for candidate in candidates}
    assert by_name["valid"].feasible
    assert by_name["valid"].projected_value == 1
    assert not by_name["invalid"].feasible

