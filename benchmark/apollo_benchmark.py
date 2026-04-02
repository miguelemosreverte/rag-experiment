#!/usr/bin/env python3
"""
Apollo 11 Transcript RAG Benchmark

Queries the 370K-token transcript, verifies against the source text,
and shows expected verbatim excerpts alongside model outputs.

Run modes:
  BENCH_APOLLO_MODE=improved  — our routing (stopwords + expansion + disambiguation)
  BENCH_APOLLO_MODE=vanilla   — basic route() with no expansion
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
    category: str
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
    expected_verbatim: str = ""


def find_verbatim_excerpt(transcript_lines: list[str], search_terms: list[str], context: int = 5) -> str:
    """Find the best excerpt from the transcript containing the search terms."""
    best_excerpt = ""
    best_score = 0
    transcript_lower = [l.lower() for l in transcript_lines]

    for i, line in enumerate(transcript_lower):
        score = sum(1 for term in search_terms if term.lower() in line)
        if score > best_score:
            best_score = score
            start = max(0, i - context)
            end = min(len(transcript_lines), i + context + 1)
            best_excerpt = "\n".join(transcript_lines[start:end]).strip()

    # If single line didn't match enough, try scanning windows
    if best_score < 2:
        for i in range(0, len(transcript_lower) - 10):
            window = " ".join(transcript_lower[i:i+10])
            score = sum(1 for term in search_terms if term.lower() in window)
            if score > best_score:
                best_score = score
                start = max(0, i - 2)
                end = min(len(transcript_lines), i + 12)
                best_excerpt = "\n".join(transcript_lines[start:end]).strip()

    return best_excerpt


QUERIES = [
    {
        "query": "Quote verbatim what Houston said to Columbia when Eagle landed at Tranquility Base.",
        "category": "verbatim",
        "verify": ["Tranquility", "Eagle", "landed"],
        "grep_terms": ["landed", "Tranquility Base", "Eagle is at"],
    },
    {
        "query": "What did the astronauts describe about the color of the lunar surface? Quote their exact words.",
        "category": "verbatim",
        "verify": ["gray", "chalky", "basalt", "Sun angle"],
        "grep_terms": ["chalky gray", "zero-phase", "country basalt"],
    },
    {
        "query": "Quote verbatim the last goodnight message from Houston to the crew.",
        "category": "verbatim",
        "verify": ["good night", "put you to bed", "crew status"],
        "grep_terms": ["put you to bed", "good night", "crew status"],
    },
    {
        "query": "What did the crew say about the chinch bugs? Quote the exact words.",
        "category": "verbatim",
        "verify": ["chinch bugs", "mower", "taciturn"],
        "grep_terms": ["chinch bugs", "mower", "taciturn"],
    },
    {
        "query": "What was the astronauts' impression of the lunar soil from the core tube samples? Quote their exact words.",
        "category": "verbatim",
        "verify": ["core tube", "moist", "packed"],
        "grep_terms": ["core tube", "moist", "packed"],
    },
    {
        "query": "What news stories from Earth were read to the astronauts? Quote the stories about Mrs. Goddard and the London bookie.",
        "category": "factual",
        "verify": ["crime-free", "Goddard", "London", "bookie"],
        "grep_terms": ["Goddard", "crime-free night", "bookie"],
    },
    {
        "query": "What technical problems did the crew report about equipment that unfolded unevenly on the lunar surface?",
        "category": "factual",
        "verify": ["unfolded", "unevenly", "terrain", "indentation"],
        "grep_terms": ["unfolded", "unevenly", "terrain"],
    },
    {
        "query": "Quote the astronauts' closing remarks where they thanked the people who built the spacecraft, mentioning Saturn, Columbia, and Eagle.",
        "category": "verbatim",
        "verify": ["Saturn", "Columbia", "Eagle", "God bless"],
        "grep_terms": ["Saturn", "Columbia", "Eagle", "God bless"],
    },
    {
        "query": "What happened with the television camera on the lunar surface? Quote what Houston said about seeing the Eagle and Earth.",
        "category": "factual",
        "verify": ["TV", "camera", "focus", "Earth", "eagle"],
        "grep_terms": ["see the eagle", "focus", "Earth in the background"],
    },
    {
        "query": "How did Neil describe collecting rock samples around the elongate double crater?",
        "category": "factual",
        "verify": ["rock", "sample", "crater", "variety", "exhaust"],
        "grep_terms": ["elongate double crater", "different types of rock", "exhaust"],
    },
]


def run_apollo_benchmark(model_path: str):
    import mlx.core as mx
    from chuk_lazarus.inference.context.knowledge.store import KnowledgeStore
    from chuk_lazarus.cli.commands.knowledge._common import load_model

    mode = os.environ.get("BENCH_APOLLO_MODE", "improved")

    sysinfo = {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "python": platform.python_version(),
        "model": model_path,
        "timestamp": datetime.now().isoformat(),
        "routing_mode": mode,
    }

    print(f"\n=== Apollo 11 Benchmark (mode={mode}) ===", file=sys.stderr)

    # Load model
    t0 = time.monotonic()
    _, kv_gen, tokenizer = load_model(model_path)
    model_load_s = time.monotonic() - t0

    # Load store
    store = KnowledgeStore.load(APOLLO_STORE)
    store.reload_index()
    store.log_stats()

    # Load transcript for verification
    transcript_text = APOLLO_TEXT.read_text(encoding="utf-8")
    transcript_lines = transcript_text.split("\n")

    # Run queries
    print(f"\n=== Running {len(QUERIES)} queries ===\n", file=sys.stderr)
    results: list[QueryResult] = []
    stop_ids = {tokenizer.eos_token_id} if tokenizer.eos_token_id else set()

    for i, qdef in enumerate(QUERIES, 1):
        qr = QueryResult(
            query=qdef["query"],
            category=qdef["category"],
            verification_terms=qdef["verify"],
        )

        # Find expected verbatim from transcript
        qr.expected_verbatim = find_verbatim_excerpt(
            transcript_lines, qdef["grep_terms"], context=6
        )

        t0 = time.monotonic()

        if mode == "improved":
            # Full improved routing: expansion + stopwords + disambiguation
            expansion_ids = KnowledgeStore._expand_query(qdef["query"], tokenizer, kv_gen)
            qr.expansion_ms = (time.monotonic() - t0) * 1000
            t_route = time.monotonic()
            window_ids = store.route_top_k(qdef["query"], tokenizer, k=3, expansion_ids=expansion_ids)
            qr.route_ms = (time.monotonic() - t_route) * 1000
        else:
            # Vanilla: basic route, no expansion
            qr.expansion_ms = 0.0
            t_route = time.monotonic()
            wid = store.route(qdef["query"], tokenizer=tokenizer)
            window_ids = [wid] if wid is not None else []
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

        # Verify
        output_lower = qr.output.lower()
        for term in qdef["verify"]:
            if term.lower() in output_lower:
                qr.terms_found.append(term)
            else:
                qr.terms_missing.append(term)

        qr.grounded = len(qr.terms_found) >= len(qdef["verify"]) * 0.5

        status = "GROUNDED" if qr.grounded else "WEAK"
        print(f"  [{i:2d}] {status:8s} | {qr.category:12s} | terms={len(qr.terms_found)}/{len(qr.verification_terms)} | {qr.total_ms:.0f}ms",
              file=sys.stderr)
        results.append(qr)

        # Live update: write partial JSON + regenerate HTML after each query
        partial_json = generate_json_report(sysinfo, model_load_s, results, store, mode)
        label = f"apollo11_{mode}"
        runs_dir = Path(__file__).parent / "runs"
        runs_dir.mkdir(exist_ok=True)
        (runs_dir / f"{label}.json").write_text(json.dumps(partial_json, indent=2) + "\n")
        partial_md = generate_md_report(sysinfo, model_load_s, results, store, mode)
        (runs_dir / f"{label}.md").write_text(partial_md)
        # Regenerate HTML
        import subprocess
        subprocess.run(["node", str(Path(__file__).parent.parent / "docs" / "md2html.js")],
                       capture_output=True, cwd=str(Path(__file__).parent.parent))

    # Generate reports
    report_md = generate_md_report(sysinfo, model_load_s, results, store, mode)
    report_json = generate_json_report(sysinfo, model_load_s, results, store, mode)
    return report_md, report_json, mode


def generate_md_report(sysinfo, model_load_s, results, store, mode):
    lines = []
    lines.append("# Apollo 11 Transcript RAG Benchmark")
    lines.append("")
    lines.append(f"**Generated:** {sysinfo['timestamp']}")
    lines.append(f"**Model:** `{sysinfo['model'].split('/')[-1]}`")
    lines.append(f"**Routing:** `{mode}`")
    lines.append(f"**Document:** 370,778 tokens | 725 windows | Markov boundary reconstruction")
    lines.append("")

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
    lines.append(f"| Avg query time | {avg_ms/1000:.1f}s |")
    lines.append("")

    # Full outputs with expected verbatim
    lines.append("## Query Results with Source Verification")
    lines.append("")
    for i, r in enumerate(results, 1):
        icon = "GROUNDED" if r.grounded else "WEAK"
        lines.append(f"### Query {i}: {r.query}")
        lines.append(f"**{r.category}** | **{icon}** | Terms: {len(r.terms_found)}/{len(r.verification_terms)} | Windows: {r.routed_windows} | {r.total_ms/1000:.1f}s")
        lines.append("")
        if r.terms_found:
            lines.append(f"Found: {', '.join(r.terms_found)}")
        if r.terms_missing:
            lines.append(f"Missing: {', '.join(r.terms_missing)}")
        lines.append("")
        lines.append("**Expected (from transcript):**")
        lines.append("```")
        lines.append(r.expected_verbatim[:600] if r.expected_verbatim else "(not found)")
        lines.append("```")
        lines.append("")
        lines.append("**Model output:**")
        lines.append(f"> {r.output[:500]}")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def generate_json_report(sysinfo, model_load_s, results, store, mode):
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
            "routing_mode": mode,
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
                "output": r.output[:800],
                "expected_verbatim": r.expected_verbatim[:600],
            }
            for r in results
        ],
    }


if __name__ == "__main__":
    model_path = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Desktop/gemma-3-4b-it")
    mode = os.environ.get("BENCH_APOLLO_MODE", "improved")

    report_md, report_json, mode = run_apollo_benchmark(model_path)

    runs_dir = Path(__file__).parent / "runs"
    runs_dir.mkdir(exist_ok=True)

    label = f"apollo11_{mode}"
    (runs_dir / f"{label}.md").write_text(report_md)
    (runs_dir / f"{label}.json").write_text(json.dumps(report_json, indent=2) + "\n")

    print(f"\nReports: benchmark/runs/{label}.*", file=sys.stderr)
    print(report_md)
