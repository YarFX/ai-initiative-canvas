#!/usr/bin/env python3
"""Render a visual AI Product & System Canvas (Nebius Academy Canvas layout) as a
self-contained HTML page.

Usage:
    python render_canvas.py canvas.json -o canvas.html

Input JSON (all text fields are plain text; keep each block to 1-3 short lines):
{
  "title": "IT helpdesk assistant",
  "subtitle": "AI Initiative Canvas · 2026-10-18",          # optional
  "lang": "en",                                               # optional, default "en"; set when the user asked for another language
  "verdict": {"label": "REFRAME → GO on MVP", "kind": "go|reframe|nogo",
              "summary": "one or two sentences"},
  "key_numbers": ["$4.2 per ticket today", "inference ≈ $6/month", "..."],  # optional, ≤4
  "pattern": "Composition: Structured output + RAG",          # optional
  "components": {
    "1": {"text": "...", "status": "fact|assumption|open"},
    ...                                                       # keys "1".."15"
  },
  "next_step": "MVP: routing + Confluence answers on 150 tickets; H1 ≥85% ...",  # optional
  "hypotheses": [{"name": "H1 Quality", "metric": "...", "threshold": "..."}]        # optional
}

status meaning: fact = from the user's data; assumption = Claude's labeled
assumption; open = not decided yet (default for layer 3 = questions for engineers).
"""
import argparse
import html
import json
import sys

BLOCKS = {
    1: ("Business problem", "What problem costs money/time today?", "why"),
    2: ("Business metrics", "Which business outcomes improve? When do we stop?", "why"),
    3: ("Value for customers", "For [who] with [problem], we provide [value]", "why"),
    4: ("Cost structure", "Costs, unit economics, breakpoint, ROI range", "why"),
    5: ("Go-to-market", "Who gets it first, first value, expansion gates", "why"),
    6: ("Product shape", "Where it lives in the workflow and what it outputs", "what"),
    7: ("AI engine", "Architecture pattern and model approach", "what"),
    8: ("Solution metrics", "Quality and performance thresholds", "what"),
    9: ("Validation strategy", "Offline → Shadow → Assist → Auto, rollback", "what"),
    10: ("User experience", "Actions, AI disclosure, override, privacy", "what"),
    11: ("Data pipelines", "Data sources, storage, KB update cadence", "how"),
    12: ("MLOps", "Tools for experimentation and evaluation", "how"),
    13: ("Compute infrastructure", "Cloud services and team composition", "how"),
    14: ("Deployment & serving", "Deployment and CI/CD", "how"),
    15: ("Monitoring", "Monitoring tools and alerting", "how"),
}

LABELS = {
    "ru": {"blueprint": "AI Product Blueprint", "system": "AI System Design",
           "why": "WHY · Business foundation", "what": "WHAT · Product blueprint",
           "how": "HOW · System design",
           "fact": "факт", "assumption": "допущение", "open": "открыто",
           "pattern": "Паттерн", "next": "Следующий шаг", "legend": "Статус блока",
           "empty": "— не заполнено —", "hyp": "Гипотеза", "metric": "Метрика", "thr": "Порог"},
    "en": {"blueprint": "AI Product Blueprint", "system": "AI System Design",
           "why": "WHY · Business foundation", "what": "WHAT · Product blueprint",
           "how": "HOW · System design",
           "fact": "fact", "assumption": "assumption", "open": "open",
           "pattern": "Pattern", "next": "Next step", "legend": "Block status",
           "empty": "— not filled —", "hyp": "Hypothesis", "metric": "Metric", "thr": "Threshold"},
}

# grid placement on a 10-column grid: (column start, column span, row start, row span)
BLUEPRINT = {1: (1, 2, 1, 2), 2: (3, 2, 1, 1), 8: (3, 2, 2, 1), 3: (5, 2, 1, 2),
             5: (7, 2, 1, 1), 9: (7, 2, 2, 1), 4: (9, 2, 1, 2),
             6: (1, 3, 3, 1), 7: (4, 4, 3, 1), 10: (8, 3, 3, 1)}
SYSTEM = {11: (1, 2, 1, 2), 12: (3, 2, 1, 1), 8: (3, 2, 2, 1), 13: (5, 2, 1, 2),
          14: (7, 2, 1, 1), 9: (7, 2, 2, 1), 15: (9, 2, 1, 2),
          6: (1, 3, 3, 1), 7: (4, 4, 3, 1), 10: (8, 3, 3, 1)}

CSS = """
:root{--bg:#f7f8fa;--surface:#ffffff;--ink:#14212b;--muted:#5b6b78;--line:#dfe4e8;
--why:#12a37a;--why-bg:#e9f8f2;--what:#e38b2c;--what-bg:#fdf3e7;--how:#4a8fe0;--how-bg:#ecf3fd;
--go:#12a37a;--reframe:#d4890f;--nogo:#d0463b;--chip:#eef1f4}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#11161b;--surface:#182029;--ink:#e6edf3;
--muted:#9aa8b4;--line:#2b3641;--why:#3ccf9f;--why-bg:#13302a;--what:#f2a65a;--what-bg:#33261a;--how:#7cb2f2;--how-bg:#172739;
--go:#3ccf9f;--reframe:#f0b04a;--nogo:#f07a70;--chip:#222c36}}
:root[data-theme="dark"]{--bg:#11161b;--surface:#182029;--ink:#e6edf3;--muted:#9aa8b4;--line:#2b3641;--why:#3ccf9f;
--why-bg:#13302a;--what:#f2a65a;--what-bg:#33261a;--how:#7cb2f2;--how-bg:#172739;--go:#3ccf9f;--reframe:#f0b04a;--nogo:#f07a70;--chip:#222c36}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:1280px;margin:0 auto;padding:28px 16px 40px}
header h1{font-size:26px;line-height:1.2;margin:0 0 4px;letter-spacing:-.01em}
.sub{color:var(--muted);margin:0 0 16px}
.verdict{display:flex;gap:12px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);
border-radius:14px;padding:14px 16px;margin-bottom:12px}
.pill{flex:none;font-weight:700;font-size:13px;padding:4px 10px;border-radius:999px;color:#fff;white-space:nowrap}
.pill.go{background:var(--go)}.pill.reframe{background:var(--reframe)}.pill.nogo{background:var(--nogo)}
.verdict p{margin:2px 0 0}
.nums{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 12px;padding:0;list-style:none}
.nums li{background:var(--chip);border-radius:8px;padding:6px 10px;font-size:13.5px}
.meta{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;margin:4px 0 18px;color:var(--muted);font-size:13.5px}
.meta b{color:var(--ink)}
.toggle{display:inline-flex;background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:4px;margin:0 auto 16px}
.toggle button{border:0;background:transparent;color:var(--muted);font:inherit;font-size:14px;padding:7px 16px;border-radius:999px;cursor:pointer}
.toggle button[aria-pressed="true"]{background:var(--ink);color:var(--bg)}
.center{text-align:center}
.grid{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:12px}
.grid[hidden]{display:none}
.card{background:var(--surface);border:1.5px solid var(--line);border-radius:14px;padding:14px 14px 12px;min-height:120px;
display:flex;flex-direction:column;gap:6px}
.card.why{border-color:var(--why);background:var(--why-bg)}
.card.what{border-color:var(--what);background:var(--what-bg)}
.card.how{border-color:var(--how);background:var(--how-bg)}
.card h3{margin:0;font-size:15px;line-height:1.25;display:flex;gap:8px;align-items:baseline}
.card h3 .n{font-size:12px;color:var(--muted);font-weight:600;min-width:1.4em}
.q{margin:0;color:var(--muted);font-size:12.5px}
.t{margin:2px 0 0;font-size:14px;white-space:pre-line}
.t.empty{color:var(--muted);font-style:italic}
.st{margin-top:auto;align-self:flex-start;font-size:11.5px;padding:2px 8px;border-radius:999px;border:1px solid var(--line);color:var(--muted);background:var(--surface)}
.st.assumption{border-style:dashed;color:var(--reframe);border-color:var(--reframe)}
.st.fact{color:var(--go);border-color:var(--go)}
.legend{display:flex;flex-wrap:wrap;gap:8px 16px;margin:16px 0 0;font-size:12.5px;color:var(--muted);align-items:center}
.sw{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-1px;border:1.5px solid}
.sw.why{border-color:var(--why);background:var(--why-bg)}.sw.what{border-color:var(--what);background:var(--what-bg)}.sw.how{border-color:var(--how);background:var(--how-bg)}
section.next{margin-top:22px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
section.next h2{font-size:16px;margin:0 0 6px}
section.next p{margin:0 0 8px}
.tbl{width:100%;border-collapse:collapse;font-size:13.5px}
.tbl th,.tbl td{text-align:left;padding:6px 8px;border-top:1px solid var(--line);vertical-align:top}
.tbl th{color:var(--muted);font-weight:600}
@media (max-width:820px){.grid{grid-template-columns:1fr}.card{grid-column:auto!important;grid-row:auto!important;min-height:0}
header h1{font-size:22px}.verdict{flex-direction:column}}
@media print{.toggle{display:none}.grid[hidden]{display:grid;margin-top:16px}body{background:#fff}}
"""

JS = """
const btns=document.querySelectorAll('.toggle button');
btns.forEach(b=>b.addEventListener('click',()=>{btns.forEach(x=>x.setAttribute('aria-pressed',x===b));
document.querySelectorAll('.grid').forEach(g=>g.hidden=g.id!==b.dataset.view);}));
"""


def esc(s):
    return html.escape(str(s or ""), quote=True)


def card(num, comp, lab, view_order):
    title, q, layer = BLOCKS[num]
    text = (comp or {}).get("text", "").strip()
    status = (comp or {}).get("status") or ("open" if layer == "how" else ("assumption" if text else "open"))
    if status not in ("fact", "assumption", "open"):
        status = "assumption"
    c1, cs, r1, rs = view_order[num]
    style = f"grid-column:{c1} / span {cs};grid-row:{r1} / span {rs};order:{num}"
    body = f'<p class="t">{esc(text)}</p>' if text else f'<p class="t empty">{esc(lab["empty"])}</p>'
    return (f'<article class="card {layer}" style="{style}">'
            f'<h3><span class="n">{num}</span>{esc(title)}</h3><p class="q">{esc(q)}</p>{body}'
            f'<span class="st {status}">{esc(lab[status])}</span></article>')


def render(data):
    lang = data.get("lang", "en")
    lab = LABELS.get(lang, LABELS["en"])
    comps = {int(k): v for k, v in (data.get("components") or {}).items() if str(k).isdigit()}
    title = data.get("title", "AI Initiative Canvas")
    v = data.get("verdict") or {}
    kind = v.get("kind", "reframe")
    if kind not in ("go", "reframe", "nogo"):
        kind = "reframe"

    parts = [f'<!doctype html><html lang="{esc(lang)}"><head><meta charset="utf-8">'
             f'<meta name="viewport" content="width=device-width,initial-scale=1">'
             f'<title>{esc(title)} — Canvas</title><style>{CSS}</style></head><body><div class="wrap">',
             f'<header><h1>{esc(title)}</h1><p class="sub">{esc(data.get("subtitle", "AI Product & System Canvas"))}</p></header>']
    if v:
        parts.append(f'<div class="verdict"><span class="pill {kind}">{esc(v.get("label", ""))}</span>'
                     f'<p>{esc(v.get("summary", ""))}</p></div>')
    nums = data.get("key_numbers") or []
    if nums:
        parts.append('<ul class="nums">' + "".join(f"<li>{esc(n)}</li>" for n in nums[:4]) + "</ul>")
    if data.get("pattern"):
        parts.append(f'<div class="meta"><span>{esc(lab["pattern"])}: <b>{esc(data["pattern"])}</b></span></div>')

    parts.append(f'<div class="center"><div class="toggle" role="group">'
                 f'<button type="button" data-view="bp" aria-pressed="true">{esc(lab["blueprint"])}</button>'
                 f'<button type="button" data-view="sd" aria-pressed="false">{esc(lab["system"])}</button></div></div>')
    parts.append('<div class="grid" id="bp">' + "".join(card(n, comps.get(n), lab, BLUEPRINT) for n in BLUEPRINT) + "</div>")
    parts.append('<div class="grid" id="sd" hidden>' + "".join(card(n, comps.get(n), lab, SYSTEM) for n in SYSTEM) + "</div>")
    parts.append(f'<div class="legend"><span><i class="sw why"></i>{esc(lab["why"])}</span>'
                 f'<span><i class="sw what"></i>{esc(lab["what"])}</span><span><i class="sw how"></i>{esc(lab["how"])}</span>'
                 f'<span>· {esc(lab["legend"])}: {esc(lab["fact"])} / {esc(lab["assumption"])} / {esc(lab["open"])}</span></div>')

    if data.get("next_step") or data.get("hypotheses"):
        parts.append(f'<section class="next"><h2>{esc(lab["next"])}</h2>')
        if data.get("next_step"):
            parts.append(f'<p>{esc(data["next_step"])}</p>')
        hyps = data.get("hypotheses") or []
        if hyps:
            parts.append(f'<table class="tbl"><tr><th>{esc(lab["hyp"])}</th><th>{esc(lab["metric"])}</th><th>{esc(lab["thr"])}</th></tr>'
                         + "".join(f'<tr><td>{esc(h.get("name"))}</td><td>{esc(h.get("metric"))}</td><td>{esc(h.get("threshold"))}</td></tr>' for h in hyps)
                         + "</table>")
        parts.append("</section>")
    parts.append(f"</div><script>{JS}</script></body></html>")
    return "".join(parts)


def main(argv=None):
    p = argparse.ArgumentParser(description="Render AI Product & System Canvas to HTML")
    p.add_argument("json_path", help="canvas JSON file ('-' for stdin)")
    p.add_argument("-o", "--out", default="canvas.html")
    a = p.parse_args(argv)
    data = json.load(sys.stdin if a.json_path == "-" else open(a.json_path, encoding="utf-8"))
    missing = [n for n in range(1, 11) if not (data.get("components") or {}).get(str(n), {}).get("text")]
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(render(data))
    print(f"Wrote {a.out}" + (f" (blocks without text: {missing})" if missing else ""))


if __name__ == "__main__":
    main()
