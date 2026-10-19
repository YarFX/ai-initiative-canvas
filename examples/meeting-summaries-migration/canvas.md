# Call summaries & action items: move LLM step to open models? — AI Initiative Canvas

*2026-10-19 · Mode: Full (unattended, missing facts marked `[assumption]`) · Data source: user's message (1,500 audio hours/month, AssemblyAI for transcription, GPT-4o for summaries, ~120 paying users at $15/month)*

## Verdict
**REFRAME → GO on a 1–2-week offline bake-off. Not on a migration yet.** As a cost move, switching the summary step from GPT-4o to an open model saves about $60/month (~3% of MRR). Transcription costs roughly 3–9× more than the LLM step and stays with AssemblyAI either way. No one has shown that fine-tuning is needed yet, and it would need customer consent for training data. Reframe the goal from "move to Token Factory" to "same or better summaries and action items at lower cost per subscriber, with an EU zero-retention option". Because the API is OpenAI-compatible, the switch itself is cheap. Run a bake-off on a 60-call golden set and migrate only if an open model is non-inferior to GPT-4o on action items. Leave fine-tuning out until a failure mode shows up that prompting can't fix.

Key numbers: revenue ~$1,800/month (~$0.90 per call) · GPT-4o ≈ $65/month (3.6% of revenue) → gpt-oss-120b ≈ $4/month · transcription ≈ $225–555/month `[assumption]`, the largest variable cost · main risk: invented or misattributed action items (wrong owner or deadline).

## Assumptions and open questions
| # | Assumption | Why it matters | How to verify |
|---|---|---|---|
| A1 | Average call is ~45 min, so ~2,000 calls/month | Sets the per-call unit and token volume | Count jobs in your DB for last month |
| A2 | ~12K tokens per audio hour (mostly English, ~150 wpm), so ~9,000 transcript + 800 system + 800 output tokens per call | Drives all LLM costs. Russian or other non-English calls need ~1.6× the tokens | Log `usage` from 50 real GPT-4o calls |
| A3 | GPT-4o at $2.50 / $10 per 1M tokens, with no batch or caching used today | Baseline LLM cost | Your OpenAI invoice for last month |
| A4 | AssemblyAI at ~$0.15–0.37 per audio hour (depends on plan and add-ons such as diarization) | Shows transcription is the main variable cost | Your AssemblyAI invoice |
| A5 | You would not replace AssemblyAI with an ASR model from the Token Factory catalog, so transcription stays where it is | The migration then touches only the smaller cost line | Check the Token Factory catalog for speech models. Self-hosted Whisper is a separate decision |
| A6 | No data yet links summary quality to churn or complaints | Without it, the "better quality via open models / fine-tuning" lever is unproven | Tag support tickets and cancellation reasons for 4 weeks. Add a thumbs up/down to summaries |
| A7 | Some customers are in the EU, so GDPR applies to recordings of all call participants | Adding a sub-processor triggers ToS/DPA obligations. Training on calls needs consent | Customer country breakdown; current ToS and sub-processor list |
| A8 | Migration plus eval harness plus golden-set labelling takes 3–6 dev-days | This is the real cost of the move | Time-box the bake-off |

## Layer 1 — Business foundation (WHY)

**1. Business problem.** About 1,500 audio hours a month (~2,000 calls `[A1]`) from ~120 paying small teams go through a two-step pipeline: transcription, then summary and action items. At a flat $15/month, cost per subscriber is ~$2.4–5.2 (16–35% of the price), mostly transcription. Margin depends on the heaviest users and on being locked to a single proprietary vendor for summaries. This matters now because usage grows with each team's meeting load while revenue per subscriber stays flat, and model choice and fine-tuning are the levers that could set the product apart. Target: keep or improve the quality of summaries and action items while lowering and controlling cost per subscriber. Constraint: call recordings contain personal data of every participant, including non-users. Customer data must not be used for training without consent.
*Primary lever:* **cost reduction (gross margin per subscriber)**. It is the only lever you can measure today. On the summary step it is small (~$60/month), so this is a finding in itself: the move pays off only if it is cheap or if it unlocks a revenue lever (quality-driven retention, EU-residency customers) that has no evidence yet `[A6]`.
*Non-AI alternatives considered:* a fair-use cap or per-hour tier for heavy users protects margin more than any model swap. OpenAI's own Batch API or a cheaper OpenAI model cuts the LLM bill without migrating (see economics).

**2. Business metrics.** Primary: AI cost of goods sold (COGS) per subscriber ≤ 25% of the price (≤ $3.75/month). Monthly churn ≤ current baseline. Secondary: support tickets about summaries ≤ baseline; share of users who open summaries ≥ baseline. Timeframe: bake-off 2 weeks → shadow 2 weeks → canary 4 weeks. **Stop:** if by the end of the bake-off (week 2) no open candidate meets H1–H2, stay on GPT-4o (optionally with batch or a cheaper OpenAI model) and revisit in 6 months. If churn or summary complaints rise above baseline during the canary, roll back to GPT-4o.

**3. Value for customers.** Primary audience is the users: team members who need to know what was decided. *For small-team members who leave a call with commitments scattered across a 45-minute conversation, we provide a short summary and an action list with owner and due date that they can trust without re-listening. That beats taking notes by hand or re-watching the recording, and it means fewer dropped follow-ups and minutes saved per call.* For you as the founder (stakeholder), the value of the migration is vendor optionality and margin headroom, not something users will notice. If users can tell the engine changed, that should only be because quality went up.

**4. Cost structure.** Costs: one-time migration (provider abstraction, prompt adaptation for the new model, eval harness, golden-set labelling: 3–6 dev-days `[A8]`) + ongoing fixed (re-running evals on every model or prompt change, quality sampling, sub-processor/ToS upkeep) + ongoing variable (transcription ~$225–555/month `[A4]`, LLM ~$65/month today, storage, and periodic training runs if fine-tuning is ever adopted). Unit: COGS per subscriber per month (now ~$2.4–5.2), guardrail ≤ $3.75. Breakpoint: (a) heavy users. At ~$0.19–0.41 COGS per audio hour, any subscriber above ~18–39 hours/month costs more than half their $15 fee, against an average of ~12.5 h. (b) At ~10× volume, the transcription bill is large enough to justify evaluating self-hosted ASR or a dedicated endpoint. ROI: switching the LLM saves ~$50–60/month (~$600–720/year). Valuing 3–6 dev-days at `[assumption]` $50/h, cash payback on cost alone is ~1.7–3.7 years. Speed of switching is the only thing that makes the case.

**5. Go-to-market.** Distribution: your own team's calls → 5–10 opt-in power users ("new summary engine" beta flag) → 20% canary → everyone. Activation: the beta user's next call produces a summary from the new engine within minutes of the call ending. Gates: beta users' thumbs-up rate and action-item edit rate within 5 pp of their own GPT-4o history; no rise in summary-related tickets; Component 9 quality evidence holds.

## Architecture pattern
**Content generation (pattern 2) with a structured (JSON) action-item section.** Everything the model needs is already in the transcript, so there is no source of truth to retrieve (not RAG). It drafts text and calls no tools (not agentic). Summary and action items come from one input in one call, so splitting them into a Composition would add complexity without a real boundary. If you later push action items into Jira, Asana or Linear automatically, that step becomes agentic and needs its own approval gate.

## Layer 2 — Product blueprint (WHAT)

**6. Product shape.** Form: the existing post-call recap (web app + email/Slack notification). User: members of the team that recorded the call. Workflow point: right after the call ends, when people decide who does what next. Output: short summary, decisions, and action items with owner, due date and a link to the transcript moment. The migration does not change the shape, only the engine behind it.

**7. AI engine.** Approach: content generation with structured action-item output. How it works: the transcript with speaker labels goes in, and one generation pass returns a summary, decisions and action items, each tied to a timestamp. Start with / Evolve to: a prompt-tuned open-weight model (same prompt family as today) → LoRA fine-tune only if a specific failure mode (e.g., missed implicit commitments, domain jargon) survives prompt iteration *and* a consented training set exists. Risks: invented or misattributed action items (wrong owner or deadline); dropped commitments; quality loss on long, crosstalk-heavy or non-English calls.

**8. Solution metrics.** Quality: action-item recall ≥ 90% and precision ≥ 85% against the gold labels. Owner and due-date correct on ≥ 90% of matched items. Summary judged "as good or better than GPT-4o" in ≥ 80% of blind pairwise comparisons. Performance: p95 time from transcript ready to summary ≤ 60 s for a 1-hour call (asynchronous, so throughput matters more than milliseconds). Reliability: ≥ 99% of outputs are valid JSON on the first attempt.

**9. Validation strategy.** Offline: a golden set of 60 calls (see MVP), scored automatically on action items plus a blind human pairwise review of summaries. LLM-as-judge is only a signal. Live: summaries are already delivered without review today ("Auto"), so live exposure for a *new engine* goes **shadow** (the open model runs in parallel on real calls, users never see its output; compare with GPT-4o on edit and recall proxies) → **canary** to beta users with GPT-4o one flag away. Expansion & monitoring: 20% → 100% gated by component 5. Weekly review of 10 sampled calls, with edit, regenerate and thumbs-down signals tracked against the GPT-4o baseline. Stop/Rollback: if the action-item edit rate or thumbs-down rate is more than 5 pp above baseline for a week, or the JSON failure rate exceeds 1%, flip the flag back to GPT-4o. Keep GPT-4o wired as a fallback for 30 days.

**10. User experience.** User scenarios: read the recap after a call; fix an action item; share the recap with the team. Primary actions: Review, Edit item, Reassign owner, Mark done, Jump to transcript, Regenerate, Report a problem. AI-specific UX: an "AI-generated" label on recaps; every action item links to its transcript timestamp as evidence; "owner unclear" / "no date mentioned" flags instead of guessed values; thumbs up/down per recap. Privacy: send only the transcript and speaker names to the LLM, no account or billing data. Use zero-retention inference. Train on customer calls only with explicit opt-in.

## Inference economics
Calculated with `token_cost.py`: 2,000 calls/month, 9,000 transcript + 800 system + 800 output tokens per call `[A1–A2]`. "Current unit" means revenue per call (~$0.90).

| Model | $ in / out per 1M | $ per call | $ / month | $ / month at 2× volume | $ / year | % of revenue per call |
|---|---|---|---|---|---|---|
| GPT-4o (current) `[A3]` | 2.50 / 10 | $0.033 | $65 | $130 | $780 | 3.6% |
| Frontier bar (Oct 2026 tier) | ~10 / ~50 | $0.14 | $276 | $552 | $3,312 | 15.3% |
| gpt-oss-120b (Token Factory) | 0.15 / 0.60 | $0.002 | $3.90 | $7.80 | $47 | 0.2% |
| Nemotron-3.5-Lightning (Token Factory) | 0.06 / 0.24 | $0.0008 | $1.56 | $3.12 | $19 | 0.1% |
| GPT-4o-mini (no migration) `[assumption: price]` | 0.15 / 0.60 | $0.002 | $3.90 | $7.80 | $47 | 0.2% |

Sensitivities: with mostly Russian calls (~15K transcript tokens, 1,300 output) GPT-4o rises to ~$105/month and gpt-oss-120b to ~$6. Sending all summaries through batch halves either bill (GPT-4o ~$32.50/month), but a ≤24 h window does not suit "recap right after the call".

**Conclusion:** the LLM step is about 3.6% of revenue, and an open model brings it down to about 0.2%: a real but small ~$60/month. Transcription (~$225–555/month, 12–31% of revenue `[A4]`) and heavy users matter more for margin than the model choice. The LLM saving can also be had without leaving OpenAI. That makes the real arguments for Token Factory **model choice beyond one vendor, EU data centers with zero retention, and a path to fine-tuning and hosting your own weights**. Each of these has value only if you can show it is needed. Fine-tuning would add training-run costs that can exceed serving costs many times over and recur with data drift. *Prices as of October 2026 (Token Factory, frontier tier) and `[assumption]` for OpenAI and AssemblyAI; verify on the official pages and your invoices before deciding.*

## Model and deployment
- **Shortlist for the bake-off:** GPT-4o (current production = quality bar) · gpt-oss-120b · one larger open instruct model from the Token Factory catalog with strong long-context and multilingual results (e.g., a Qwen or Llama 70B+ class model) · Nemotron-3.5-Lightning (cheap tier, to see where quality breaks) · GPT-4o-mini as the no-migration control. Benchmarks only pick the shortlist; your golden set decides.
- **Selection rule:** among candidates that pass all H1–H4 thresholds, pick the one with the higher action-item quality, then fewer unsupported items, then lower cost, then lower latency. If only GPT-4o passes, stay.
- **Deployment:** API / pay-per-token on Token Factory (Base flavor; the work is asynchronous), EU region with zero-retention. Same-class alternatives: Together AI, Fireworks, AWS Bedrock, or staying on OpenAI. Revisit if volume grows ~10× (dedicated endpoint for predictable latency) or if a fine-tuned model is adopted (hosted LoRA). Self-hosting the LLM makes no sense at ~$4/month of tokens.

## Next step: MVP experiment
**Capability to test:** action-item extraction (owner, task, due date, timestamp) plus summary from an existing transcript. This is the part users act on, and the riskiest part for a smaller model. In scope: the LLM step only, on stored AssemblyAI transcripts, English and one secondary language if you have one. Out of scope: transcription changes, fine-tuning, integrations, UI changes.

| Hypothesis | Metric | Threshold (set before running) |
|---|---|---|
| H1 Quality | Action-item recall / precision vs gold; blind pairwise summary preference vs GPT-4o | Recall ≥ 90%, precision ≥ 85%; "as good or better" ≥ 80% of pairs |
| H2 Safety | Unsupported action items: owner, deadline or commitment not stated in the transcript | ≤ 3% of extracted items, and no worse than GPT-4o |
| H3 Unit economics | LLM cost per call at measured tokens | ≤ $0.01 per call (≤ $20/month at 2,000 calls) |
| H4 Speed & reliability | p95 generation time for a 1-hour call; valid JSON on first attempt | ≤ 60 s; ≥ 99% |

**Golden dataset:** 60 calls. Take ~30 from your own team or customers who explicitly opt in, plus ~30 from public meeting corpora with human annotations (e.g., AMI/ICSI) to cover crosstalk without any consent question. You label them yourself from the transcript, not from GPT-4o's output, to avoid baking in its bias: ~20–30 min per call, ~25 hours total. Include edge cases: calls with no action items, implicit commitments ("I'll look into it"), reassigned tasks, relative dates ("by next Friday"), 2-hour calls, heavy crosstalk or ASR errors, mixed-language calls, misrecognized names. Keep a separate 10-call dev set for prompt work. Never tune on the 60.
**Decision rule:** all of H1–H4 pass → shadow, then canary. H1 or H2 fails by ≤ 10 pp → one round of prompt work (label definitions for "commitment", owner and date rules, explicit "unclear" output), then re-test. A structural failure (e.g., systematic owner errors on multi-speaker calls) → stay on GPT-4o and log this as the concrete failure mode a fine-tune would have to fix.

## Risks and compliance
- **Personal data of every participant**, including people who never signed up. Calls may touch special categories (health in HR calls, etc.); check that the provider allows that, and keep zero-retention on.
- **New sub-processor:** adding Token Factory means updating the privacy policy and sub-processor list, notifying customers as your ToS requires, and signing a DPA. EU data centers (Finland, France) plus zero-retention are a selling point for EU teams. Compare them against OpenAI's own residency and retention options before treating this as a differentiator.
- **Fine-tuning on customer calls** needs explicit opt-in and a ToS change. Until then use public corpora, your own calls and synthetic data. Check model and provider terms before training on another model's outputs (distillation).
- **Confident mistake in front of the customer:** a wrong owner or invented deadline leads to missed follow-ups and lost trust in the product. Timestamp evidence and "unclear" flags are the mitigation.
- **Untrusted input:** anything said on a call is input to the model ("ignore previous instructions…"). The impact is low while output is a recap. It becomes an action risk once items are pushed into task trackers automatically.
- **EU AI Act:** likely limited risk (disclose AI-generated content). It would move toward high risk if recaps were used to evaluate employees, so keep that use case out of scope.

## Gate review — still open
- The primary lever is weak: about $60/month. The case rests on an *unproven* quality or EU-residency demand `[A6, A7]`.
- All volumes and prices except the user's three facts are `[assumption]` until checked against invoices and `usage` logs.
- The transcription cost line (the larger one) is not addressed by this initiative. It deserves its own canvas: self-hosted Whisper-class ASR on serverless GPUs vs AssemblyAI, with diarization quality as the key risk for action-item owners.
- There is no baseline yet for churn, summary complaints or edit rate. Instrument these before the canary, or the stop condition can't fire.
- Heavy-user economics at a flat $15 is a pricing question, not a model question.

## Layer 3 (HOW) — questions for engineers
- **Data pipelines:** Where are transcripts stored, for how long, and can you replay them for evals without breaching the retention policy?
- **MLOps:** What runs the 60-call golden set automatically on every prompt or model change, and where are results versioned?
- **Compute:** Is there a single provider abstraction (OpenAI SDK + base_url) so that a model swap is a config change? Who owns it?
- **Deployment & serving:** How do the feature flag and per-user routing between GPT-4o and the open model work, and what is the fallback on timeout or invalid JSON?
- **Monitoring:** Which alerts fire on JSON failure rate, p95 latency, cost per call and thumbs-down rate, and who responds?
