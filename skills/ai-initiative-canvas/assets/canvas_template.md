# [Initiative name] — AI Initiative Canvas

*[Date] · Mode: [Full / Quick / Wizard / Review] · Data source: [what the user provided]*

## Verdict
**[GO → MVP experiment / REFRAME / NO-GO]** — [one or two sentences: why, and what to do next].

Key numbers: [current unit cost] → [projected AI inference per unit] · [primary business metric and target] · [main risk].

## Assumptions and open questions
| # | Assumption | Why it matters | How to verify |
|---|---|---|---|
| A1 | … | … | … |

## Layer 1 — Business foundation (WHY)
**1. Business problem.** At ~[scale], [current workflow] causes [pain/cost/risk]. This matters because … Target: … Constraint: …
*Primary lever:* [revenue growth / capital efficiency / cost reduction / risk reduction].

**2. Business metrics.** Primary: … Secondary: … Timeframe: … Stop: if … then …

**3. Value for customers.** For [user] with [problem], we provide [value], better than [current alternative], resulting in [measurable benefit].

**4. Cost structure.** Costs: … + … ; Unit: … ; Breakpoint: … → … ; ROI: …

**5. Go-to-market.** Distribution: … → … → … ; Activation: … ; Gates: … + Component 9 quality evidence holds.

## Architecture pattern
**[Pattern]** — [why this one under "simplest pattern that fits"; why not the neighbouring ones].

## Layer 2 — Product blueprint (WHAT)
**6. Product shape.** Form: … ; User: … ; Workflow point: … ; Output: …

**7. AI engine.** Approach: … ; How it works: … ; Start with / Evolve to: … → … ; Risks: …

**8. Solution metrics.** Quality: … ; Performance: …

**9. Validation strategy.** Offline: … ; Live: … ; Expansion & monitoring: … ; Stop/Rollback: if … then …

**10. User experience.** User scenarios: … ; Primary actions: … ; AI-specific UX: … ; Privacy: …

## Inference economics
[Table from scripts/token_cost.py: model, $/request, $/month, $/year, % of current unit cost.]
[Conclusion: inference's share of total costs; which cost items really matter.]
*Prices as of [date]; verify before deciding.*

## Model and deployment
- Shortlist for the experiment: [frontier bar] + [2–3 smaller/cheaper candidates].
- Selection rule: among candidates passing all thresholds — …
- Deployment: [API / dedicated / serverless / self-hosted] — because …; revisit when: …

## Next step: MVP experiment
Capability to test: [the riskiest/most foundational part]. In scope: … Out of scope: …

| Hypothesis | Metric | Threshold |
|---|---|---|
| H1 Quality | … | … |
| H2 Safety | … | … |
| H3 Unit economics | … | … |
| H4 Speed | … | … |

Golden dataset: [size, source, who labels it, which edge cases]. Decision rule: [continue / improve & re-test / stop].

## Risks and compliance
- …

## Gate review — still open
- …

## Layer 3 (HOW) — questions for engineers
- Data pipelines: …
- MLOps: …
- Compute: …
- Deployment & serving: …
- Monitoring: …
