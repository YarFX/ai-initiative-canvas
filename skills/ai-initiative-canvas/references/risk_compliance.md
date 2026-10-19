# Risk, security, compliance

Use in Key constraint (component 1), Risks (7), UX/Privacy (10) and the gate review. This is not legal advice; for serious regulatory questions recommend a lawyer / DPO.

## Three risk classes

| Class | Essence | Example |
|---|---|---|
| **Safety** | Harm during normal operation or from internal failures | A hallucinated refund policy; a double charge |
| **Security** | Abuse by external attackers | Prompt injection → data leak |
| **Legal / compliance** | Conformance with laws and contracts | Storing conversations in the wrong region |

Why AI has a different risk profile: LLMs are **non-deterministic**; errors can be **content** errors (substantively wrong) or **form** errors (wrong format, toxic tone — breaks pipelines and trust). Hallucinations happen most at the edges of the model's knowledge, when there is no answer but "helpfulness" pushes it to answer, and in long dense prompts.

## Typical failure/abuse scenarios
Hallucinations · bias · jailbreaks · **prompt injection (direct and indirect)** · data leakage · over-promising (Chevrolet: a bot "sold" a Tahoe for $1; Air Canada: the company was held liable for its bot's words).

Lessons from incidents (EchoLeak in M365 Copilot, "Invitation Is All You Need" in Gemini, Imprompter, JetBrains Rider):
- external content (emails, invites, files, metadata) is **untrusted input**;
- separate **content ingestion** from **action execution**;
- human confirmation before actions;
- least-privilege tools; detection of anomalous outputs; outputs must not drive external channels unchecked.

## Mitigation
- **RAG** — the most practical measure against factual errors; reduces, does not eliminate.
- Input checks, **output checkers** (safety/moderation classifiers, fact-checking).
- **Escalation / uncertainty flags** are a safety mechanism, not a weakness. Calibration matters more than confidence.
- Ordinary cybersecurity still applies.

## Data: governance vs security
Governance — rules and accountability (who may use data, why, under which rules; retention, ownership). Security — technical protection (access control, encryption, backups). Security is a subset of governance: governance sets the rules, security enforces them.

## GDPR / UK-GDPR checklist
- Applies as soon as **personal data** is processed (any information about an identifiable person, including IP, online identifiers, behavioural patterns). In AI, personal data lives in prompts/chats, RAG documents, **logs/traces/feedback**, eval datasets, embeddings, outputs.
- **Pseudonymization ≠ anonymization.**
- **Special categories** (health, biometrics, genetics, race, political/religious beliefs, sexual orientation) need special legal bases and safeguards. **Nebius AI Cloud does not support processing special categories** (medical records, payment card data) — check the chosen provider's limits.
- Principles: **lawful basis** · **data minimization** · **storage limitation** (including logs and embeddings) · **DPIA** for high-risk processing.
- The provider is usually a **data processor**; a **DPA** is needed; in US healthcare, a **BAA**.

## EU AI Act
Risk-based: **unacceptable** (banned) · **high risk** (strict requirements) · **limited risk** (transparency obligations — e.g. disclose that it is AI) · **minimal risk**. The team's main duty is to **classify the system by risk level** and apply the requirements. Consider which decisions the system influences, who relies on its outputs, and how errors affect people. Hiring, credit, access to services, healthcare and education are high-risk candidates.

## Questions for the initiative
1. Which personal data goes into prompts, context, logs? Can it be minimized?
2. Are there special categories? Does the chosen provider support them?
3. Where is data physically processed and stored (data residency)? Is zero-retention available?
4. Is there a DPA / BAA with the provider?
5. Which EU AI Act risk class applies (if relevant)?
6. Which external inputs are untrusted? Can the AI take actions based on their content?
7. What happens if the AI is confidently wrong in front of a customer? Who is accountable?

Safety, security and compliance are built in from the MVP, not "before launch"; compliance must be demonstrated continuously.
