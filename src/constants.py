"""Shared constants for the Kaggriculture agent.

Only stable game-level values belong here.  Strategy thresholds should stay
close to the policy that uses them so their purpose remains auditable.
"""

TURNS_PER_DAY = 24
TOTAL_DAYS = 30
TOTAL_STEPS = TURNS_PER_DAY * TOTAL_DAYS

MAX_MARKET_ORDERS = 10
FINAL_DAY = TOTAL_DAYS - 1

# Expensive planning checkpoints used by the current family of agents.
MIDGAME_PLANNING_STEP = 288
LATEGAME_PLANNING_STEP = 624
FINAL_PLANNING_STEP = 648

# Items normally retained while a completed daily plan still needs them.
PROTECTED_INPUTS = frozenset({"WHEAT", "FERTILIZER"})

BUY = "BUY"
SELL = "SELL"
PICKUP = "PICKUP"
PLACE = "PLACE"

