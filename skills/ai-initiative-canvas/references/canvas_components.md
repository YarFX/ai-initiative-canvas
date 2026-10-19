# AI Product & System Canvas — components 1–10

Method from the Nebius Academy "AI Leader" course (Canvas author: Mikhail Rozhkov, inspired by Osterwalder's Business Model Canvas).
15 components in 3 layers; the skill fills layers 1–2 and lists only open questions for layer 3.

| Layer | Question | Components |
|---|---|---|
| 1. Business foundation | **WHY** — why build it, which problem, how we'll know it worked | 1 Business problem · 2 Business metrics · 3 Value for customers · 4 Cost structure · 5 Go-to-market |
| 2. Product blueprint | **WHAT** — which product, how it should behave | 6 Product shape · 7 AI engine · 8 Solution metrics · 9 Validation strategy · 10 User experience |
| 3. AI system design | **HOW** — implementation and operations | 11 Data pipelines · 12 MLOps · 13 Compute · 14 Deployment & serving · 15 Monitoring |

**Decision cascade**: early decisions constrain later ones; mistakes compound. The most common reason AI projects fail is an inverted sequence (model and infrastructure first, then "does this solve the problem?"). So layer 1 never names models, vendors or infrastructure. The process is iterative: components 7–8 may force a revisit of layer-1 economics and gates.

Layer 3 is not filled in up front for two reasons: these are technical decisions made together with engineers, and the key assumptions are still hypotheses that the MVP experiment must test first.

---

## Contents

1. Business problem
2. Business metrics
3. Value for customers
4. Cost structure
5. Go-to-market strategy
6. Product shape
7. AI engine
8. Solution metrics
9. Validation strategy
10. User experience
11–15. Layer 3: what to list as open questions

---

## 1. Business problem

**Purpose**: describe the real business problem or opportunity **without assuming the answer is AI**.

Include:
- **scale** — volume (messages/documents/users per month);
- **current workflow** — who does what today;
- **pain / cost / risk** — direct and indirect losses;
- **why now** — growth, SLA, seasonality, regulation, competitors;
- **target outcome** — in business language;
- **key constraint** — safety, compliance, brand, latency, cost.

Name **one primary financial lever** out of four: revenue growth · capital efficiency · cost reduction · risk reduction. If you cannot name one, the business case is not yet clear — that is a finding in itself.

**Format**: `At ~[scale], [current workflow] causes [pain/cost/risk]. This matters because [why now]. Target: [outcome]. Constraint: [limit/guardrail].`

Example (Revolut): "At ~millions of interactions/month, manual support and risk review workflows create delays, high operational cost, and increased error risk. … Constraint: strict compliance and risk control" — the problem is clear, no model is named.

Checks:
- "If we do nothing for 6 months, what gets worse, and where does it show up in money, time or risk?"
- Would a new stakeholder understand the problem in one read? If not, add one number and one real consequence.
- Could a rule, regex, ordinary software or a process change solve it? If so, say so; AI is not mandatory.

## 2. Business metrics

Separate **business outcomes** (what the organization already tracks: cost per ticket, response time, churn, revenue protected) from **model performance** (accuracy, latency → component 8).

Include: 2–3 primary outcomes · success thresholds (minimum viable improvement) · timeframe (pilot vs sustained) · **stop condition** · 1–2 secondary outcomes (satisfaction, adoption, compliance).

**Format**: `Primary: [metric ≥/≤ threshold]; Secondary: [metric ≥/≤ threshold]; Timeframe: [weeks]; Stop: if [condition] by [date], then [pause/rescope].`

Layer test: could the primary metric appear in a weekly operations report unrelated to AI? Yes → layer 1. If you need AI context to understand it → component 8. "Routing accuracy ≥85%" in component 2 is a **layer error**.

Without a stop condition a pilot runs forever — it is a mandatory field.

## 3. Value for customers

Two groups: **stakeholders** (approve and fund) and **users** (whose work actually changes). A common mistake is designing for stakeholders and forgetting users. Pick **one primary audience**; the other can be secondary.

**Feature ≠ value**. A feature is what the product does ("classifies and summarizes"). Value is what improves ("the team spends less time on manual triage"). Describe it in workflow terms. If the text would fit a product spec, it belongs in layer 2.

Include: primary user · pain in workflow terms · delivered value · **current alternative** · measurable benefit.

**Format**: `For [user] with [problem], we provide [specific value], better than [current alternative], resulting in [measurable benefit].`

Example (Shopify Sidekick): "For merchants with complex admin tasks and limited time, we provide faster insights and actions through simple requests, better than manual reports and navigation, resulting in faster decisions and lower operational overhead."

## 4. Cost structure

Details and formulas — `economics_and_models.md`. Here — what to write down.

Four steps:
1. **Where the money goes** — one-time (integration, data preparation, workflow redesign) · ongoing fixed (human review, monitoring, iteration cadence; grows as a **step function**) · ongoing variable (serving, training/fine-tuning, labeling, tool and retrieval calls).
2. **Unit** — the unit the business already uses to measure the process: cost per message / per user / per document.
3. **Breakpoint** — the threshold beyond which growth **changes the structure** of costs rather than just increasing them (the review team can no longer keep up; load justifies a dedicated endpoint).
4. **ROI guardrail** — a boundary, not a forecast: max cost per interaction, payback range, savings range.

**Format**: `Costs: [one-time drivers] + [ongoing drivers]; Unit: [$/interaction or $/user]; Breakpoint: [trigger → cost structure change]; ROI: [payback range] / [savings or revenue range].`

Traps: false precision ("$45K, payback 9 months" with no data); treating serving as the only variable cost; missing that for simple routing/classification inference is a small share and the main costs are integration, human review and monitoring.

## 5. Go-to-market strategy

AI fails in non-obvious ways (confidently wrong), so AI products are rarely launched to everyone at once. Rollout expands two different things:
- **Audience** (how many people) — component 5, a business decision;
- **Autonomy** (how much control the AI has) — component 9, a quality decision.

Every expansion is based on evidence, not on how good a demo looked.

Include: **Distribution** (who goes first, cohort sequence) · **Activation** (what "first value" looks like and how fast) · **Gates** (adoption/business thresholds + quality evidence from component 9).

**Format**: `Distribution: [cohort 1] → [cohort 2] → [broad]; Activation: [first value in X time]; Gates: [adoption/business thresholds] + Component 9 quality evidence holds.`

First cohort — **2–3 experienced specialists**: they catch confident-but-wrong output, give useful feedback, become champions and limit the damage. Not the whole team, and not juniors.
Good gates: "≥70% of pilot specialists actively use suggestions" + "AI quality thresholds met". Bad ones: "leadership liked the demo", "two months have passed".

---

## 6. Product shape

One business goal → different product forms. The classic choice: customer-facing bot vs **internal assist tool** (a specialist approves suggestions). Assist-first limits exposure and makes errors easier to contain; with high stakes and unproven quality it is the default.

Four elements: **Form** (embedded feature / assistant / API / workflow step) · **User** (who interacts directly) · **Workflow point** (where it enters their work — a place, not a sequence) · **Output** (draft, label, summary, recommendation).

**Format**: `Form: [where it lives]; User: [who interacts]; Workflow point: [where it enters their work]; Output: [what it provides].`

Test: would this entry fit a product brief read by non-engineers? "Suggested category and response draft" — product (6). "Classify the message and generate a draft" — AI logic (7). APIs, queues, JSON — layer 3.

## 7. AI engine

The starting point is the chosen architecture pattern (`architecture_patterns.md`). Describe the AI approach at product level, without model names, vendors or APIs.

Include: **Approach** (pattern) · **How it works** (one end-to-end sentence) · **Start with / Evolve to** (off-the-shelf → custom if quality or cost requires) · **Risks** (1–3 failure modes of the AI itself).

**Format**: `Approach: [pattern]; How it works: [one sentence]; Start with / Evolve to: [off-the-shelf] → [custom later, if …]; Risks: [top 1–3 AI failure modes].`

Risks here are only AI failure modes (misrouting, confident wrong draft, wrong action). Not here: business failure ("FRT didn't improve"), UX risks ("over-reliance"), infrastructure ("vector DB downtime").

## 8. Solution metrics

Two kinds of signal:
- **Quality** (output-level) — the pattern's primary metric (table in `architecture_patterns.md`);
- **System performance** (system-level) — **latency** (does it fit the moment in the workflow), **throughput** (critical when moving to production), **reliability** (% of requests with usable output: timeouts, malformed responses, API failures — separate from quality errors). Include only those that can actually break the product.

A metric without a threshold is useless: "misroute rate" says what to measure; "misroute rate ≤8%" says what we will accept. Thresholds give GO / PAUSE. Directional targets are fine in a pilot and get replaced with numbers later.

**Format**: `Quality: [metric ≥/≤ threshold]; Performance: [latency / throughput / reliability thresholds].`

Latency reference points (NN/g, RAIL): ~0.1 s feels instant; ~1 s keeps flow; ~10 s risks losing attention.

Mistakes: putting business outcomes here (FRT, support cost belong in component 2); using a "model confidence score" as a quality metric (it is not quality; calibration is needed).

## 9. Validation strategy

How to collect evidence against the component-8 bar. Details — `validation_and_experiments.md`.

Four phases: Offline validation → Live exposure (**Shadow → Assist → Auto**) → Gradual expansion (staged rollout, canary 1–5%) → Ongoing monitoring & impact (sampling, feedback loops, A/B after stabilization).

**Format**: `Offline: [golden dataset + evaluation]; Live: [initial exposure]; Expansion & monitoring: [gate + ongoing evidence]; Stop/Rollback: if [condition], then [action].`

Mistakes: auto mode from day one; assist on all categories at once; LLM-as-judge as a verdict (it is a signal).

## 10. User experience

| | Component 6 | Component 10 |
|---|---|---|
| Question | Where is the product in the work? | How does the user interact with it? |
| Defines | Form, user, workflow point, output | Scenarios, actions, controls, feedback, fallback |

Layer 1 — **scenarios and primary actions** (interface verbs: Review, Approve, Edit, Escalate, Revert) — visible and unambiguous.
Layer 2 — **AI-specific UX**, three principles:
1. **Disclose AI** — an "AI-generated" label next to the content;
2. **Human override** — correct, reject, escalate as first-class actions; discard-only is not recovery;
3. **Privacy by default** — only the data the task needs; transparency.
Plus **uncertainty**: a low-confidence flag ("please verify").

**Format**: `User scenarios: [2–3]; Primary actions: [verbs]; AI-specific UX: [disclosure + control + uncertainty]; Privacy: [data minimisation + transparency].`

Mistakes: auto-approval at confidence >80% (that is an autonomy decision, component 9); hiding AI "to keep the UI clean"; passing the full customer profile; storing everything for training without consent.

---

## 11–15. Layer 3 (HOW) — open questions only

Do not fill these with decisions. List questions to discuss with engineers:
- 11 Data pipelines — sources, storage, knowledge base update cadence;
- 12 MLOps — experimentation and evaluation tooling;
- 13 Compute infrastructure — cloud services, team composition;
- 14 Deployment & serving — API vs dedicated vs self-hosted, CI/CD;
- 15 Monitoring — metrics, alerts, who responds.
