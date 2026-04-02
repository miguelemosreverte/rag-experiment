#!/usr/bin/env python3
"""
Apollo 11 Transcript Benchmark

Queries the 370K-token Apollo 11 air-to-ground transcript via the
Markov knowledge store, verifies answers against the actual transcript,
and generates a Markdown + JSON report.
"""

from __future__ import annotations

import json
import os
import platform
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LAZARUS_SRC = PROJECT_ROOT / "chuk-lazarus" / "src"
sys.path.insert(0, str(LAZARUS_SRC))

APOLLO_STORE = PROJECT_ROOT / "apollo11_store"
APOLLO_TEXT = PROJECT_ROOT / "apollo-demo" / "docs" / "apollo11_clean.txt"


@dataclass
class QueryResult:
    query: str
    category: str  # "factual", "verbatim", "interpretive"
    routed_windows: list[int] = field(default_factory=list)
    expansion_ms: float = 0.0
    route_ms: float = 0.0
    prefill_ms: float = 0.0
    generate_ms: float = 0.0
    total_ms: float = 0.0
    output: str = ""
    verification_terms: list[str] = field(default_factory=list)
    terms_found: list[str] = field(default_factory=list)
    terms_missing: list[str] = field(default_factory=list)
    grounded: bool = False


QUERIES = [
    {
        "query": "Quote verbatim what Houston said to Columbia when Eagle landed. Provide only the exact words from the transcript.",
        "category": "verbatim",
        "verify": ["Tranquility Base", "Eagle", "landed"],
    },
    {
        "query": "What did the astronauts describe seeing on the lunar surface? Quote their exact words about the color and texture.",
        "category": "verbatim",
        "verify": ["gray", "chalky", "basalt", "Sun angle"],
    },
    {
        "query": "Quote verbatim the goodnight message from Houston near the end of the mission.",
        "category": "verbatim",
        "verify": ["good night", "bed", "crew status"],
    },
    {
        "query": "What did the crew say about the chinch bugs? Quote the exact exchange from the transcript.",
        "category": "verbatim",
        "verify": ["chinch bugs", "mower"],
    },
    {
        "query": "What was the astronauts' impression of the lunar soil when they collected core tube samples? Quote their exact words.",
        "category": "verbatim",
        "verify": ["core tube", "moist", "packed"],
    },
    {
        "query": "What news from Earth was read to the astronauts during the mission? Quote the specific stories mentioned.",
        "category": "factual",
        "verify": ["crime-free", "Goddard", "London", "bookie"],
    },
    {
        "query": "What technical problems did the crew report during their EVA on the lunar surface?",
        "category": "factual",
        "verify": ["unfolded", "unevenly", "terrain"],
    },
    {
        "query": "Describe the astronauts' closing remarks before splashdown. What did they thank people for?",
        "category": "interpretive",
        "verify": ["spacecraft", "Saturn", "Columbia", "Eagle", "God bless"],
    },
    {
        "query": "What was the crew's experience with the television broadcast from the lunar surface?",
        "category": "factual",
        "verify": ["TV", "camera", "focus", "Earth"],
    },
    {
        "query": "How did the crew describe the process of collecting rock samples on the Moon?",
        "category": "factual",
        "verify": ["rock", "sample", "crater", "variety"],
    },
]


def run_apollo_benchmark(model_path: str):
    import mlx.core as mx
    from chuk_lazarus.inference.context.knowledge.store import KnowledgeStore
    from chuk_lazarus.cli.commands.knowledge._common import load_model

    sysinfo = {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "python": platform.python_version(),
        "model": model_path,
        "timestamp": datetime.now().isoformat(),
    }

    # Load model
    print("\n=== Loading model ===", file=sys.stderr)
    t0 = time.monotonic()
    _, kv_gen, tokenizer = load_model(model_path)
    model_load_s = time.monotonic() - t0

    # Load store
    print("=== Loading store ===", file=sys.stderr)
    store = KnowledgeStore.load(APOLLO_STORE)
    store.reload_index()
    store.log_stats()

    # Load transcript for verification
    transcript = APOLLO_TEXT.read_text(encoding="utf-8").lower()

    # Run queries
    print("\n=== Running queries ===\n", file=sys.stderr)
    results: list[QueryResult] = []
    stop_ids = {tokenizer.eos_token_id} if tokenizer.eos_token_id else set()

    for i, qdef in enumerate(QUERIES, 1):
        qr = QueryResult(
            query=qdef["query"],
            category=qdef["category"],
            verification_terms=qdef["verify"],
        )

        t0 = time.monotonic()

        # Expansion
        expansion_ids = KnowledgeStore._expand_query(qdef["query"], tokenizer, kv_gen)
        qr.expansion_ms = (time.monotonic() - t0) * 1000

        # Route
        t_route = time.monotonic()
        window_ids = store.route_top_k(qdef["query"], tokenizer, k=3, expansion_ids=expansion_ids)
        qr.route_ms = (time.monotonic() - t_route) * 1000
        qr.routed_windows = window_ids

        # Generate
        if window_ids:
            wid = window_ids[0]
            try:
                boundary = store.load_boundary(wid)
                boundary = boundary.reshape(1, 1, -1)
                has_boundary = True
            except (FileNotFoundError, ValueError):
                boundary = None
                has_boundary = False

            window_text = store.get_window_text(wid, tokenizer)
            if len(window_ids) > 1:
                for extra_wid in window_ids[1:]:
                    window_text += "\n\n---\n\n" + store.get_window_text(extra_wid, tokenizer)

            donor_content = f"{window_text}\n\n{qdef['query']}"
            try:
                ctx_ids = tokenizer.apply_chat_template(
                    [{"role": "user", "content": donor_content}],
                    add_generation_prompt=True,
                )
            except Exception:
                ctx_ids = tokenizer.encode(donor_content, add_special_tokens=True)

            ctx_mx = mx.array([ctx_ids])

            t_prefill = time.monotonic()
            if has_boundary:
                h = kv_gen.prefill_to_layer(ctx_mx, target_layer=store.config.crystal_layer,
                                            initial_residual=boundary)
                logits, _ = kv_gen.prefill_from_layer(h, start_layer=store.config.crystal_layer + 1)
                mx.eval(logits)
                _, kv_store = kv_gen.prefill(ctx_mx)
                mx.eval(*[t for p in kv_store for t in p])
                seq_len = ctx_mx.shape[1] + 1
            else:
                logits, kv_store = kv_gen.prefill(ctx_mx)
                mx.eval(logits)
                seq_len = ctx_mx.shape[1]

            qr.prefill_ms = (time.monotonic() - t_prefill) * 1000

            t_gen = time.monotonic()
            generated = []
            for _ in range(500):
                token = int(mx.argmax(logits[0, -1]).item())
                if token in stop_ids:
                    break
                generated.append(token)
                logits, kv_store = kv_gen.step_uncompiled(
                    mx.array([[token]]), kv_store, seq_len=seq_len)
                seq_len += 1
            qr.generate_ms = (time.monotonic() - t_gen) * 1000
            qr.output = tokenizer.decode(generated, skip_special_tokens=True)

        qr.total_ms = (time.monotonic() - t0) * 1000 + qr.expansion_ms

        # Verify: check if key terms from the actual transcript appear in the output
        output_lower = qr.output.lower()
        for term in qdef["verify"]:
            if term.lower() in output_lower or term.lower() in transcript:
                # Check if the model's output contains this term
                if term.lower() in output_lower:
                    qr.terms_found.append(term)
                else:
                    qr.terms_missing.append(term)

        qr.grounded = len(qr.terms_found) >= len(qdef["verify"]) * 0.5

        status = "GROUNDED" if qr.grounded else "WEAK"
        found_pct = len(qr.terms_found) / max(len(qdef["verify"]), 1) * 100
        print(f"  [{i:2d}] {status:8s} | {qr.category:12s} | terms={len(qr.terms_found)}/{len(qdef['verify'])} ({found_pct:.0f}%) | {qr.total_ms:.0f}ms",
              file=sys.stderr)
        print(f"       Found: {qr.terms_found}", file=sys.stderr)
        if qr.terms_missing:
            print(f"       Missing: {qr.terms_missing}", file=sys.stderr)

        results.append(qr)

    # Generate reports
    report_md = generate_md_report(sysinfo, model_load_s, results, store)
    report_json = generate_json_report(sysinfo, model_load_s, results, store)
    return report_md, report_json


def generate_md_report(sysinfo, model_load_s, results, store):
    lines = []
    lines.append("# Apollo 11 Transcript RAG Benchmark")
    lines.append("")
    lines.append(f"**Generated:** {sysinfo['timestamp']}")
    lines.append(f"**Model:** `{sysinfo['model'].split('/')[-1]}`")
    lines.append(f"**Document:** 370,778 tokens | 725 windows | Markov boundary reconstruction")
    lines.append(f"**Store:** {store.num_windows} windows, {len(store.entries):,} entries, {len(store.idf):,} IDF tokens")
    lines.append("")

    # Summary
    grounded = sum(1 for r in results if r.grounded)
    total = len(results)
    all_found = sum(len(r.terms_found) for r in results)
    all_expected = sum(len(r.verification_terms) for r in results)
    avg_ms = sum(r.total_ms for r in results) / total

    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Queries grounded | **{grounded}/{total} ({grounded/total*100:.0f}%)** |")
    lines.append(f"| Verification terms found | {all_found}/{all_expected} ({all_found/all_expected*100:.0f}%) |")
    lines.append(f"| Avg query time | {avg_ms:.0f}ms |")
    lines.append(f"| Model load time | {model_load_s:.1f}s |")
    lines.append("")

    # By category
    lines.append("### By Category")
    lines.append("")
    for cat in ["verbatim", "factual", "interpretive"]:
        subset = [r for r in results if r.category == cat]
        if subset:
            g = sum(1 for r in subset if r.grounded)
            lines.append(f"- **{cat.capitalize()}:** {g}/{len(subset)}")
    lines.append("")

    # Detail table
    lines.append("## Query Results")
    lines.append("")
    lines.append("| # | Category | Grounded | Terms | Time (ms) | Query |")
    lines.append("|---|----------|----------|-------|-----------|-------|")
    for i, r in enumerate(results, 1):
        icon = "yes" if r.grounded else "weak"
        q_short = r.query[:60] + "..." if len(r.query) > 60 else r.query
        lines.append(f"| {i} | {r.category} | {icon} | {len(r.terms_found)}/{len(r.verification_terms)} | {r.total_ms:.0f} | {q_short} |")
    lines.append("")

    # Timing
    lines.append("## Timing Breakdown")
    lines.append("")
    lines.append("| # | Expansion (ms) | Route (ms) | Prefill (ms) | Generate (ms) | Total (ms) |")
    lines.append("|---|---------------|------------|-------------|--------------|------------|")
    for i, r in enumerate(results, 1):
        lines.append(f"| {i} | {r.expansion_ms:.0f} | {r.route_ms:.0f} | {r.prefill_ms:.0f} | {r.generate_ms:.0f} | {r.total_ms:.0f} |")
    lines.append("")

    # Full outputs
    lines.append("## Full Query Outputs")
    lines.append("")
    for i, r in enumerate(results, 1):
        lines.append(f"### Query {i}: {r.query}")
        lines.append(f"- **Category:** {r.category} | **Windows:** {r.routed_windows}")
        lines.append(f"- **Verification:** {len(r.terms_found)}/{len(r.verification_terms)} terms found")
        lines.append(f"  - Found: {', '.join(r.terms_found) if r.terms_found else '(none)'}")
        if r.terms_missing:
            lines.append(f"  - Missing: {', '.join(r.terms_missing)}")
        lines.append(f"- **Output:**")
        lines.append("")
        # Indent output as blockquote
        for para in r.output.split("\n"):
            lines.append(f"> {para}")
        lines.append("")

    return "\n".join(lines)


def generate_json_report(sysinfo, model_load_s, results, store):
    grounded = sum(1 for r in results if r.grounded)
    total = len(results)
    all_found = sum(len(r.terms_found) for r in results)
    all_expected = sum(len(r.verification_terms) for r in results)

    return {
        "meta": {
            **sysinfo,
            "benchmark": "apollo11",
            "run_id": sysinfo["timestamp"].replace(":", "-").replace(".", "-"),
        },
        "document": {
            "tokens": 370778,
            "windows": store.num_windows,
            "entries": len(store.entries),
            "idf_tokens": len(store.idf),
        },
        "summary": {
            "grounded": grounded,
            "total": total,
            "grounded_pct": round(grounded / total * 100, 1),
            "terms_found": all_found,
            "terms_expected": all_expected,
            "terms_pct": round(all_found / max(all_expected, 1) * 100, 1),
            "avg_query_ms": round(sum(r.total_ms for r in results) / total, 0),
            "model_load_s": round(model_load_s, 2),
        },
        "queries": [
            {
                "query": r.query,
                "category": r.category,
                "grounded": r.grounded,
                "terms_found": r.terms_found,
                "terms_missing": r.terms_missing,
                "routed_windows": r.routed_windows,
                "expansion_ms": round(r.expansion_ms, 1),
                "route_ms": round(r.route_ms, 1),
                "prefill_ms": round(r.prefill_ms, 1),
                "generate_ms": round(r.generate_ms, 1),
                "total_ms": round(r.total_ms, 1),
                "output": r.output[:500],
            }
            for r in results
        ],
    }


if __name__ == "__main__":
    model_path = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Desktop/gemma-3-4b-it")

    print(f"Starting Apollo 11 benchmark with model: {model_path}", file=sys.stderr)
    report_md, report_json = run_apollo_benchmark(model_path)

    # Save
    runs_dir = Path(__file__).parent / "runs"
    runs_dir.mkdir(exist_ok=True)

    (runs_dir / "apollo11.md").write_text(report_md)
    (runs_dir / "apollo11.json").write_text(json.dumps(report_json, indent=2) + "\n")
    (Path(__file__).parent / "APOLLO_REPORT.md").write_text(report_md)

    print(f"\nReports written to benchmark/runs/apollo11.*", file=sys.stderr)
    print(report_md)
