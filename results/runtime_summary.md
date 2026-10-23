# Runtime verification

## Initialization-only guard

- Standalone import and callable-agent smoke test: passed.
- External workspace reads during the isolated smoke test: none detected.
- Saved source SHA-256:
  `da569ba096414f21b05134c0b8b61e07e473793b8afd8f60011dc98a4b32530d`.
- Normal-budget paired comparisons: 32.
- Recorded normal-budget behavior: all 32 had identical actions, states and
  scores relative to the reference.

Two artificial low-time tests completed within the local official-time model,
but produced severe score losses. Therefore the guard provides only a legal
last-resort action path. It is not an online timeout guarantee and is not a
score-preservation guarantee.

## Joint accelerated25

The version uses a shared 25-second internal planning budget at step 288 and
retains the later optional-search safety mechanism. Its saved validation covers
31 frozen-opponent paired games. Timing behavior can vary with hardware and
server load, so this result must not be interpreted as a universal runtime
guarantee.

