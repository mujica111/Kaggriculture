**Agricultural Strategy Agent**

A multi-route strategy agent developed for a Kaggle farming strategy competition, with strategy refinement guided by the analysis and imitation of gameplay patterns from a high-ranking player's replays and LLM-assisted code iteration.

Competition Result: **Silver Medal:488/10148 (top 5%)** 

Built upon an open-source baseline, the project involved iterative strategy refinement, opponent evaluation, randomized shop simulations, and runtime optimization, guided by gameplay replay analysis and empirical testing.


## Competition Results

**Platform:** Kaggle
**Achievement:** Silver Medal
link:https://www.kaggle.com/certification/competitions/a982295350/kaggriculture




## Strategy Development

The development process evolved from heuristic refinement into a replay-guided approach to strategy development.

### 1. Open-Source Baseline and Iterative Heuristic Refinement

- Started with an initial agent of approximately 400 lines, built around a fixed economic and production strategy.
- Later adopted an open-source agent with a multi-route strategy framework as the development baseline.
- Iteratively modified route selection, opponent-specific decisions, and strategic heuristics across numerous versions.
- Found that adding more rules did not consistently improve performance. Adjustments targeting specific losing scenarios could overfit known replays, introduce regressions, and fail to generalize to different opponents or game states.

### 2. Multi-Baseline Heuristic Refinement

- Experimented with multiple open-source agents, using their strategies as references to improve my own agent.
- Used LLM-assisted code modifications to develop counter-strategies against available open-source opponents and common game configurations.
- Achieved short-term performance improvements through targeted adjustments, but these gains were difficult to sustain as new open-source agents were continuously released.
- Repeatedly patched the strategy to address newly encountered opponents, creating a cycle of reactive modifications rather than a consistently generalizable strategy.
- After more than 20 iterations, recognized the limitations of this approach and shifted toward reconstructing strategies from a high-ranking player's gameplay replays.

### 3. Learning from High-Ranking Player Replays

Replay analysis became the central direction of further development after repeated heuristic modifications produced diminishing returns.

- Initially experimented with approximately 100 replays from another player, but found the available evidence too sparse and noisy to reliably identify strategic patterns.
- Shifted to approximately 200 replays from a high-ranking player to investigate how their decisions differed from the open-source baseline.
- Compared strategic behavior throughout games rather than focusing only on final outcomes. The high-ranking player's early-game behavior was often similar to the baseline, while more substantial differences emerged in the midgame.
- Used these observed differences to narrow down the decisions and game states requiring further investigation, then iteratively refined the agent with LLM assistance.

This process shifted strategy development from making isolated, intuition-driven rule changes toward identifying and reproducing decision patterns observed in stronger gameplay.

### 4. Replay-Guided Iteration and Generalization

- Investigated losses by tracing replays to points where resource levels, score progression, or strategic decisions began to diverge.
- Used the observed game state—including player resources, shop configuration, crops, and inventory—to investigate why a particular route or decision performed poorly.
- Evaluated new versions against recent losing games, a historical set of approximately 100 games, and existing open-source opponents.
- Ran additional simulations with randomized shop configurations to check whether improvements generalized beyond specific game setups.
- Continued revising the strategy based on measured results, while monitoring the risk of regressions and overfitting to previously observed games.

### 5. Runtime-Aware Decision Making

The agent also faced a strict execution-time limit in the competition environment.

- Inspected execution records to identify expensive decision steps involving statistical calculations.
- Found that switching to a fallback strategy whenever an individual step took too long could prematurely interrupt important strategic decisions.
- Changed the fallback logic to consider the remaining overall execution budget instead of relying solely on the duration of a single step.
- Tuned the threshold through repeated testing to reduce timeout risk while preserving important decisions. Differences between local and competition runtimes meant that timeouts were mitigated rather than completely eliminated.




## Evaluation and Testing

I used a multi-layered evaluation workflow to assess strategy improvements, detect regressions, and test generalization across different game scenarios.

| Evaluation Method | Purpose |
|---|---|
| Recent losing games | Tested whether a new version addressed weaknesses identified in the previous version's losing replays. |
| Historical test set | Evaluated changes against approximately 100 previously recorded games to detect regressions. |
| Open-source opponents | Compared performance against existing agents to assess competitiveness. |
| Randomized shop simulations | Tested whether improvements generalized across different shop configurations rather than relying on specific game setups. |

### Iterative Validation

- Compared successive agent versions using gameplay simulations, usually testing two versions at a time.
- Added further tests when early losses suggested that a change might be ineffective or harmful.
- Examined replay outcomes and changes in game progression to investigate why a strategy performed differently.
- Used Kaggle leaderboard performance as the primary external measure of progress, while accounting for the variability of results across submissions.

This workflow helped distinguish improvements against known failure cases from changes that could generalize to a wider range of game configurations.
