# Validation strategy and the MVP experiment

## Contents
1. The four validation phases (component 9)
2. From Canvas to MVP experiment: hypotheses H1–H4
3. Evaluation metrics
4. Reading results and making decisions
5. Prompting levers for iterations

---

## 1. The four validation phases

| Phase | Question | Tools |
|---|---|---|
| 1. **Offline validation** | Is the AI ready to enter the real workflow? | **Golden dataset** + automated scoring + human review (+ LLM-as-judge as a signal) |
| 2. **Live exposure** | Is it safe with real inputs and users? | **Shadow → Assist → Auto** |
| 3. **Gradual expansion** | Is there enough evidence to expand scope or autonomy? | **Staged rollout** (by category/channel), **canary** (1–5% of traffic) |
| 4. **Ongoing monitoring & impact** | Does it stay good and improve business results? | **Sampling** (quality drift), **feedback loops** (edits, rejections, escalations), **A/B testing** vs baseline — only after stabilization |

- **Golden dataset** — a small, hand-labelled set: typical cases + edge cases + known failure modes; a repeatable baseline for comparing versions. 100 requests in the course. It must reflect the real data distribution, or you get "great on golden, poor in production".
- **LLM-as-judge** scales but inherits the judge's bias — **a signal, not a verdict**.
- **Shadow** — the AI processes real requests, nobody sees the output. **Assist** — suggestions to humans, humans stay in control. **Auto** — no approval, only in narrow scenarios already proven reliable.
- Boundaries: 8 — what "good enough" means; 9 — how to collect evidence; 5 — who gets access and in what order; 2 — which business outcomes must improve.

## 2. MVP experiment: H1–H4

A product definition is a set of assumptions. Before a live pilot, prove that the **core AI capability** works offline. Don't validate everything at once: an impressive prototype is a bad experiment (when it fails you can't tell where it broke). Pick **one small but meaningful capability** — usually the riskiest one, or the one everything else depends on (for Candlekeep: routing with a confidence level, without drafting or RAG).

Hypothesis template (thresholds set **before** results → a decision rule):

| Component | Hypothesis | Metric | Threshold (Candlekeep, for reference) |
|---|---|---|---|
| 8 | **H1 — Quality** | The pattern's primary quality metric (accuracy, groundedness, task success…) | dept. accuracy ≥85% |
| 9 | **H2 — Safety / guardrail** | Unsafe auto-action rate = share of high-confidence answers that are wrong | ≤3% |
| 4 | **H3 — Unit economics** | Projected inference cost at target volume | < $1,000/month at 20,000 messages |
| 8 | **H4 — Speed** | p95 latency | < 5,000 ms |

Adapt H1–H4 to the pattern: for RAG, H1 is groundedness/policy match and H2 is the share of confident answers not backed by a source; for agentic, H1 is task success rate and H2 is irreversible action rate.

What an offline experiment **can** tell you: is it accurate enough, is confidence reliable as a future guardrail, does it fit the cost target, is it fast enough.
What it **cannot**: will users adopt it, how much time the team saves, will satisfaction rise. A controlled pilot answers those.

Process: **Develop → Evaluate → Compare → Decide**.
1. Develop — Prompt v1 on a few dev examples (one per class), one model, low temperature, record the model ID.
2. Evaluate — on the golden dataset; the model never sees gold labels.
3. Compare — against the H1–H4 thresholds.
4. Decide — continue / improve & re-test / stop.

**Never use the evaluation dataset while developing the prompt** — that is data leakage and biases the evaluation.
**Never change expected answers** to make a prompt "pass".

Lightweight playground check (even earlier, before code): a one-line job description → 6–10 real "messy" examples → instructions under ~10 lines → 2–3 models of different sizes, same prompt, low temperature → look at behaviour (grounding, escalation, no invented promises), not just format → a yes / maybe / no decision for a short pilot. A useful test: run the prompt without the policy text — does the model bluff?

## 3. Metrics

| Metric | What it measures |
|---|---|
| Accuracy | Share of correct answers; unreliable with class imbalance (a class < 10% of rows → look at F1) |
| Misroute rate | 1 − routing accuracy |
| F1 per class / macro | Precision–recall balance per class |
| Confusion matrix | Where errors concentrate (often a "default class" under uncertainty) |
| High-confidence rate (coverage) | Share of answers marked High |
| Auto-action precision | Share correct among high-confidence answers |
| Unsafe auto-action rate | ≈ high_conf_rate × (1 − auto_precision); wide coverage with low precision = overconfidence |
| Draft acceptance / edit rate | For content generation |
| Groundedness / policy match | For RAG |
| Task success / irreversible action rate | For agentic |
| p95 / median latency | p95 — UX under load; median — the typical case. Clarify: LLM latency or end-to-end |
| Reliability | % of requests with usable output (timeouts, malformed JSON, API errors) |

Results are non-deterministic: a 1–2 pp difference is noise, rerun; 10+ pp is significant.

## 4. Reading results

- Compare versions in a **controlled comparison**: same model, same data, same schema; change one factor.
- Read deltas in order: quality → safety (does it rise together with quality?) → cost/latency (is the gain proportional?).
- If accuracy ↑ but unsafe ↑, the prompt gives more confident but less reliable answers.
- **The best candidate is the one that passes all predefined criteria**, not the one with the highest accuracy. Course example: the improved prompt (94%, unsafe 3%) beats few-shot (91%, unsafe 7–8%). Combining both is a new version that needs its own evidence.
- A failed baseline is no reason to stop. **Hard stop** only on a structural problem: the task is too ambiguous, the data too noisy, or the model doesn't follow the schema at all.
- Passing H1–H4 ≠ production readiness and ≠ a proven business case. It is the basis for moving to a **controlled pilot**.

## 5. Prompting levers (for the iteration plan)

| Technique | Effect | Trade-off |
|---|---|---|
| Explicit label definitions + mapping | Big accuracy gain | Slightly longer prompt |
| Company/domain context | Reads ambiguous inputs better | Input tokens |
| Key distinctions (edge-case rules) | Targets pairs from the confusion matrix | — |
| Confidence definitions (calibration) | Makes the guardrail meaningful | — |
| Structured output / JSON mode | Reliable format for pipelines | — |
| Few-shot | Accuracy gain (jump at n=8 in the course) | Cost and latency grow linearly; may hurt calibration |
| Grounding + escalation instruction | Against bluffing and over-promising | Needs a source |
| Low temperature | Comparable experiments | — |
