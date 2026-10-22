# Version comparison

| Version | Validation | Recorded result | Interpretation |
|---|---:|---:|---|
| Joint rotation experimental | 73 paired frozen-opponent games | Wins increased from 60 to 62; mean paired delta +366.75; no win-to-loss regression | Research improvement over its runtime-fixed parent. The saved manifest does not separately report every non-win as a loss. |
| Joint accelerated25 | 31 paired frozen-opponent games | 22 wins, 9 losses; mean paired delta +262.48; 7 improved, 24 unchanged, 0 regressed | Validates the merged joint policy and shared step-288 budget on the recorded set. |
| Joint init-only guard | 32 normal-budget exact comparisons | 32 unchanged; 0 action/state/score regressions | Initialization-only protection preserved the recorded normal-budget behavior. |

## Important limitations

1. Frozen-opponent comparisons hold the opponent action stream fixed. They are
   regression evidence, not proof of performance against an adaptive agent.
2. These sets were accumulated during development and are not presented as an
   untouched leaderboard holdout.
3. Emergency low-time fallback can materially reduce score. It is a last-resort
   mechanism rather than a strategic improvement.
4. A local successful run does not guarantee identical timing on Kaggle's
   execution environment.

