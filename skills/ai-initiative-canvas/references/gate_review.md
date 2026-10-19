# Gate review — checklist before delivering

Go through the list and fix what you find **before** delivering. In the final document's "Gate review" section list only what remains open (risks, unverified assumptions), not the whole checklist.

Use the same list in **Review** mode, when the user brings someone else's canvas, pitch or proposal: for each item found give a quote, why it is a problem, and a corrected formulation.

## A. Sequence and layers
- [ ] Layer 1 (components 1–5) names no models, vendors or infrastructure.
- [ ] The business problem is stated without assuming the answer is AI; a non-AI alternative was considered.
- [ ] One primary financial lever is named.
- [ ] Component 2 contains no AI metrics (accuracy, misroute, latency) — those belong in 8. Component 8 contains no business metrics (FRT, cost per ticket) — those belong in 2.
- [ ] Component 7 Risks lists only AI failure modes, not business/UX/infrastructure risks.
- [ ] Component 6 is written in product language (no JSON, APIs, queues).
- [ ] Layer 3 holds no decisions — only open questions.

## B. Mandatory fields
- [ ] Stop condition in component 2.
- [ ] Unit, breakpoint and an ROI **range** in component 4.
- [ ] Gates in component 5 are measurable (adoption %, quality thresholds), not "the demo went well" or "N months passed".
- [ ] Every component-8 metric has a threshold (or is explicitly marked directional for the pilot).
- [ ] Stop/Rollback in component 9.

## C. Common traps
- [ ] "Benchmarks confirm quality" → benchmarks only give a shortlist; validation happens on your own data.
- [ ] "Accuracy gives the full picture" → system metrics are needed too (latency, reliability, cost).
- [ ] "A newer/bigger model is better" → smallest model that reliably solves the task; predictable beats impressive.
- [ ] "The highest accuracy is the best candidate" → not if it fails the safety/calibration guardrail.
- [ ] "Passed the offline test = production-ready / business case proven" → next comes a controlled pilot.
- [ ] "Inference is the main cost" → for simple tasks the main costs are integration, review, monitoring; for fine-tuning, training.
- [ ] "Web search / tool call on every message" → unnecessary tool calls.
- [ ] "Self-deployment is always cheaper" → only at high stable utilization; proprietary models can't be self-deployed.
- [ ] "Model confidence = quality" → calibration is needed; a confidence score is not a quality metric.
- [ ] "Escalation is a weakness" → it is a safety mechanism.
- [ ] "Use the golden set to tune the prompt" → data leakage.
- [ ] "RAG eliminates hallucinations" → it reduces them.
- [ ] Auto mode or broad rollout from day one → Shadow → Assist → Auto; 2–3 experienced users first.
- [ ] Hiding AI in the UI → violates disclose-AI.
- [ ] Composition "just in case" → start simple, then compose.

## D. Honest and consistent numbers
- [ ] Every number comes from the user's input, from the script's calculation, or is marked `[assumption]`.
- [ ] Repeated numbers match across all sections and derive from the same assumptions.
- [ ] No false precision in ROI.
- [ ] Model prices carry a date and a note that they need verification.

## D2. Your own recommendations pass the same checklist
- [ ] The proposed plan (rollout, timing, experiment) does not repeat the mistake the document criticizes: e.g. no auto mode at the seasonal peak, no audience expansion without measurable gates.

## E. Risks and compliance (see `risk_compliance.md`)
- [ ] Personal data / special categories / data residency are addressed where present.
- [ ] For agentic: approval gates, restricted permissions, audit log, untrusted input.
- [ ] For customer-facing: what happens on a confident mistake in front of a customer.

## Verdict

| Verdict | When |
|---|---|
| **GO → MVP experiment** | Problem and primary lever are clear; pattern defined; economics survive the peak with margin; measurable H1–H4 thresholds exist |
| **REFRAME / NARROW** | Problem is vague, no primary lever, scope too broad (agentic/auto/all users at once), economics marginal, or key data unknown — say what to narrow or find out |
| **NO-GO** | A rule/ordinary software/process change solves it better; or value doesn't cover costs even optimistically; or risk/regulation is unacceptable |

The verdict is about the next step (is the experiment worth the time), not about production.
