# Agricultural Strategy Agent

A multi-route heuristic agent developed for the Kaggriculture competition. The strategy was refined through comparative gameplay replay analysis, controlled regression testing, runtime profiling, and LLM-assisted implementation.

**Competition result:** Silver Medal — 488th of 10,148 teams (top 4.81%)

The project was built upon an open-source baseline and extended through iterative strategy development, opponent evaluation, randomized shop simulations, and runtime optimization. A major part of the work involved converting patterns observed in high-ranking gameplay into testable strategic hypotheses while controlling for regression and overfitting.

## Competition Result

- **Platform:** Kaggle
- **Competition:** Kaggriculture
- **Achievement:** Silver Medal
- **Final rank:** 488th of 10,148 teams
- **Percentile:** Top 4.81%

[View Kaggle certification](https://www.kaggle.com/certification/competitions/a982295350/kaggriculture)

## Agent Design

The agent uses a multi-route heuristic framework rather than following one fixed sequence of actions. Its decisions are derived from the observable game state and adjusted according to available resources, production capacity, investment timing, and runtime constraints.

- **Multi-route planning:** Supports multiple production and economic routes with different investment timing, crop allocation, livestock development, and selling decisions.

- **State-aware decision-making:** Evaluates observable information such as cash, inventory, available workers, crop state, livestock, shop availability, remaining production cycles, and game progress.

- **Adaptive economic management:** Coordinates purchases, planting, feeding, fertilizing, harvesting, transportation, and sales while considering capital requirements and whether an investment can generate returns before the game ends.

- **Opponent-state awareness:** Uses observable opponent development as contextual information where it affects competitive priorities. The agent does not depend on opponent identities, replay IDs, or hard-coded responses to individual matches.

- **Route continuity:** Strategic adjustments are designed to preserve viable production chains. A local state change does not automatically replace the entire route.

- **Runtime safeguards:** Monitors the remaining execution budget and can switch to lightweight fallback decisions when necessary, reducing timeout risk while preserving completed strategic decisions whenever possible.

## Strategy Development

The project evolved from a fixed-strategy agent into a multi-route system, followed by a broader effort to reconstruct effective strategies from high-ranking gameplay.

### 1. From a Fixed Strategy to Multi-Route Heuristics

The initial agent contained approximately 400 lines and followed a largely fixed economic and production strategy.

I later adopted an open-source multi-route agent as the development baseline and iteratively refined its route selection, observable opponent-state heuristics, and economic decision rules.

This stage revealed an important limitation: adding more rules did not consistently improve performance. Modifications designed around individual losing games often overfitted known replays, introduced regressions, or performed poorly under different game states and shop configurations.

As a result, new changes increasingly had to demonstrate value across multiple games rather than solve only the replay that originally motivated them.

### 2. Moving Beyond Reactive Open-Source Adaptation

I experimented with several open-source agents and used LLM-assisted code iteration to develop responses to commonly available strategies and opponent configurations.

Although some targeted changes produced immediate improvements, the gains were difficult to maintain as new open-source agents appeared. A route that countered one opponent could weaken performance against another or damage an existing production chain.

After more than 20 major iterations, I concluded that repeatedly patching the agent against the latest opponent was producing diminishing returns. I therefore shifted the focus from reactive counter-strategy development toward identifying broader strategic principles from high-ranking gameplay.

### 3. Comparing Heuristics and Reinforcement Learning

In parallel, other members of the team developed a reinforcement-learning agent. This allowed us to compare the RL approach with my multi-route heuristic agent under the same project constraints.

On a shared 169-case offline evaluation set, the heuristic agent recorded 145 winning outcomes, while the RL agent recorded 70 under the same evaluation procedure.

These figures describe the project's internal offline evaluation and should not be interpreted as leaderboard win rates against adaptive opponents.

The heuristic approach benefited from existing strategic knowledge and the ability to incorporate specific economic reasoning. The RL agent did not achieve comparable results within the available development period, partly because an effective reference policy was not available to guide learning.

This comparison supported the decision to continue improving the heuristic agent through strategic analysis and reconstruction rather than relying primarily on further trial-and-error modification or RL training.

### 4. Reconstructing Strategies from High-Ranking Replays

My first attempt involved providing an LLM with approximately 100 gameplay replays without defining a sufficiently focused analytical objective. This produced little useful progress.

I subsequently examined approximately 200 replays from a high-ranking player and compared them with the open-source baseline.

The analysis produced several findings:

- Early-game behavior was often similar, while larger strategic differences emerged during the midgame.
- Crop allocation and field usage differed across several recurring production routes.
- The reference agent's use of the fourth field for larger-scale tomato production appeared to be a significant structural difference.
- Attempts to add this route as a small extension to the existing strategy produced limited improvement because it conflicted with legacy scheduling and investment decisions.
- Giving the reconstructed route priority—and removing conflicting legacy behavior where necessary—produced substantially better results.
- The investigation was later narrowed to third-field investment, crop allocation, and rotation decisions.

This process converted replay observations into testable strategic hypotheses. My role was to identify meaningful differences, define the questions to investigate, evaluate the resulting implementations, and reject changes that produced regressions or relied on overly narrow conditions.

The LLM was used as an implementation and analysis assistant rather than as an independent source of strategy.

## Evaluation and Testing

I used a multi-layered evaluation workflow to determine whether changes addressed known weaknesses without sacrificing performance elsewhere.

| Evaluation method | Purpose |
|---|---|
| Recent losing games | Determine whether a candidate addressed weaknesses exposed by the previous version. |
| Historical regression sets | Test against previously recorded games and detect regressions. |
| Open-source opponents | Assess competitiveness against publicly available strategies. |
| Randomized shop simulations | Check whether decisions remained effective across different shop configurations. |
| Kaggle leaderboard submissions | Observe external performance while accounting for matchmaking and result variability. |

### Iterative Validation

The evaluation process generally followed these steps:

1. Compare the candidate directly with its baseline on the same test cases.
2. Inspect early results before committing resources to a full regression run.
3. Trace replays to find where resources, production, score progression, or actions began to diverge.
4. Examine the relevant game state, including cash, inventory, workers, crops, livestock, shop configuration, and remaining production cycles.
5. Test whether the proposed solution improved multiple related cases rather than only one replay.
6. Reject candidates that improved selected losses by weakening established regression sets.

This workflow helped distinguish broadly useful improvements from changes that merely fitted known failure cases.

## Runtime Optimization

The environment provided a per-action time allowance together with a 60-second banked overage budget. Expensive planning steps could consume a large portion of this shared budget and eventually cause the agent to time out.

Execution records showed that several planning stages were particularly expensive, especially around step 288.

### Runtime Improvements

- **Execution profiling:** Inspected JSON execution records to identify decisions that consumed unusually large amounts of the available time budget.

- **Fallback analysis:** An early implementation activated a fallback route when an individual step exceeded a fixed threshold. This proved too conservative: one expensive step did not necessarily mean that the entire game would exceed its budget.

- **Remaining-budget control:** Replaced the single-step rule with logic based on the remaining overall time budget.

- **Strategy preservation:** Adjusted fallback behavior to preserve already completed strategic decisions rather than replacing the production plan with an unrelated route.

- **Threshold testing:** Evaluated different safety thresholds to reduce timeout risk without prematurely abandoning strategically important searches.

### Runtime Evaluation

| Metric | Before optimization | After optimization |
|---|---:|---:|
| Test games | 30 | 30 |
| Timed-out games | 16 | 2 |
| Observed timeout rate | 53.3% | 6.7% |

Across two separate 30-game evaluation batches, the observed timeout rate decreased by 46.7 percentage points.

The two replay formats did not expose identical timing information. The older format recorded consumption of the banked overage allowance, while the newer logs included per-step duration values. Their average runtime values were therefore not directly comparable and were excluded from the table.

Occasional timeouts remained possible because execution performance differed between local testing and the competition environment.

## Key Takeaways

- **Choose development methods empirically.** Under this project's constraints, a heuristic agent built upon existing strategic knowledge outperformed the available RL approach in the internal evaluation.

- **Use focused hypotheses when working with LLMs.** Supplying large numbers of replays without a clear analytical question produced limited value. Progress improved when the investigation focused on specific strategic differences, such as field usage, crop allocation, investment timing, and route conflicts.

- **Prioritize generalization over reactive patching.** Repeatedly countering newly released agents produced temporary gains but also created regressions. Reconstructing broader strategic principles from high-ranking gameplay provided a more sustainable direction.

- **Treat regression testing as part of strategy development.** A change was not considered successful merely because it fixed the replay that motivated it. It also had to preserve established advantages across historical test sets.

- **Treat runtime as part of agent design.** A strategically strong decision is ineffective if it cannot complete within the available execution budget. Runtime safeguards therefore had to preserve both computational safety and route continuity.


## Agent Design

The final agent combines a route-based heuristic policy with state-dependent economic evaluation, calendar-based production planning, and runtime safeguards.

Its decision process can be summarized as:

```text
Observation
    ↓
Normalize the current farm and market state
    ↓
Load the active route and its existing production commitments
    ↓
Evaluate optional investments and crop rotations
    ↓
Compile feasible worker schedules and material flows
    ↓
Apply inventory, funding, and route-continuity checks
    ↓
Return the completed action or activate the runtime safeguard
```

### Route-Based Strategy Layer

The original open-source framework represents major strategies as route plans containing scheduled movement, production, purchasing, and selling actions.

The final agent preserves this route structure instead of generating every action independently. A route provides a stable production foundation, while additional decision layers can repair or extend it when the current state differs from its original assumptions.

The active route influences:

- land and infrastructure investment;
- crop allocation and replanting;
- livestock and feeding schedules;
- worker hiring and task assignment;
- warehouse usage and material transportation;
- the timing of purchases and sales.

This structure helps preserve long production chains that would be easy to break through isolated rule changes.

### State Representation and Decision Inputs

Each decision is based on the current observation rather than replay identifiers or player identities.

The agent evaluates information including:

- current cash and expected funding requirements;
- warehouse inventory and remaining storage capacity;
- owned land, crops, crop ages, and remaining production cycles;
- livestock, feed requirements, fertilizer, and other production inputs;
- available workers and their current positions;
- market prices and unlocked shops;
- previously committed production work;
- the current day, hour, and remaining game duration;
- the remaining execution-time allowance.

These state variables are converted into feasibility and economic checks before a candidate route modification is accepted.

### Calendar-Based Production Planning

Midgame crop changes are evaluated as complete production projects rather than isolated planting actions.

For a proposed project, the planning system considers:

1. which existing crops and tasks must remain protected;
2. when land becomes available;
3. planting, watering, fertilizing, harvesting, and transportation requirements;
4. seed, fertilizer, feed, and inventory dependencies;
5. worker availability and additional payroll;
6. whether the resulting products can be delivered or sold before the game ends;
7. the opportunity cost of replacing the existing route.

The planner compiles these requirements into daily worker schedules. A candidate is rejected if its required work, inputs, funding, or timing cannot be completed.

### Joint Route and Crop-Rotation Evaluation

The final version includes a scoped third-field crop-rotation mechanism.

Instead of treating the new crop project as an independent overlay, the agent evaluates it together with existing work on the same field. Existing feed-dependent harvests and other protected operations remain fixed, while compatible crop tasks may be rescheduled across available workers.

The economic assessment compares the candidate against the original route's investment opportunity. This prevents a proposed rotation from appearing profitable merely because it ignored land, payroll, inventory, or production commitments already present in the baseline strategy.

A project is committed only when:

- the required land is compatible with existing ownership;
- its production calendar is feasible;
- necessary inputs and payroll can be funded;
- it does not overwrite protected route commitments;
- its evaluated value is preferable to retaining the existing plan.

### Action Repair and Continuity Layers

Before returning an action, the agent applies several consistency checks to preserve the production chain.

These checks include:

- repairing planting or building actions when a target tile still requires preparation;
- reserving inventory needed by later actions;
- preventing sales that would remove required production inputs;
- respecting warehouse-capacity constraints;
- preserving worker and material-flow dependencies;
- avoiding conflicting land purchases or crop commitments;
- liquidating eligible terminal inventory when it is no longer required.

These layers modify local actions without replacing the entire active route.

### Runtime Safeguards

Some planning stages—particularly calendar compilation and route allocation—can be computationally expensive.

The runtime controller derives a working deadline from:

- the environment's per-action allowance;
- the remaining banked overage time;
- the time already consumed by the current decision.

Planning checkpoints periodically test this deadline. If the remaining budget becomes too small, the agent stops extending the search.

The safeguard follows two levels:

1. **Completed-plan fallback:** If one or more compatible plans have already been fully compiled, the agent returns a completed plan rather than an interrupted partial result.
2. **Emergency current-state action:** If no completed plan exists, it constructs a lightweight action from the current observation, prioritizing immediately necessary care, safe inventory handling, and executable work.

Random selection, where used, is restricted to fully completed and currently compatible plans. It is not used to select arbitrary routes or identify opponents.

### Implementation Constraints

The deployed agent is self-contained and uses only the Python standard library. Its required modules and strategy data are embedded into one submission file.

The runtime policy does not read:

- local replay files;
- opponent identities;
- episode IDs;
- future actions;
- external strategy tables.

Replay analysis was used during development to form and test strategic hypotheses, but replay-specific information is not part of the deployed decision interface.
