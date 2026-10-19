# AI architecture patterns

A pattern describes **how AI is used in the product**, without choosing a model or vendor. It sets component 7 (AI engine), the starting point for component 6, and the primary quality metric for component 8.

## The five patterns

| # | Pattern | Best for | What it needs | Key risks | Primary quality metric |
|---|---|---|---|---|---|
| 1 | **Structured output** | Classification, routing, tagging, field extraction | Defined labels/fields; examples help; training optional | Wrong classification/extraction | Accuracy, **misroute rate**, **F1 per class** |
| 2 | **Content generation** | Create, rewrite, summarize, transform | **All needed information is already in the input**; guidelines/examples | Inaccurate/inappropriate content | **Draft acceptance rate**, edit rate |
| 3 | **Grounded generation (RAG)** | Answers based on a specific **source of truth** | Reliable sources + good retrieval | Poor retrieval, unreliable source | **Groundedness**, policy match rate |
| 4 | **Agentic tool-using workflow** | Multi-step tasks with external systems | Tools + permissions + controls | **Wrong action, wrong target, irreversible effect** | **Task success rate**, **irreversible action rate** |
| 5 | **Composition** | A workflow of several **distinct** AI tasks | Requirements of every combined pattern | Combined risks + complexity | Primary metric of each dominant pattern |

## Selection algorithm — simplest pattern that fits

1. Need to classify / route / tag / extract fields? → **Structured output**
2. Need to create or transform content, and everything needed is in the input? → **Content generation**
3. Does the answer depend on information from a source of truth that is not in the input (policies, stock, order status)? → **Grounded generation (RAG)**
4. Need to call tools / interact with external systems (APIs, live data, actions)? → **Agentic tool-using workflow**
5. Several distinct tasks needing different patterns? → **Composition** — name each pattern and the boundary between them.

**Start simple, then compose.** Add a pattern only when a specific part of the workflow requires it, not "just in case". If you cannot draw the boundary between tasks, it is one pattern with a fuzzy scope.

## Subtleties people get wrong

- **RAG already includes generation.** Don't combine patterns 2 and 3 just because the output is text.
- **RAG reduces but does not eliminate** hallucinations: a grounded but wrong answer is possible (bad retrieval or stale source).
- **Agentic = "doing steps", not "writing text".** A draft a human acts on is pattern 2 or 3. Changing data is not required, though: API calls, queries to live systems and search through tools are agentic too.
- Mandatory controls for agentic: **human approval gates** before sensitive actions, **restricted tool permissions**, **audit logs**, tested rollback. Separate content ingestion from action execution (defence against indirect prompt injection).
- The right evolution order is Doctolib's: RAG first, then an agentic layer with a user confirmation gate (pattern 3 → 4).
- Not every task needs an LLM: regex, if-else, a classic classifier, OCR/Document AI, a moderation classifier or ASR are often cheaper and more reliable. Multimodality is more expensive and slower — use it only when needed.

## Practice mappings (from the course)

| Scenario | Pattern |
|---|---|
| Employee questions about the expense policy, answered from the current policy with a citation | 3 — RAG |
| Clinic referrals (PDF/email): extract name, symptoms, urgency; assign a queue | 1 — Structured output |
| Release notes from a list of PRs in the company's tone, no extra lookup | 2 — Content generation |
| "Where is my order?": check status, update the ticket, sometimes trigger a reshipment | 4 — Agentic |
| IT helpdesk: identify request type + answer from current internal procedures | 5 — Composition: structured output + grounded generation |
| Support triage + reply draft, sometimes based on the returns policy | 5 — Composition: structured + content generation + RAG (RAG only when the policy is needed) |

## Case studies for arguments

- **Structured**: Instacart PARSE (product attributes from text and images); Picnic (intent/sentiment, multilingual); Roblox (~6.1B messages a day; AI is deployed only when it is significantly better than humans on precision and recall).
- **Content generation**: Duolingo DuoRadio (10× faster production); SumUp ("Reason for Suspicion" narratives, reviewed by compliance agents); Mercado Libre GenAds.
- **RAG**: Nubank AskNu (96% ticket deflection, answer in ~9 s instead of up to 30 min of searching); Harvey (legal, traceable citations); LinkedIn (RAG + knowledge graph, −28.6% median resolution time).
- **Agentic**: Ramp Policy Agent (65%+ of approvals fully by the agent, 99% policy-application accuracy, every decision logged); Shopify Sidekick (50+ tools, ground truth from real conversations).
- **Composition**: Uber Genie (+27% acceptable answers, −60% wrong advice); Dropbox Dash; Doctolib (RAG → agentic layer with a confirmation gate).
