"""Tests for observation parsing and game-clock calculations."""

from __future__ import annotations

from conftest import make_observation
from src.state import GameClock, PlayerSnapshot, is_valid_observation, quantity


def test_clock_decodes_day_and_hour() -> None:
    clock = GameClock.from_observation(make_observation(step=49))

    assert clock.step == 49
    assert clock.day == 2
    assert clock.hour == 1
    assert clock.steps_left == 670


def test_player_snapshot_reads_private_state() -> None:
    observation = make_observation(
        cash=12_345,
        shed={"WHEAT": 9, "MILK": 3},
        hand_count=4,
    )

    player = PlayerSnapshot.from_observation(observation)

    assert player.seat == 0
    assert player.cash == 12_345
    assert player.hand_count == 4
    assert quantity(player.shed, "WHEAT") == 9
    assert quantity(player.shed, "UNKNOWN") == 0


def test_observation_validation_rejects_wrong_shapes() -> None:
    assert is_valid_observation(make_observation())
    assert not is_valid_observation({"step": 0, "farms": {}, "private": {}})
    assert not is_valid_observation({"step": "0", "farms": [], "private": {}})

