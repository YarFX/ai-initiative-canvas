# Nebius stack — when to suggest what

> Prices and limits below were collected in **October 2026** and go stale quickly. Before a calculation that decisions will rest on, check them against the official pages (docs.tokenfactory.nebius.com, nebius.com/token-factory, docs.tavily.com). If you can't check, use these numbers with a note: "prices as of October 2026, need verification".
>
> The skill does not sell Nebius. Suggest a Nebius product when it fits the requirements, and name same-class alternatives (Together AI, Fireworks, AWS Bedrock, Azure AI Foundry; first-party APIs from OpenAI/Anthropic/Google) unless the user is committed to Nebius.

## Product map

| Level | Product | When to suggest |
|---|---|---|
| Inference-as-a-service | **Nebius Token Factory** | Fast start on open-weight models; cheap routing/classification/extraction; EU/US data residency or zero-retention needed; migrating from a proprietary API (OpenAI-compatible) |
| No infrastructure management | **Nebius Serverless AI** | Your own container/model without a cluster: **Jobs** (fine-tuning, batch inference, data processing) and **Endpoints** (real-time services) |
| Infrastructure | **Nebius AI Cloud** | Training your own models, self-hosted inference with high stable load, full control (GPU VMs, Managed Kubernetes, Slurm/Soperator, InfiniBand) |
| Web access for agents | **Tavily** | Grounding on the open web: research/monitoring agents, fresh data. Don't enable it on every message — it is a tool call with its own price |

Nebius's phrasing: "Token Factory helps agents reason, while Tavily helps them know".

## Token Factory — what matters for decisions
- **OpenAI-compatible API** (`https://api.tokenfactory.nebius.com/v1/`) — migrate from the OpenAI SDK by swapping base_url and key.
- **60+ open models**: gpt-oss, DeepSeek, Llama, Qwen, Nemotron, Kimi, GLM and others; embeddings and rerank (RAG building blocks); vision; you can host your own models.
- **Playground** — side-by-side model comparison, JSON response format, presets.
- **Fast vs Base flavors** — Fast for interactive scenarios (low latency), Base for economical background throughput; switch without redeploying.
- **Batch inference** — ≈50% cheaper than real time.
- **Dedicated endpoints** — isolation, predictable latency, reserved capacity, **99.9% SLA**, EU or US region.
- Starter limits: **400K TPM / 600 RPM**, best-effort 99% availability; Enterprise — no throughput limits.
- **Post-training**: LoRA and full fine-tuning, hosting of fine-tuned models; distillation (per Nebius, up to 70% lower cost/latency).
- Structured output / JSON, function calling & tools, observability, RBAC/SSO, Data Lab, sandboxes for agents.
- **Compliance**: zero-retention mode (data not stored or used for training); data centers in Finland, France, USA; SOC 2 Type II (incl. HIPAA), ISO 27001; custom DPA for Enterprise.

## Indicative prices (October 2026, $ per 1M tokens input / output)

| Model | Where | Input | Output | Comment |
|---|---|---|---|---|
| openai/gpt-oss-120b | Token Factory | 0.15 | 0.60 | Strong quality/cost balance for routing and classification in benchmarks of this method; verify on your data |
| NVIDIA Nemotron-3.5-Lightning | Token Factory | 0.06 | 0.24 | Ultra-cheap tier for simple tasks |
| Frontier proprietary (e.g. top-tier GPT / Claude / Gemini models) | First-party API | ~10 | ~50 | Quality bar; expensive for high-volume routine work |

Illustrative measurement (support routing, gpt-oss-120b): ~174 input + ~155 output tokens per message → ~$0.00012 per message → ~$2.4/month for 20,000 messages.

## Tavily — prices
1,000 free credits/month; pay-as-you-go **$0.008 per credit**. Search basic/fast = 1 credit, advanced = 2 credits. Endpoints: Search, Extract (up to 20 URLs), Map, Crawl, Research (multi-step report with citations). Connects to Token Factory via function calling or the Tavily MCP server.

## Case studies for arguments
- **Chatfuel**: from GPT-4 to a Llama-405B cascade on Nebius → routing performance +24% vs GPT-4o, faster and cheaper; in production within a month.
- **Prosus**: per Nebius, up to 26× lower cost vs proprietary models, up to 200B tokens a day.
- **Recraft**: trains its own image models on Nebius AI Cloud.

## Deployment evolution path
Token Factory (pay-per-token) → dedicated endpoint (stable load, SLA, predictable latency) → Serverless / AI Cloud (own weights, high stable utilization, deep customization).
