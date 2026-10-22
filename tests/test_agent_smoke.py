"""Smoke test for the final repository entry point."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENTRY_POINT = PROJECT_ROOT / "agent.py"


def test_agent_entry_point_exports_callable() -> None:
    if not ENTRY_POINT.exists():
        pytest.skip("agent.py has not been added to the public package yet")

    spec = importlib.util.spec_from_file_location("public_agent", ENTRY_POINT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert callable(getattr(module, "agent", None))

