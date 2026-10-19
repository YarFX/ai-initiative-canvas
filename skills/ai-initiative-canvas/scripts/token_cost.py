#!/usr/bin/env python3
"""Token economics calculator for AI initiatives.

Computes cost per request, per month, per year (and at peak) for one or more
models, optionally with batch discount, tool calls (e.g. web search), and a
comparison against the current (non-AI) unit cost of the process.

Examples
--------
# Candlekeep-like routing: 20K msgs/month, measured tokens, two models + frontier bar
python token_cost.py --requests 20000 --in-tokens 174 --out-tokens 155 \
    --preset gpt-oss-120b --preset nemotron-lightning --preset frontier \
    --baseline-unit-cost 4.10

# Estimate tokens from characters, add a 600-token system prompt, 30% batch,
# 1 web search per 5 requests at $0.008, peak = 2x average
python token_cost.py --requests 50000 --in-chars 1200 --out-chars 800 \
    --system-tokens 600 --model "my-model:0.20:0.80" --batch-share 0.3 \
    --tool-calls 0.2 --tool-cost 0.008 --peak-multiplier 2

Prices are USD per 1M tokens. Presets reflect October 2026 list prices and
must be re-checked before decisions are made on them.
"""
import argparse
import json
import sys

PRESETS = {
    # name: (input $/1M, output $/1M, note)
    "gpt-oss-120b": (0.15, 0.60, "Nebius Token Factory, Oct 2026"),
    "nemotron-lightning": (0.06, 0.24, "NVIDIA Nemotron-3.5-Lightning, Token Factory, Oct 2026"),
    "frontier": (10.0, 50.0, "Illustrative frontier proprietary tier, Oct 2026"),
}


def parse_model(spec):
    parts = spec.split(":")
    if len(parts) != 3:
        raise argparse.ArgumentTypeError(
            f"--model must be 'name:input_price:output_price', got '{spec}'")
    name, pin, pout = parts
    return name, float(pin), float(pout), "user-supplied"


def fmt_money(x):
    if x == 0:
        return "$0"
    if x < 0.01:
        return f"${x:.6f}"
    if x < 100:
        return f"${x:,.2f}"
    return f"${x:,.0f}"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--requests", type=float, required=True,
                   help="Requests (units of work) per month, average")
    p.add_argument("--in-tokens", type=float, help="Input tokens per request (user content + context)")
    p.add_argument("--out-tokens", type=float, help="Output tokens per request")
    p.add_argument("--in-chars", type=float, help="Input characters per request (alternative to --in-tokens)")
    p.add_argument("--out-chars", type=float, help="Output characters per request (alternative to --out-tokens)")
    p.add_argument("--chars-per-token", type=float, default=4.0,
                   help="~4 for English, ~2.5 for Russian (default 4)")
    p.add_argument("--system-tokens", type=float, default=0.0,
                   help="System prompt + few-shot tokens added to EVERY request")
    p.add_argument("--calls-per-request", type=float, default=1.0,
                   help="LLM calls per unit of work (e.g. 2 for classify + draft)")
    p.add_argument("--model", type=parse_model, action="append", default=[],
                   help="name:input_price_per_1M:output_price_per_1M (repeatable)")
    p.add_argument("--preset", action="append", default=[], choices=sorted(PRESETS),
                   help="Use a built-in price preset (repeatable)")
    p.add_argument("--batch-share", type=float, default=0.0,
                   help="Share of traffic sent via batch (0..1)")
    p.add_argument("--batch-discount", type=float, default=0.5,
                   help="Batch discount (default 0.5 = -50%%)")
    p.add_argument("--tool-calls", type=float, default=0.0,
                   help="Tool calls (e.g. web searches) per request, average")
    p.add_argument("--tool-cost", type=float, default=0.0,
                   help="Cost per tool call in USD (Tavily basic ~0.008)")
    p.add_argument("--peak-multiplier", type=float, default=1.0,
                   help="Peak month volume as a multiple of average")
    p.add_argument("--baseline-unit-cost", type=float,
                   help="Current cost per unit of work without AI (e.g. 4.10)")
    p.add_argument("--json", action="store_true", help="Print JSON instead of a Markdown table")
    a = p.parse_args(argv)

    if a.in_tokens is None and a.in_chars is None:
        p.error("give --in-tokens or --in-chars")
    if a.out_tokens is None and a.out_chars is None:
        p.error("give --out-tokens or --out-chars")
    if not 0 <= a.batch_share <= 1:
        p.error("--batch-share must be between 0 and 1")

    in_tok = a.in_tokens if a.in_tokens is not None else a.in_chars / a.chars_per_token
    out_tok = a.out_tokens if a.out_tokens is not None else a.out_chars / a.chars_per_token
    in_tok_total = in_tok + a.system_tokens

    models = list(a.model) + [(n, *PRESETS[n]) for n in a.preset]
    if not models:
        p.error("give at least one --model or --preset")

    batch_factor = (1 - a.batch_share) + a.batch_share * (1 - a.batch_discount)
    rows = []
    for name, pin, pout, note in models:
        llm_per_call = in_tok_total * pin / 1e6 + out_tok * pout / 1e6
        llm_per_unit = llm_per_call * a.calls_per_request * batch_factor
        tools_per_unit = a.tool_calls * a.tool_cost
        per_unit = llm_per_unit + tools_per_unit
        monthly = per_unit * a.requests
        row = {
            "model": name,
            "price_in_per_1M": pin,
            "price_out_per_1M": pout,
            "price_note": note,
            "cost_per_unit": per_unit,
            "llm_cost_per_unit": llm_per_unit,
            "tool_cost_per_unit": tools_per_unit,
            "cost_per_1k_units": per_unit * 1000,
            "monthly": monthly,
            "monthly_peak": monthly * a.peak_multiplier,
            "annual": monthly * 12,
        }
        if a.baseline_unit_cost:
            row["share_of_baseline_unit_cost"] = per_unit / a.baseline_unit_cost
        rows.append(row)

    assumptions = {
        "requests_per_month": a.requests,
        "input_tokens_per_call": round(in_tok, 1),
        "system_tokens_per_call": a.system_tokens,
        "output_tokens_per_call": round(out_tok, 1),
        "calls_per_unit": a.calls_per_request,
        "batch_share": a.batch_share,
        "batch_discount": a.batch_discount,
        "tool_calls_per_unit": a.tool_calls,
        "tool_cost": a.tool_cost,
        "peak_multiplier": a.peak_multiplier,
        "baseline_unit_cost": a.baseline_unit_cost,
    }

    if a.json:
        json.dump({"assumptions": assumptions, "results": rows}, sys.stdout, indent=2)
        print()
        return

    print("**Assumptions:** "
          f"{a.requests:,.0f} units/month; {in_tok:,.0f} input + {a.system_tokens:,.0f} system "
          f"+ {out_tok:,.0f} output tokens per call; {a.calls_per_request:g} call(s) per unit; "
          f"batch share {a.batch_share:.0%}; tool calls/unit {a.tool_calls:g} × {fmt_money(a.tool_cost)}; "
          f"peak ×{a.peak_multiplier:g}.")
    print()
    head = ["Model", "$ in/out per 1M", "Cost per unit", "Per 1K units", "Monthly", "Monthly at peak", "Annual"]
    if a.baseline_unit_cost:
        head.append(f"% of current unit cost ({fmt_money(a.baseline_unit_cost)})")
    print("| " + " | ".join(head) + " |")
    print("|" + "---|" * len(head))
    for r in rows:
        cells = [r["model"], f"{r['price_in_per_1M']:g} / {r['price_out_per_1M']:g}",
                 fmt_money(r["cost_per_unit"]), fmt_money(r["cost_per_1k_units"]),
                 fmt_money(r["monthly"]), fmt_money(r["monthly_peak"]), fmt_money(r["annual"])]
        if a.baseline_unit_cost:
            cells.append(f"{r['share_of_baseline_unit_cost']:.3%}")
        print("| " + " | ".join(cells) + " |")
    print()
    print("_Inference only: integration, human review, monitoring and (if any) fine-tuning "
          "are not included. Preset prices are Oct 2026 list prices — re-check before deciding._")


if __name__ == "__main__":
    main()
