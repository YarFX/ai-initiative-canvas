# AI CV reading for an HR screening bot — AI Initiative Canvas

*2026-10-19 · Mode: Wizard (10 steps with the product owner) · Data source: owner's answers + the bot's repository and product notes. Unconfirmed numbers are marked `[assumption]`.*

## Verdict
**GO → offline MVP experiment, with a compliance gate before any live use.** The economics are overwhelmingly positive: AI costs ~$0.0003–0.0009 per CV against ~$1.00 of HR time, and a client gets 25–60 h/month back for a +$100 tier. The real risk is that AI-assisted candidate screening is a **high-risk use under the EU AI Act** and processes CVs under GDPR. Run the offline bake-off now; put the compliance baseline (DPA with the client, DPIA, candidate notice, decision logging) in place before Shadow on real candidates.

Key numbers: manual CV reading ≈ $1.00 per response (3 min × $20/h) → AI ≈ $0.0003–0.0009 per response · Primary metric: ≥40% of the next 10–20 clients pay for the AI tier · Main risk: a false "✗ contradicted" pushing a good candidate towards rejection, plus high-risk compliance.

## Assumptions and open questions
| # | Assumption | Why it matters | How to verify |
|---|---|---|---|
| A1 | AI tier priced at +$100/client/month on a $50 base | Drives ROI and the primary metric | Price test with the pilot client at conversion |
| A2 | External compliance help costs $1–3K one-time | Payback range | Quote from a GDPR/AI Act consultant |
| A3 | Gemini 2.5 Flash list price $0.30 / $2.50 per 1M tokens; batch discount available | Current-model cost line | Provider pricing page; check the batch option via the current gateway |
| A4 | ~1,800 input tokens per CV + answers, 700 for instructions and criteria, 400 output | Inference estimate | `usage` from the first 50 real calls |
| A5 | EU AI Act high-risk obligations apply to this product at GA; the exact application date must be checked | Timeline of compliance cost | Legal review before GA |
| A6 | Kazakhstan's data-localization rules may require local storage for Kazakh candidates | Blocks KZ rollout on an EU-only stack | Legal check before onboarding KZ clients |

## Layer 1 — Business foundation (WHY)

**1. Business problem.** At ~10 active vacancies across 2 HR clients today (10–20 clients expected within a month), each vacancy gets 100–250 responses a month, and HR reads every applicant's bot answers and CV by hand: ~5 min per response, 3 of them on the CV, ~$1.67 of HR time at $20/h. That is 40–100 h/month of screening per client. The existing AI shortlist reads only the bot answers, so HR still opens every CV. This matters because client count is set to grow 5–10× while screening time grows linearly with volume. Target: HR opens CVs only for candidates worth a call, and no candidate is left without an answer. Constraint: HR keeps every decision; clients and candidates are in the EU and Kazakhstan.
*Primary lever:* **revenue growth** — AI CV reading as a paid tier for HRs without an expensive ATS.

**2. Business metrics.** Primary: ≥40% of the next 10–20 clients choose and pay for the AI CV tier. Leading signal: HR screening time ≤2 min per response (from ~5). Secondary: median time from response to HR decision ≤2 days; candidates left without an answer = 0. Timeframe: 6-week pilot with one client. Stop: if after 6 weeks HR time per response falls by <40%, or HR still opens ≥80% of CVs, stop and keep AI on the bot answers only.

**3. Value for customers.** For in-house HRs at small and mid-size companies and IT recruiters, who get 100–250 responses per vacancy and have no expensive ATS, we provide a short CV summary checked against the vacancy's must-have criteria, with a verbatim quote for every claim. It's better than opening and reading every CV by hand, and it saves ~3 min per response (~60% of screening time). Stakeholder (pays): the manager, who gets vacancies closed without hiring screening capacity. Candidates: a faster and guaranteed answer, an upfront AI notice, and a person who always decides.

**4. Cost structure.** Costs: one-time = CV text extraction, criteria prompt, golden-set labelling, compliance baseline (DPIA, candidate notice, logging, risk documentation), build time 30–40 h × $30 = $900–1,200. Ongoing = inference, weekly sample audits, CV storage with 3-month retention, compliance upkeep. Unit: AI cost per screened response, guardrail ≤$0.01. Breakpoint: general availability in the EU turns compliance into a fixed cost; a rising share of scanned CVs means OCR or vision models (×5–10 per CV). ROI: ~$800/month at 8 of 20 clients on the AI tier against ~$100/month ongoing; payback ~2–6 months depending on A2. Client side: 25–60 h/month (≈$500–1,250) of HR time for $100.

**5. Go-to-market.** Distribution: 1 current client on its highest-volume vacancy → both current clients → new clients, with the AI tier as a paid add-on; new clients get only the base bot until the gates pass. Activation: the first shortlist with CV summaries within 24 h of switching on, and the HR opens fewer than half of the CVs. Pilot pricing: free for 6 weeks, then +$100/month with an easy opt-out. Gates: HR time ≤2 min/response on the pilot vacancy; the pilot client converts to paid; Component 9 quality evidence holds.

## Architecture pattern
**Structured output** (extraction + classification against criteria). Everything the model needs — CV text and the HR's criteria — is in the input, so it is not RAG. The AI takes no actions (HR taps, the bot sends), so it is not agentic. The 2-line summary is one more field in the same JSON, so no Composition is needed. PDF text extraction is ordinary software in front of the model.

## Layer 2 — Product blueprint (WHAT)

**6. Product shape.** Form: an "AI CV check" block inside the existing candidate card in the HR group. User: the HR of a connected client. Workflow point: the card arrives as today; a batch run every 4 h on working days adds the AI block before the HR reviews the backlog. Output: a must-have checklist (✓ confirmed / ✗ contradicted / ? not visible) with a verbatim CV quote per item, a 2-line summary and an "AI suggestion: invite / review / reject" label. Later: a batch shortlist report per vacancy, after the pilot.

**7. AI engine.** Approach: Structured output. How it works: extract text from text-based CVs (scans are marked "AI check unavailable" in the pilot) and strip protected attributes (photo, date of birth, nationality, marital status, gender markers) → one LLM call returns per-criterion status with a verbatim quote, plus a 2-line summary → code checks every quote against the CV text and computes the suggested bucket. The model uses only HR-written criteria; no must-haves means no AI check. Start with / Evolve to: an off-the-shelf model → per-vacancy examples or a small fine-tuned model only if DE/ES quality lags; OCR if scans grow. Risks: a false "✗ contradicted" leading to an unfair rejection; misread facts; prompt injection hidden in a CV.

**8. Solution metrics.** Quality: per-criterion status accuracy ≥90% on the golden set; **false-contradicted rate ≤3%** of criteria; 100% of shown quotes found verbatim in the CV (claims without a valid quote are downgraded to "?"); "AI suggestion: reject" agrees with the HR's decision in ≥95% of cases; accuracy gap between EN / DE / ES ≤5 pp. Performance: AI block added within one batch cycle (4 h, working days); ≥98% of text-based CVs processed; ≥99% valid structured outputs.

**9. Validation strategy.** Offline: golden dataset of ~120 CVs — the pilot client's past CVs (with their OK, pseudonymised) plus ~30 synthetic DE/ES CVs; the owner labels every criterion (~5–6 h), the pilot HR reviews only ✗ and disputed items (~1–2 h). Live: Shadow for 2 weeks or 150 responses, whichever comes later, comparing suggestions with HR decisions; then Assist, with the block visible to the pilot HR. No Auto stage — the AI never decides; expansion means more vacancies and clients, not more autonomy. Monitoring: weekly 20-card sample, per-language accuracy, "Flag AI error" counts, re-check when criteria change. Stop/Rollback: false-contradicted >3% in a weekly sample, or a candidate complaint about an AI-influenced rejection → that vacancy returns to Shadow.

**10. User experience.** Scenarios: the HR works through the backlog of cards; the HR checks a doubtful ✗; a candidate starts the survey. Primary actions: Invite / Reject (unchanged, two-tap confirmation), Open CV, **Flag AI error**. AI-specific UX: "🤖 AI suggestion — the decision is yours"; "⏳ AI check pending" until the batch runs; "? not visible in CV" shown, not hidden; scans show "AI check unavailable". Candidates: at /start, "AI helps HR read your CV; a person makes every decision", with a privacy-notice link and human-only review on request. Privacy: protected attributes stripped before the model; EU-region zero-retention API; CVs never used for training; CV text and AI outputs deleted 3 months after the vacancy closes.

## Inference economics
Batch mode (every 4 h) at 20 clients ≈ 25,000 CVs/month; tokens per CV per A4; batch pricing assumed for all tiers.

| Model | Per CV | Per month | At peak ×1.5 | Share of the $1.00 manual CV cost |
|---|---|---|---|---|
| Gemini 2.5 Flash (current) `[A3]` | $0.0009 | $22 | $33 | 0.09% |
| gpt-oss-120b (Token Factory) | $0.0003 | $8 | $12 | 0.03% |
| Frontier tier (quality bar only) | $0.0225 | $562 | $844 | 2.3% |

Today's volume (2,500 CVs/month) costs under $1/month on gpt-oss-120b. Inference is not a decision factor; build time, compliance and audit time are. *Prices as of October 2026; verify before deciding.*

## Model and deployment
- **Shortlist for the bake-off:** a frontier model as the quality bar (golden set only, not production) + Gemini 2.5 Flash (current) + gpt-oss-120b + one larger multilingual open-weight model, the last two on Nebius Token Factory. All are tested on EN, DE and ES.
- **Selection rule:** among models passing all H1–H4 thresholds → lowest false-contradicted rate → cheaper → faster. Highest accuracy alone does not win.
- **Deployment:** a pay-per-token API in an EU region with zero retention, using the batch endpoint. Token Factory meets both by default (EU data centers, zero-retention mode, OpenAI-compatible — a base_url swap). If Gemini stays, pin the EU region and no-retention terms through the gateway. Revisit only if Kazakh data must stay in Kazakhstan (A6), which would require a local deployment.

## Next step: MVP experiment
Capability to test: per-criterion extraction with verbatim quotes on text-based CVs — the riskiest part (false ✗, language parity). In scope: golden set, prompt v1, code quote-check and bucket rule, 3–4 models. Out of scope: the card UI, OCR, live candidates, the batch shortlist report.

| Hypothesis | Metric | Threshold |
|---|---|---|
| H1 Quality | Per-criterion status accuracy; language gap | ≥90%; EN/DE/ES gap ≤5 pp |
| H2 Safety | False-contradicted rate; invalid quotes after code check | ≤3%; 0 shown |
| H3 Unit economics | AI cost per CV | ≤$0.01 |
| H4 Speed / reliability | Batch of 250 CVs; valid structured outputs | <30 min; ≥99% |

Golden dataset: ~120 CVs (≈40 per language), 1–3 vacancies' criteria, edge cases included (career gaps, freelance work, mixed-language CVs, embedded instructions). Never tune the prompt on the golden set. Decision rule: all four pass → compliance baseline → Shadow; H1/H2 fail → improve the prompt (criterion definitions, "not visible" vs "contradicted" rules), then try another model; still failing on DE/ES → pilot on EN-only vacancies.

## Risks and compliance
- **EU AI Act — high-risk.** AI used to filter applications or evaluate candidates falls into the employment category of high-risk systems. As the provider, expect risk management, data governance, technical documentation, logging, human-oversight design, accuracy targets and post-market monitoring; clients as deployers must inform candidates. Check the current application date and obligations with a lawyer before GA (A5).
- **GDPR.** The client is the controller, the bot owner a processor: a DPA with each client, the LLM provider listed as a sub-processor, a DPIA, data minimisation (attribute stripping), 3-month retention. Decisions are not solely automated (Art. 22): HR decides with two taps, and the UI must keep that real.
- **Bias and automation bias.** Monitor reject-suggestion and false-✗ rates per language; watch for HR agreement with "reject" so close to 100% that it suggests rubber-stamping; the weekly audit samples AI-suggested rejects first.
- **Prompt injection in CVs.** CVs are untrusted input; the model has no tools, so injection can only skew the output. Verbatim-quote checks and a code-computed bucket limit the impact; flag CVs with instruction-like text.
- **Kazakhstan.** Possible localization requirements (A6); KZ clients stay on the base bot until checked.

## Gate review — still open
- Price (A1) and compliance cost (A2) are unconfirmed; the primary metric depends on A1.
- The current model runs through a gateway whose region and retention must be pinned before any real CV is sent.
- Lawful basis and the pilot client's consent for using past CVs in the golden set must be in writing before labelling.
- The "AI check pending" state must make clear that a card without the AI block is incomplete, so HR doesn't decide on half the picture.

## Layer 3 (HOW) — questions for engineering
- **Data pipelines:** where extracted CV text lives (today the CV is a Telegram file id); how the 3-month deletion runs; where synthetic CVs are stored.
- **MLOps:** how the golden-set eval reruns on every prompt or model change; where the model ID and prompt version are recorded per card.
- **Compute:** batch API vs a scheduled job; who owns the integration.
- **Deployment & serving:** how a new prompt version reaches one vacancy before all (canary by vacancy).
- **Monitoring:** alerts on false-✗ rate, "Flag AI error" spikes and batch failures; decision logs kept for audit.
