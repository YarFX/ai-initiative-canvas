# Wizard — filling in the Canvas step by step with the user

The wizard runs when the sufficiency check (SKILL.md, step 0) shows that data is thin, or the request is phrased as a solution without a problem ("an agent that handles everything", "we want ChatGPT for the team"). The goal is not to hand over a document built on invented numbers, but to gather, together with the user, the facts the decision actually rests on.

All wizard messages are in English unless the user has asked for another language.

## Route

| Step | Block | Layer | Who leads |
|---|---|---|---|
| 1 | Business problem | WHY | The user answers |
| 2 | Business metrics | WHY | The user answers, Claude proposes thresholds |
| 3 | Value for customers | WHY | The user answers |
| 4 | Cost structure | WHY | The user gives numbers, Claude calculates |
| 5 | Go-to-market | WHY | Claude proposes, the user chooses |
| 6 | Product shape | WHAT | Claude offers 2 options, the user picks |
| 7 | AI engine | WHAT | Claude recommends a pattern, the user confirms |
| 8 | Solution metrics | WHAT | Claude proposes metrics and thresholds, the user adjusts |
| 9 | Validation strategy | WHAT | Claude proposes, the user confirms |
| 10 | User experience | WHAT | Claude proposes, the user confirms |
| Result | Economics, MVP H1–H4, risks, gate review, verdict, document + visual Canvas | — | Claude |

Layer 3 (11–15) is not part of the wizard: those are engineering decisions; in the result they appear as a list of questions.

## The first wizard message

1. In one or two sentences explain why a wizard: what is missing for an honest assessment (e.g. "there is a desired solution, but no problem, scale or cost of the current process — the whole conclusion rests on those"). No reproach: "an agent that handles everything" is a perfectly normal starting point.
2. Show the route: 10 steps across two layers + the result; a time estimate (usually 10–15 minutes of answers).
3. Explain the control replies: "don't know" → I'll record an assumption and move on; "skip" → the block stays open; "finish it yourself" → I'll fill the remaining blocks on assumptions and go straight to the result.
4. Start step 1 in the same message, so no turn is wasted on "ready?".

## Format of every step

```
**Step N of 10 · <Block name>** — Layer <1 WHY | 2 WHAT>
Progress: ✅1 ✅2 ▶3 ○4 ○5 | ○6 ○7 ○8 ○9 ○10 | result

<What we define here — one sentence in plain language.>

<What is already known from your answers / a draft entry — if any.>

Questions:
1. … (default: …)
2. …

Next step: N+1 · <Name> — <why, in one sentence>.
```

After the user replies — in **one** message:
1. "Recorded in the Canvas (block N):" — the final entry for the block in the methodology's format, 1–3 sentences, assumptions marked `[assumption]`;
2. if the user's numbers contradict each other (e.g. volume × time per unit exceeds the team's available hours), name the discrepancy and base the next thresholds on a consistent picture (usually the conservative one), not on one of the conflicting numbers; when in doubt, add a clarifying question to the next step;
3. if the answer contradicts the method (e.g. an AI metric among business metrics, auto mode from day one), say so briefly and propose a fix without overriding the user's choice;
4. the next step straight away, in the format above.

Rules that keep the wizard tolerable:
- **1–4 questions per step**, each with a default or options. The user should be able to answer in a word.
- If the original description already answers a block's question, don't ask again: show the draft entry and ask to "confirm or correct".
- In steps 5–10 Claude mostly **proposes** rather than asks: users usually know their business better than the method. A proposal + 1–2 choice questions.
- If the environment has a multiple-choice question tool, you may use it for option questions, but the step header, progress line and "Next step" are still written as text in the message.
- After step 5 (end of layer 1) briefly summarize the layer: problem, primary lever, unit cost, stop condition. If it is already clear that AI isn't needed or the economics don't work, say so and offer to stop at NO-GO/REFRAME without going through layer 2.
- If the user replies "finish it yourself", fill the remaining blocks on marked assumptions and go to the result.

## Question bank per step

Pick the 1–4 that matter most for the case, not all of them.

**1. Business problem**
- What exactly is wrong today? What happens to a request/document/customer from arrival to resolution? (If the user came with a solution — "an agent", "a bot" — translate it into a problem: "what hurts without this agent?")
- Scale: how many units of work per month (requests, documents, calls)?
- What does it cost today: people (FTEs) × time per unit, delays, losses, penalties?
- Why now: growth, SLA, season, regulation, a competitor?
- Constraints: compliance, data, brand, budget?
- Primary lever hint: "if the problem disappeared, would it mainly save money, bring revenue, reduce risk or free up capital?"

**2. Business metrics**
- Which number from an operations report (not about AI) do you want to move, and to what value? (Claude proposes 1–2 metrics and a threshold from step 1 data)
- Over what period should the pilot show an effect? (default 8–12 weeks)
- Stop condition: at what result will we honestly stop? (Claude proposes one)

**3. Value for customers**
- Whose work actually changes (users), and who pays/approves (stakeholders)?
- How do these people cope today (current alternative)?
- Who is the primary audience: an internal team or external customers?

**4. Cost structure**
- What does one unit of work cost today (or FTEs × rate, if never calculated)?
- Is there a budget / per-unit limit / expected payback period?
- Who will review AI outputs and maintain the knowledge base — are there people for that?
- (Claude calculates inference with `scripts/token_cost.py` and shows its share of the current unit cost.)

**5. Go-to-market**
- Who could be the first cohort of 2–3 experienced people? (Claude proposes)
- What does "first value" on day one look like?
- What evidence justifies expansion? (Claude proposes gates: adoption % + quality thresholds)

**6. Product shape** — offer 2 options and ask which is closer:
- A: an internal assist tool (a human approves) — lower risk, faster trust;
- B: a customer-facing/autonomous option — bigger effect, higher cost of error.
- Where exactly in the workflow does it appear (a place, not a sequence)? What is the output: a label, a draft, an answer, an action?

**7. AI engine**
- Recommend a pattern via the algorithm in `architecture_patterns.md`, with one sentence on "why not the neighbouring one".
- Ask only what changes the pattern: "Do answers depend on documents/policies not in the input?" "Are actions in external systems needed?"
- For agentic: "Which actions are reversible, which are not?"

**8. Solution metrics** — propose the pattern's primary quality metric with a threshold and 1–2 system metrics (latency/reliability); ask whether the thresholds are acceptable.

**9. Validation strategy** — propose: golden dataset (size, who labels it), Shadow → Assist → Auto, a rollback condition. Ask: "Who can label 50–100 real examples?"

**10. User experience** — propose scenarios and primary actions, disclose AI, override, a low-confidence flag, data minimization. Ask about interface constraints (Slack, CRM, your own app).

## Result

After step 10 (or "finish it yourself") run steps 4–8 of the main workflow (economics, model and deployment, MVP, risks, gate review) and deliver both artifacts: the document and the visual Canvas. Open the final message with the verdict and what to do next.
