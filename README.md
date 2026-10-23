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

These routes provide stable production chains. Additional decision layers may repair or extend a route when the current state differs from its original assumptions, without unnecessarily replacing the entire strategy.

Route decisions consider information including:

- cash and inventory;
- workers and livestock;
- crops and remaining production cycles;
- land ownership;
- market prices and unlocked shops;
- required production inputs;
- remaining game time and execution budget.

### Calendar-Based Production Planning

Midgame crop changes are evaluated as complete production projects rather than isolated planting actions.

The planner considers:

- land availability;
- crop maturity and remaining yields;
- planting, watering, fertilizing, harvesting, and transportation;
- seeds, feed, fertilizer, and warehouse capacity;
- worker availability and additional payroll;
- whether production can be completed and sold before the game ends;
- the opportunity cost of replacing the existing route.

A candidate is rejected if its work, funding, inputs, or timing cannot be completed.

### Joint Route Evaluation

An early implementation added a reconstructed tomato strategy on top of the existing route. Although the tomato project appeared profitable in isolation, it competed with the original strategy for land, workers, cash, inputs, inventory space, and transportation time.

The later system evaluates the new crop rotation together with the existing route. Protected work remains fixed, while compatible crop tasks may be rescheduled across available workers.

The agent therefore evaluates:

```text
Value of the new project
+ retained value from the existing route
- additional inputs and payroll
- displaced production
- land and transportation costs
```
A project is committed only when the combined schedule is feasible and economically preferable to retaining the original plan.

### Runtime Safeguards

Planning and worker allocation can be computationally expensive. The runtime controller monitors the current action allowance and remaining banked overage time.

If the available budget becomes too small:

1. the agent returns a compatible plan that has already been fully compiled; or
2. if no complete plan exists, it constructs a lightweight action from the current state.

The deployed policy does not read replay files, episode IDs, opponent identities, recorded future actions, or external strategy tables.


## Strategy Development

### 1. From a Fixed Strategy to a Multi-Route Baseline

The first agent contained approximately 400 lines and followed a mostly fixed economic and production strategy.

This approach was understandable but inflexible. When shop availability, resources, or opponent development differed from its assumptions, the agent had few ways to recover.

I therefore adopted an open-source multi-route agent as the development baseline. My work focused on extending its route selection, economic rules, production planning, regression safety, and runtime reliability.

### 2. Limitations of Reactive Counter-Strategies

Early development was strongly opponent-driven. I tested against newly released open-source agents, inspected losing replays, and used LLM-assisted iteration to implement counter-strategies.

Some changes produced immediate improvements, but they were difficult to maintain:

- a rule that defeated one strategy could weaken another matchup;
- changing complete routes during a game could break existing production;
- replay-specific fixes frequently caused historical regressions;
- additional rules increased code complexity and runtime cost.

After more than 20 major iterations, I shifted the objective from fixing individual losses to identifying recurring economic and production problems.

A candidate was no longer judged only by whether it won the replay that motivated it. It also had to preserve established advantages across unrelated test sets.

### 3. Learning from High-Ranking Gameplay

My first attempt supplied an LLM with approximately 100 replays without a sufficiently focused analytical objective. This produced little useful progress.

I later manually compared approximately 200 additional replays from a high-ranking player with the open-source baseline.

The comparison showed that early behavior was often similar, while larger differences emerged during midgame investment and field expansion. Recurring differences included:

- field allocation;
- crop mixtures;
- crop replacement timing;
- fourth-field tomato production;
- third-field crop rotation;
- coordination between hiring, purchasing, production, and selling.

These observations were converted into focused engineering questions.

Instead of asking the LLM to imitate an entire agent, I asked whether a proposed project could be funded, scheduled, supplied, harvested, transported, and sold without damaging the existing production chain.

This produced more useful results than supplying raw replays without a specific hypothesis.

### 4. Regression-Aware Structural Improvements

Later development focused on complete economic chains rather than isolated parameter changes.

When a candidate improved one test set but damaged another, I compared their action sequences and game states to determine:

- whether capital was committed too early or too late;
- whether required feed, seeds, or fertilizer were removed;
- whether additional workers recovered their payroll;
- whether new crops displaced more valuable production;
- whether goods reached the warehouse and were sold;
- whether runtime fallback disrupted the active route.

This process led to the joint crop-rotation and opportunity-cost evaluation used by the final agent.

## Evaluation and Testing

No single evaluation method was treated as sufficient.

| Evaluation source | Purpose |
|---|---|
| Recent losing games | Check whether a candidate addressed newly observed weaknesses. |
| Historical regression sets | Detect damage to previously successful behavior. |
| Open-source opponents | Compare against reproducible public strategies. |
| Randomized shop simulations | Test sensitivity to different market and shop configurations. |
| Frozen replay comparisons | Compare versions under identical recorded conditions. |
| Kaggle submissions | Observe performance in the real execution environment. |

### Evaluation Process

Meaningful changes followed a staged process:

```text
Mechanical feasibility checks
        ↓
Focused screening on relevant games
        ↓
Paired comparison with the baseline
        ↓
Cross-set regression testing
        ↓
Kaggle submission
```

Mechanical checks verified that actions, worker routes, production windows, inputs, inventory, and market orders were valid.

Promising candidates were then compared with the baseline on the same cases. Evaluation considered score differences, win/loss direction, regressions, action divergence, and timeout behavior.

A candidate was rejected if it gained a small number of wins while introducing larger losses elsewhere.

### Preventing Replay Overfitting

Replay analysis was used to identify mechanisms, not to build per-game lookup rules.

Candidate conditions had to use state information available during normal gameplay, such as cash, inventory, crop age, land ownership, production capacity, shop availability, and remaining time.

The deployed agent does not use:

- episode IDs;
- replay filenames;
- player identities;
- recorded future actions;
- hard-coded decisions for individual matches.

### Interpreting Offline Results

Frozen replay tests allow controlled version comparisons, but they do not measure a true win rate against an adaptive opponent.

If the candidate changes its behavior, a live opponent may respond differently from the actions stored in the replay. Offline results are therefore described as paired replay outcomes or frozen-opponent comparisons rather than general leaderboard win rates.

### Heuristic and RL Comparison

The heuristic and RL agents were evaluated using the same internal 169-case procedure.

| Agent | Winning outcomes |
|---|---:|
| Multi-route heuristic agent | 145 / 169 |
| RL agent | 70 / 169 |

This internal comparison influenced the project's development direction. It does not establish that heuristic methods generally outperform reinforcement learning or represent an adaptive leaderboard win rate.

Under the available development time, data, and training setup, the heuristic system made more effective use of existing strategic knowledge and was selected as the primary agent.

## Runtime Optimization

The environment provided a per-action allowance and a shared 60-second banked overage budget.

Execution profiling showed that most decisions were inexpensive, while several planning steps consumed substantially more time. Step 288 was the most common source of a large runtime spike.

An early safeguard stopped planning when an individual step exceeded a fixed threshold. This was too conservative: a long step did not always imply that the entire game would time out, and premature fallback could remove productive work or disrupt the active route.

The final safeguard instead considers the remaining overall budget. It stops expensive searches at controlled checkpoints and prefers plans that have already been completely compiled.

### Runtime Results

| Metric | Before optimization | After optimization |
|---|---:|---:|
| Test games | 30 | 30 |
| Timed-out games | 16 | 2 |
| Observed timeout rate | 53.3% | 6.7% |

The observed timeout rate decreased by 46.7 percentage points across two separate 30-game batches.

Average runtime is not directly compared because the older replay format recorded only consumption of the overage bank, while the newer logs recorded a duration for every action.

Runtime safeguards reduced but did not eliminate timeout risk. Execution could still vary with server load, initialization cost, state-dependent search complexity, and differences between local and competition environments.

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
- packaging the final self-contained submission agent.

The RL agent used in the internal comparison was developed by other team members.

## Key Takeaways

- **Use empirical comparisons to choose development methods.** Under this project's constraints, the heuristic approach outperformed the available RL implementation.

- **Give LLMs focused technical questions.** Raw replays produced limited value until gameplay differences were converted into specific hypotheses.

- **Evaluate complete economic chains.** A profitable crop project can reduce total value if it ignores payroll, displaced production, input requirements, or transportation.

- **Prioritize generalization over reactive patching.** Fixing one replay is insufficient if the change damages unrelated games.

- **Treat regression and runtime as part of agent design.** A strategy must preserve existing advantages and complete within the available execution budget.




## Results

Public summaries are stored in `results/`.

- `benchmark_summary.csv` contains version-level evaluation summaries.
- `version_comparison.md` explains the main differences between selected versions.
- `runtime_summary.md` documents the runtime evaluation and its measurement limitations.


## License and Attribution

This project was developed from an open-source baseline whose preserved source uses Apache License 2.0 notices.


