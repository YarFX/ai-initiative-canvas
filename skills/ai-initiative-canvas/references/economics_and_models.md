# Economics, model selection, deployment

## Contents
1. AI cost structure (component 4)
2. Token economics and formulas
3. Where tokens are wasted and how to cut costs
4. Model selection
5. Deployment: API vs serverless vs cloud vs on-prem

---

## 1. AI cost structure

AI fails economically in different ways than traditional software: new cost types appear, and some of them grow with usage.

| Cost layer | Drivers | Behaviour at scale | What to watch |
|---|---|---|---|
| **One-time** | Integration, data quality gaps, workflow redesign | One-off | Scope creep; underestimated data preparation |
| **Ongoing fixed** | Human review team, monitoring, iteration cadence | **Step function**: flat until a threshold, then a jump | The review team becomes the bottleneck |
| **Ongoing variable** | Serving (API), training/fine-tuning, data labeling, tool and retrieval calls | Serving — linear in requests; training — periodic; data — grows with the KB | Mistake: treating serving as the only variable cost |

Key takeaways from the course:
- For API-based routing/classification on an open-weight model, **inference is a small share**. Candlekeep: ~$2–5 per month for 20,000 messages vs a current $4.10 per message. The real risks are integration, human-review staffing and monitoring — none of which show up on the provider's bill.
- With custom fine-tuning, **training runs can cost ~100× more than serving**, and they repeat with data drift.
- Unit economics must survive **peaks and heavy users**, not only the average pilot scenario.
- The best cost-structure entry: the full cost structure + a measurable unit-cost guardrail + a breakpoint tied to a change in economics + a realistic ROI **range**. Exact sums without data are false precision.

## 2. Token economics and formulas

- You pay **per token**, not per message. A token ≈ ¾ of an English word ≈ 4 characters. Other scripts use more tokens per character (roughly 1 token ≈ 2–3 Cyrillic characters) — fine for an order-of-magnitude estimate.
- Input and output are billed separately; **output is typically ~5× more expensive**.
- **The system prompt is paid on every request**: 500 tokens × 20,000 messages = 10M input tokens before any customer text.
- Few-shot examples and long instructions add input tokens and a little latency; few-shot cost grows linearly with the number of examples.
- **Batch ≈ −50%** on Nebius (asynchronous, window up to ~24 h) — for back-office work and eval pipelines, not real time.
- Open-weight models via API are **10–200× cheaper** than frontier proprietary ones.
- The cost of GPT-3.5-level inference fell >280× in ~2 years (Stanford HAI) — but cheap tokens ≠ a cheap product: pennies multiply by millions of requests.

Formulas:
```
cost_per_request = in_tokens × in_price_per_1M / 1e6 + out_tokens × out_price_per_1M / 1e6
monthly_cost     = cost_per_request × requests_per_month
annual_cost      = monthly_cost × 12
```
The most accurate source is `usage` from real API responses; at discovery an order-of-magnitude estimate is enough. Use `scripts/token_cost.py` rather than mental arithmetic.

Course example (margin comparison): 4,000 requests/day; small model $0.05 per 1,000 requests → $0.20/day; frontier $8 per 1,000 → $32/day; revenue $80/day → the small model preserves the margin.

## 3. Where tokens are wasted and how to cut costs

| Driver | Fix |
|---|---|
| Web search / tool call on every message | Call tools only when the workflow needs them |
| Full history (24 months of orders) in context | Only relevant context |
| A 2,000-token policy in the system prompt × every request | Retrieve the relevant fragments |
| A premium reasoning model for everything | Route routine tasks to smaller models |
| Real-time summarization of everything | Move non-urgent work to batch |
| Heavy users on "unlimited" plans | Usage caps, workspace limits |

Also: caching, structured outputs, simple post-processing — not every problem needs another LLM call. Quantization makes inference cheaper at a small quality cost.

## 4. Model selection

Principles:
1. **Benchmarks → shortlist**, not a decision. MMLU, GPQA, SWE-bench etc. say nothing about quality on your data; contamination is possible. Where to look: Artificial Analysis (Intelligence index, provider comparisons for the same model).
2. **Start with a capable frontier model** to set the quality bar and see failure modes (a reference point, not the production choice).
3. **Optimize downward deliberately** — test smaller/cheaper models against that bar, by measurement, not assumption.
4. **Choose the smallest model that reliably solves the task.**
5. **Route by task type, not globally**: classification/extraction/formatting → small models; open-ended reasoning and high-stakes user-facing work must "earn" the downgrade.

Selection rule from Notebook A: among models that pass **all** predefined thresholds — max quality → lower unsafe rate → cheaper → faster. Alternative: drop those failing the quality threshold and take the cheapest of the rest. The highest accuracy is not the best candidate if it fails the safety/calibration guardrail.

What failed → what to do:
| Failure | Action |
|---|---|
| Quality | Prompt improvement first (label definitions, key distinctions, confidence definitions), then few-shot, then another model |
| Safety / calibration | Analyse high-confidence errors; do not enable auto mode |
| Cost | Lighter model, trim context, batch |
| Latency | Smaller model (size is the main latency driver), not a longer prompt |

Model family vs provider: the provider determines regions, latency, quotas, throughput, data handling, prices and tooling — these can outweigh small quality differences. Proprietary models (GPT, Claude, Gemini) are available only from their developer; open-weight models (gpt-oss, Llama, Qwen, DeepSeek, Nemotron, Kimi, GLM) from many providers or on your own infrastructure.

Fix these before choosing a model:
- max LLM cost per request/user **at peak**;
- routing rule (what goes to a small model, what escalates to frontier/reasoning);
- batch vs real-time split;
- constraints beyond price: data ownership, legal, regulatory, region;
- customization needs (fine-tuning, own weights).

## 5. Deployment approaches

| Criterion | **API / AI-as-a-service** | **Serverless** | **Cloud self-deployment** | **On-premises** |
|---|---|---|---|---|
| What you manage | Integration only | Container/model | Model, serving, scaling | Everything, including hardware |
| Time to start | Fastest | Fast | Medium | Slow |
| Billing | Per token/request | Per actual resource time | Per provisioned GPU, even when idle | CapEx + operations |
| Economics best at | Low / unpredictable demand | Periodic jobs, variable load | **High, stable** demand (high utilization) | Very large stable volumes + strict requirements |
| Control | Limited (catalog, fine-tuning/LoRA, dedicated endpoints) | Medium | Full (any open-weight model) | Maximum |
| Expertise | Minimal | Medium | High (ML engineers, MLOps) | Very high |

Rules:
- Fastest start without infrastructure → API.
- Self-deployment requires open weights and pays off only with high, stable GPU utilization.
- Typical path: **API → dedicated endpoints → self-deployment**, once demand is large and predictable or there are data-ownership / regulatory / deep-customization requirements.
- Interactive chat/support — latency matters; back-office — throughput → batch.
- Questions for the vendor: latency under load; throughput ceilings (quotas, regional capacity); batch/offline options; data retention; regions.
