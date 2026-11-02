# Agricultural Strategy Agent

A multi-route heuristic agent developed for the Kaggriculture competition. The project combined gameplay replay analysis, regression testing, runtime profiling, and LLM-assisted implementation.

**Competition result:** Silver Medal — 488th of 10,148 teams (top 4.81%)

The agent was built upon an open-source multi-route baseline and extended through strategy reconstruction, calendar-based production planning, economic evaluation, and runtime safeguards.

[View Kaggle certification](https://www.kaggle.com/certification/competitions/a982295350/kaggriculture)

## Agent Design

The agent follows multiple production and economic routes rather than one fixed sequence of actions.

Its high-level decision process is:

```text
Game observation
    ↓
Load the active route and existing commitments
    ↓
Evaluate optional investments and crop rotations
    ↓
Compile feasible worker and material schedules
    ↓
Apply funding, inventory, and continuity checks
    ↓
Return a completed action or activate a runtime safeguard
```

### Route-Based Strategy

The open-source foundation represents strategies as route plans containing movement, farming, livestock, purchasing, and selling actions.

These routes provide stable production chains. Route decisions consider information including, cash and inventory, workers and livestock, crops and remaining production cycles, land ownership, market prices and unlocked shops, required production inputs and remaining game time and execution budget.

[gameshock of a game](image/gameshock.png)

### Calendar-Based Production Planning

Mid-game crop changes are evaluated as complete production projects rather than isolated planting action.

The planner considers land availability;
- crop maturity and remaining yields;
- planting, watering, fertilizing, harvesting, and transportation;
- seeds, feed, fertilizer, and warehouse capacity;
- worker availability and additional payroll;
- whether production can be completed and sold before the game ends;
- the opportunity cost of replacing the existing route.

### Joint Route Evaluation

An early implementation added a reconstructed tomato strategy on top of the existing route since the tomato project appeared profitable in isolation. However, it competed with the original strategy for land, workers, cash, inputs, inventory space, and transportation time.

The later system evaluates the new crop rotation together with the existing route. Protected work remains fixed, while compatible crop tasks may be rescheduled across available workers.

Combining routes thus involves retained value from the existing route, additional inputs and payroll, displaced production and land and transportation costs. New route will only be adapted in the multi-route system if much profit is estimated.

### Runtime Safeguards

Planning and worker allocation can be computationally expensive. The runtime controller monitors the current action allowance and remaining banked overage time.

If the available budget becomes too small, no complete plan exists and ***no*** action will be chosen.


## Strategy Development

### 1. From a Fixed Strategy to a Multi-Route Baseline

The first agent contained approximately 400 lines and followed a mostly fixed economic and production strategy.

This approach was understandable but inflexible. When shop availability, resources, or opponent development differed from its assumptions, the agent had few ways to recover.

I therefore adopted an open-source multi-route agent as the development baseline and focused on extending its route selection, economic rules, production planning, regression safety, and runtime reliability. Due to the massive scale of the codebase (over 10,000 lines of Python), I leveraged LLMs for code generation to optimize development efficiency and focus on system architecture.


### 2. Limitations of Reactive Counter-Strategies

Early development was strongly opponent-driven. I tested against newly released open-source agents, inspected losing replays, and implement counter-strategies.

Some changes produced immediate improvements, but they were difficult to maintain due to several factors including historical regression problem and new opponents with new strategies. Besides, changing the original route may break existing production.

After more than 20 major iterations, I shifted the objective from fixing individual losses to identifying recurring economic and production problems.

A candidate was no longer judged only by whether it won the replay that motivated it. It also had to preserve established advantages across unrelated test sets.

### 3. Learning from High-Ranking Gameplay

My first attempt supplied an LLM with approximately 100 replays without a sufficiently focused analytical objective. This produced little useful progress.

I later manually collected approximately 200 replays from another high-ranking player with a similar strategies comparing with the open-source baseline.
 
Comparison shows that their early behavior(roughly before 300 steps) was often similar, while larger differences emerged during mid-game investment and field expansion. 

I translated these observations into specific engineering questions and used the LLM to help investigate potential solutions. 

This more focused, evidence-driven approach produced more useful results than providing raw replay data without a clear analytical direction.

### 4. Regression-Aware Structural Improvements

Later development focused on complete economic chains rather than isolated parameter changes：

## Evaluation and Testing

No single evaluation method was treated as sufficient.

| Evaluation source | Purpose |
|---|---|
| Recent losing games | Check whether a candidate addressed newly observed weaknesses. |
| Historical regression sets | Detect damage to previously successful behavior. |
| Open-source opponents | Compare against reproducible public strategies. |
| Randomized game(shop) simulations | Test sensitivity to different market and shop configurations. |
| Frozen replay comparisons | Compare versions under identical recorded conditions. |
| Kaggle ranking submissions | Observe performance in the real execution environment. |

Mechanical checks verified that actions, worker routes, production windows, inputs, inventory, and market orders were valid.

Promising candidates were then compared with the baseline on the same cases. Evaluation considered score differences, win/loss direction, regressions, action divergence, and timeout behavior.

A candidate was rejected if it gained a small number of wins while introducing larger losses elsewhere, or showing high tendency of regressions.

### Preventing Replay Overfitting

Replay analysis was used to identify mechanisms, not to build per-game lookup rules.

Candidate conditions had to use state information available during normal gameplay, such as cash, inventory, crop age, land ownership, production capacity, shop availability, and remaining time, while episodes IDs, player identities and recorded future actions should not be considered. 

### Interpreting Offline Results

Frozen replay tests allow controlled version comparisons, but they do not measure a true win rate against an adaptive opponent.

If the candidate changes its behavior, a live opponent may respond differently from the actions stored in the replay. Offline results are therefore described as paired replay outcomes or frozen-opponent comparisons rather than general leaderboard win rates.

### Heuristic and RL Comparison

The heuristic and RL agents developed by my teammates were evaluated using the same internal 169-case procedure.

| Agent | Winning outcomes |
|---|---:|
| Multi-route heuristic agent | 145 / 169 |
| RL agent | 70 / 169 |

This internal comparison influenced the project's development direction. It does not establish that heuristic methods generally outperform reinforcement learning or represent an adaptive leaderboard win rate. However, under the available and limited development time, data, and training setup, the heuristic system made more effective use of existing strategic knowledge and was selected as the primary agent.

## Runtime Optimization

The environment provided a per-action allowance and a shared 60-second banked overage budget.

Worker scheduling is essentially an NP-Hard multi-agent routing problem. The massive task-to-worker combinations cause combinatorial explosion. Furthermore, strict temporal dependencies and tight compute budgets force the agent to trade off search depth against the risk of triggering timeouts. Step 288 was the most common source of a large runtime spike(shown by the game replays).

An early safeguard stopped planning when an individual step exceeded a fixed threshold and a backup plan will be adapted. This was too conservative: a long step did not always imply that the entire game would time out, and the backup could remove productive work or disrupt the original, active route.

The final safeguard instead considers the remaining overall budget. It stops expensive searches at controlled checkpoints and prefers plans that have already been completely compiled.

### Runtime Results

| Metric | Before optimization | After optimization |
|---|---:|---:|
| Test games | 30 | 30 |
| Timed-out games | 16 | 2 |
| Observed timeout rate | 53.3% | 6.7% |

The observed timeout rate decreased by 46.7 percentage points across two separate 30-game batches.

## My Contributions

My contributions included:

- inspecting gameplay replays and identifying strategic differences;
- selecting which differences were worth implementing;
- separating general problems from replay-specific symptoms;
- extending the open-source multi-route baseline;
- defining regression criteria and evaluation sets;
- rejecting overfitted or economically incomplete candidates;
- analyzing runtime failures and fallback behavior;
- directing LLM-assisted implementation and testing;

The RL agent used in initial comparison was developed by other team members.

## Key Takeaways

- **Use empirical comparisons to choose development methods.** Under this project's constraints, the heuristic approach outperformed the available RL implementation.

- **Give LLMs focused technical questions.** Raw replays produced limited value until gameplay differences were converted into specific hypotheses.

- **Prioritize generalization over reactive patching.** Fixing one replay is insufficient if the change damages unrelated games.

- **Treat regression and runtime as part of agent design.** A strategy must preserve existing advantages and consider efficiency.




## Results

Public summaries are stored in `results/`.

- `benchmark_summary.csv` contains version-level evaluation summaries.
- `version_comparison.md` explains the main differences between selected versions.
- `runtime_summary.md` documents the runtime evaluation and its measurement limitations.


## License and Attribution

This project was developed from an open-source baseline whose preserved source uses Apache License 2.0 notices.


