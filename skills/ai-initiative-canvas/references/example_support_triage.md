# Illustrative case: customer-support triage assistant

A fictional, generic example. Use it as a model of **level of detail and tone**, not as a content template: another initiative will have a different pattern, thresholds and product shape. All numbers are illustrative.

## Input
A mid-market online retailer. ~15,000 customer messages per month (email, chat, marketplace reviews); 8 support agents sort and answer them manually; ~6 min per message; first response time ~5 h. Delays push some customers to cancel or leave negative reviews. Labor ~$540K/year + estimated lost revenue ~$180K/year = **~$720K/year ≈ $4.00 per message**. Leadership's first idea: "a chatbot that answers customers automatically and cuts support costs by 70%". The Canvas narrows this to an internal assist tool.

## Canvas

| # | Component | Entry |
|---|---|---|
| 1 | Business problem | At ~15,000 messages/month, agents manually read, categorize, route and draft every reply — ~$720K/year and a ~5-hour first response. This matters because volume grows ~20% a year and hiring can't keep up. Target: cut repetitive handling and waiting. Constraint: assist-only first; no AI reply reaches a customer unapproved. |
| 2 | Business metrics | Primary: first-response time ≤1 h (from ~5 h). Secondary: reopen/escalation rate ≤ pre-launch baseline. Timeframe: 10 weeks. Stop: if cost per message rises above the ~$4.00 baseline or reopen rate exceeds baseline +5 pp, pause and rescope. |
| 3 | Value | Primary: For customers waiting ~5 hours for a first reply, we provide a fast, accurate acknowledgement and answer, better than a generic auto-reply, resulting in less waiting and fewer repeat contacts. Secondary: For agents handling ~1,900 messages each per month, we cut sorting and drafting time, resulting in more capacity for complex cases. |
| 4 | Cost structure | Costs: one-time integration + workflow setup; ongoing serving + human review + monitoring. Unit: cost per message (guardrail: ≤ half of the ~$4.00 baseline). Breakpoint: if agents stop reviewing every draft, review cost drops but quality monitoring becomes mandatory. ROI: payback 9–18 months. |
| 5 | Go-to-market | Distribution: 2–3 experienced agents → whole support team → customer-visible scope. Activation: first approved AI draft within the first shift. Gates: ≥70% of pilot agents actively using suggestions; AI quality thresholds hold. |
| 6 | Product shape | Form: panel inside the agent's helpdesk workspace. User: support agents. Workflow point: when a new message arrives, before the agent replies. Output: suggested category, routing destination and reply draft. |
| 7 | AI engine | Approach: Composition (Structured output + Grounded generation). How it works: categorize and route → retrieve the relevant policy when the answer depends on it → draft the reply. Start with / Evolve to: off-the-shelf LLM → a small fine-tuned classifier if routing cost or quality requires. Risks: misrouting; confidently wrong policy statements in drafts. |
| 8 | Solution metrics | Quality: misroute rate ≤10%; draft acceptance ≥60%. Performance: suggestion ready ≤5 s p95; ≥99% valid outputs. |
| 9 | Validation | Offline: golden dataset of ~150 labelled messages, automated scoring + human review of edge cases. Live: shadow → assist once the bar holds on real traffic. Expansion & monitoring: expand by message category; weekly sample review and agent-edit tracking. Stop/Rollback: back to shadow if misroute or unacceptable drafts exceed the bar for a week. |
| 10 | UX | Scenarios: message triage; draft review. Actions: Review / Approve / Edit / Escalate / Handle manually. AI-specific UX: "AI-generated" label; low-confidence flag; one-click override; no auto-send. Privacy: only the order and message data the task needs. |

Why: an **internal triage + draft assistant** (not a customer-facing bot) is consistent with assist-first. Two distinct tasks → two patterns; retrieval only when the answer depends on policy, not on every message. Default: small-model-first routing, escalating hard cases.

## MVP experiment (what to test first)
Scope: routing only — category + department + confidence → JSON (no drafting, no retrieval). Golden dataset of ~150 messages, thresholds fixed in advance.

| Hypothesis | Metric | Threshold |
|---|---|---|
| H1 Quality | Routing accuracy | ≥85% |
| H2 Safety | Unsafe auto-route rate (high-confidence and wrong) | ≤3% |
| H3 Economics | Inference cost at 15,000 messages/month | < $500/month |
| H4 Speed | p95 latency | < 5,000 ms |

A typical iteration story: a bare prompt fails H1 and H2; adding label definitions, key distinctions for commonly confused categories and explicit confidence definitions passes all four; adding few-shot examples raises accuracy further but worsens calibration (H2 fails). Carry forward the version that passes **all** thresholds, not the one with the highest accuracy. Next step: a controlled pilot with 2–3 agents.
