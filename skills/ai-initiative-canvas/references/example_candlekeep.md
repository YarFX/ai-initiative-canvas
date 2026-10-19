# Reference case: Candlekeep Retail Group (the course's running case)

Use it as a model of **level of detail and tone**, not as a content template: another initiative will have a different pattern, thresholds and product shape.

## Input
Mid-market home-goods retailer. 20,000 customer messages per month (email, chat, social, reviews); 10 support FTEs sort and answer them manually; ~5 min per message; first response time ~4 h; 12,000 customers a year hit delays → −15% satisfaction in that segment. Labor $672K/year + lost revenue $306K/year = **$978K/year ≈ $4.10 per message**. Leadership's initial "AI hypothesis": automate 80% of sorting, −70% costs, FRT under 2 seconds — the Canvas brought these ambitions down to earth.

## Canvas

| # | Component | Entry |
|---|---|---|
| 1 | Business problem | At 20,000 messages/month, support manually reads, categorizes, routes, and drafts — costing ~$978K/year and causing 4-hour first response. This matters as volume grows. Target: reduce repetitive work and delays. Constraint: assist-only first. |
| 2 | Business metrics | Primary: first-response time ≤30 min (from ~4 h). Secondary: escalation rate ≤ pre-launch baseline. Timeframe: 12 weeks. Stop: if cost per request rises above baseline (~$4.10), pause and rescope. |
| 3 | Value | Primary: For customers with 4.2-hour response delays, we provide immediate, personalized acknowledgment, better than generic templates, resulting in less uncertainty and waiting. Secondary: For support agents handling 10K+ monthly messages, we cut categorization time, better than manual workflows, resulting in more capacity for complex cases. |
| 4 | Cost structure | Costs: one-time integration + workflow setup; ongoing serving + human review + monitoring. Unit: cost per message (guardrail: ≤ half of the $4.10 baseline). Breakpoint: volume/context growth → shift serving approach. ROI: payback 12–18 months. |
| 5 | Go-to-market | Distribution: 2–3 experienced support specialists → full support team → customer-visible scope. Activation: first approved AI draft within the first shift. Gates: ≥70% of pilot specialists actively using suggestions; no opt-outs; AI quality thresholds hold. |
| 6 | Product shape | Form: support specialist workspace. User: support specialists. Workflow point: when a new customer message arrives, before the specialist responds. Output: suggested category, routing destination, response draft. |
| 7 | AI engine | Approach: Composition (Structured output + Content generation + Grounded generation). How it works: categorize and route → decide whether current policy knowledge is needed → retrieve relevant policy when required → generate draft. Start with / Evolve to: off-the-shelf LLM → custom classifier if quality or cost requires. Risks: misrouting; confident wrong drafts. |
| 8 | Solution metrics | Quality: misroute rate ≤10%; draft acceptance ≥60%. Performance: routing latency fast enough to improve FRT (directional for pilot). |
| 9 | Validation | Offline: 100-sample golden dataset, automated evaluation + human edge-case review. Live: shadow → assist after the quality bar holds on real messages. Expansion & monitoring: expand by message category; review sampled outputs and specialist corrections. Stop/Rollback: pause or roll back if quality or performance falls below the bar. |
| 10 | UX | Scenarios: message triage; draft review. Actions: Review / Approve / Edit / Escalate / Handle manually. AI-specific UX: label AI-generated suggestions; flag low-confidence; override or continue manually; no auto-send. Privacy: only task-required customer data; transparent AI data use. |

Why: the chosen form is a **triage + first-response assistant** for specialists (not a customer-facing bot) — consistent with assist-first. Three distinct tasks → three patterns; RAG only when the answer depends on the current policy, not on every message. Default: small-model-first routing with escalation of hard cases.

## MVP experiment (what was tested first)
Scope: routing only — category + department + confidence → JSON (no drafting, no RAG). Golden dataset of 100 requests.

| Hypothesis | Threshold | Baseline prompt | Prompt v1 | Improved prompt | Few-shot n=8 |
|---|---|---|---|---|---|
| H1 dept. accuracy | ≥85% | 55% ❌ | 86% ✅ | **94% ✅** | 91% ✅ |
| H2 unsafe auto-route | ≤3% | 25% ❌ | 10% ❌ | **3% ✅** | 7–8% ❌ |
| H3 cost / month (20K) | < $1,000 | $2.4 ✅ | $2.3 ✅ | $2.9 ✅ | $3.9–4.6 ✅ |
| H4 p95 latency | < 5,000 ms | 1.4 s ✅ | 1.1 s ✅ | 1.1 s ✅ | 1.1–1.2 s ✅ |

Model: openai/gpt-oss-120b on Nebius Token Factory (picked on a 30% sample from 4 candidates). Decision: carry forward the **improved prompt** (passes all 4), not few-shot, which had higher accuracy in some runs but failed H2. Next step: a controlled pilot.
