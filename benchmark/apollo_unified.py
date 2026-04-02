#!/usr/bin/env python3
"""
Apollo 11 Unified Benchmark — Same 10 queries, 3 routing methods, side-by-side.

1. Official lazarus CLI (fresh model per query)
2. Our improved routing (stopwords + expansion + disambiguation)
3. Vanilla baseline (basic TF-IDF, no expansion)

Outputs JSON + Markdown + regenerates HTML after each query.
"""

from __future__ import annotations

import json
import os
import platform
import re
import subprocess
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
MODEL_PATH = os.path.expanduser("~/Desktop/gemma-3-4b-it")


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
        "query": "Quote the astronauts' farewell message where they said God bless you and good night from Apollo 11.",
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


def find_verbatim_excerpt(transcript_lines, search_terms, context=6):
    best_excerpt = ""
    best_score = 0
    transcript_lower = [l.lower() for l in transcript_lines]
    for i in range(0, len(transcript_lower) - 10):
        window = " ".join(transcript_lower[i:i+10])
        score = sum(1 for term in search_terms if term.lower() in window)
        if score > best_score:
            best_score = score
            start = max(0, i - 2)
            end = min(len(transcript_lines), i + 12)
            best_excerpt = "\n".join(transcript_lines[start:end]).strip()
    return best_excerpt


def verify_output(output, verify_terms):
    output_lower = output.lower()
    found = [t for t in verify_terms if t.lower() in output_lower]
    missing = [t for t in verify_terms if t.lower() not in output_lower]
    grounded = len(found) >= len(verify_terms) * 0.5
    return found, missing, grounded


def run_cli_query(query, max_tokens=300):
    """Run a single query via the lazarus CLI as a subprocess.

    Uses the currently installed code (whatever version of store.py is active).
    """
    env = os.environ.copy()
    env["PATH"] = os.path.expanduser("~/.local/bin") + ":" + env.get("PATH", "")
    env["PYTHONPATH"] = str(LAZARUS_SRC)
    cmd = [
        sys.executable, "-m", "chuk_lazarus.cli.main",
        "knowledge", "query",
        "-m", MODEL_PATH,
        "-s", str(APOLLO_STORE),
        "-p", query,
        "--max-tokens", str(max_tokens),
    ]
    t0 = time.monotonic()
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=300,
        cwd=str(PROJECT_ROOT),
        env=env,
    )
    elapsed_ms = (time.monotonic() - t0) * 1000
    output = result.stdout.strip()
    stderr = result.stderr
    route_ms = 0
    for line in stderr.split("\n"):
        if "Routed to" in line:
            m = re.search(r"\(([\d.]+) ms\)", line)
            if m:
                route_ms = float(m.group(1))
    return output, elapsed_ms, route_ms, stderr


def run_benchmark_query(query, store, kv_gen, tokenizer, mode="improved"):
    """Run a query through our benchmark code."""
    import mlx.core as mx
    from chuk_lazarus.inference.context.knowledge.store import KnowledgeStore

    stop_ids = {tokenizer.eos_token_id} if tokenizer.eos_token_id else set()
    t0 = time.monotonic()

    if mode == "improved":
        expansion_ids = KnowledgeStore._expand_query(query, tokenizer, kv_gen)
        expansion_ms = (time.monotonic() - t0) * 1000
        t_route = time.monotonic()
        window_ids = store.route_top_k(query, tokenizer, k=3, expansion_ids=expansion_ids)
        route_ms = (time.monotonic() - t_route) * 1000
    else:
        expansion_ms = 0
        t_route = time.monotonic()
        wid = store.route(query, tokenizer=tokenizer)
        window_ids = [wid] if wid is not None else []
        route_ms = (time.monotonic() - t_route) * 1000

    output = ""
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

        donor_content = f"{window_text}\n\n{query}"
        try:
            ctx_ids = tokenizer.apply_chat_template(
                [{"role": "user", "content": donor_content}],
                add_generation_prompt=True,
            )
        except Exception:
            ctx_ids = tokenizer.encode(donor_content, add_special_tokens=True)

        ctx_mx = mx.array([ctx_ids])
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

        generated = []
        for _ in range(300):
            token = int(mx.argmax(logits[0, -1]).item())
            if token in stop_ids:
                break
            generated.append(token)
            logits, kv_store = kv_gen.step_uncompiled(
                mx.array([[token]]), kv_store, seq_len=seq_len)
            seq_len += 1
        output = tokenizer.decode(generated, skip_special_tokens=True)

    total_ms = (time.monotonic() - t0) * 1000
    return output, total_ms, window_ids


def swap_to_upstream():
    """Temporarily checkout upstream store.py and route.py."""
    lazarus_dir = PROJECT_ROOT / "chuk-lazarus"
    files = [
        "src/chuk_lazarus/inference/context/knowledge/store.py",
        "src/chuk_lazarus/inference/context/knowledge/route.py",
        "src/chuk_lazarus/cli/commands/knowledge/_query.py",
        "src/chuk_lazarus/cli/commands/knowledge/_chat.py",
    ]
    for f in files:
        subprocess.run(["git", "checkout", "origin/main", "--", f],
                       cwd=str(lazarus_dir), capture_output=True)


def swap_to_improved():
    """Restore our improved code."""
    lazarus_dir = PROJECT_ROOT / "chuk-lazarus"
    subprocess.run(["git", "checkout", "HEAD", "--", "src/"],
                   cwd=str(lazarus_dir), capture_output=True)


def live_update(sysinfo, all_results):
    """Write JSON + MD + regenerate HTML."""
    runs_dir = Path(__file__).parent / "runs"
    runs_dir.mkdir(exist_ok=True)
    report = build_json_report(sysinfo, all_results)
    (runs_dir / "apollo11_unified.json").write_text(json.dumps(report, indent=2) + "\n")
    md = build_md_report(sysinfo, all_results)
    (runs_dir / "apollo11_unified.md").write_text(md)
    subprocess.run(["node", str(PROJECT_ROOT / "docs" / "md2html.js")],
                   capture_output=True, cwd=str(PROJECT_ROOT))
    return md


def main():
    from chuk_lazarus.inference.context.knowledge.store import KnowledgeStore
    from chuk_lazarus.cli.commands.knowledge._common import load_model

    transcript_lines = APOLLO_TEXT.read_text(encoding="utf-8").split("\n")

    sysinfo = {
        "platform": platform.platform(),
        "timestamp": datetime.now().isoformat(),
        "model": MODEL_PATH.split("/")[-1],
    }

    all_results = []

    # Pre-compute expected verbatim for all queries
    for qdef in QUERIES:
        expected = find_verbatim_excerpt(transcript_lines, qdef["grep_terms"])
        all_results.append({
            "query": qdef["query"],
            "category": qdef["category"],
            "verify_terms": qdef["verify"],
            "expected_verbatim": expected[:600],
            "results": {},
        })

    # ══════════════════════════════════════════════════════════════════
    # Phase 1: Improved routing (our code, in-process)
    # ══════════════════════════════════════════════════════════════════
    print("\n=== Phase 1: IMPROVED routing ===", file=sys.stderr)
    print("=== Loading model ===", file=sys.stderr)
    _, kv_gen, tokenizer = load_model(MODEL_PATH)
    store = KnowledgeStore.load(APOLLO_STORE)
    store.reload_index()

    for i, qdef in enumerate(QUERIES):
        print(f"  [IMP] Query {i+1}/10...", file=sys.stderr)
        store.reload_index()
        output, ms, windows = run_benchmark_query(qdef["query"], store, kv_gen, tokenizer, "improved")
        found, missing, grounded = verify_output(output, qdef["verify"])
        all_results[i]["results"]["improved"] = {
            "output": output[:800],
            "total_ms": round(ms, 0),
            "windows": windows,
            "terms_found": found,
            "terms_missing": missing,
            "grounded": grounded,
        }
        status = "GROUNDED" if grounded else "WEAK"
        print(f"  [IMP] {status:8s} | terms={len(found)}/{len(qdef['verify'])} | {ms/1000:.1f}s", file=sys.stderr)
        live_update(sysinfo, all_results)

    # ══════════════════════════════════════════════════════════════════
    # Phase 2: Vanilla routing (our code, basic route, in-process)
    # ══════════════════════════════════════════════════════════════════
    print("\n=== Phase 2: VANILLA routing ===", file=sys.stderr)

    for i, qdef in enumerate(QUERIES):
        print(f"  [VAN] Query {i+1}/10...", file=sys.stderr)
        store.reload_index()
        output, ms, windows = run_benchmark_query(qdef["query"], store, kv_gen, tokenizer, "vanilla")
        found, missing, grounded = verify_output(output, qdef["verify"])
        all_results[i]["results"]["vanilla"] = {
            "output": output[:800],
            "total_ms": round(ms, 0),
            "windows": windows,
            "terms_found": found,
            "terms_missing": missing,
            "grounded": grounded,
        }
        status = "GROUNDED" if grounded else "WEAK"
        print(f"  [VAN] {status:8s} | terms={len(found)}/{len(qdef['verify'])} | {ms/1000:.1f}s", file=sys.stderr)
        live_update(sysinfo, all_results)

    # Free model memory before CLI phase
    del kv_gen, tokenizer, store
    import gc; gc.collect()
    try:
        import mlx.core as mx; mx.metal.clear_cache()
    except Exception:
        pass

    # ══════════════════════════════════════════════════════════════════
    # Phase 3: Upstream original (swap code, run via CLI subprocess)
    # Each CLI call loads model fresh — only one instance at a time.
    # ══════════════════════════════════════════════════════════════════
    print("\n=== Phase 3: UPSTREAM ORIGINAL (via CLI) ===", file=sys.stderr)
    print("  Swapping to upstream code...", file=sys.stderr)
    swap_to_upstream()

    for i, qdef in enumerate(QUERIES):
        print(f"  [ORI] Query {i+1}/10...", file=sys.stderr)
        output, ms, route_ms, stderr = run_cli_query(qdef["query"])
        found, missing, grounded = verify_output(output, qdef["verify"])
        all_results[i]["results"]["original"] = {
            "output": output[:800],
            "total_ms": round(ms, 0),
            "terms_found": found,
            "terms_missing": missing,
            "grounded": grounded,
        }
        status = "GROUNDED" if grounded else "WEAK"
        print(f"  [ORI] {status:8s} | terms={len(found)}/{len(qdef['verify'])} | {ms/1000:.1f}s", file=sys.stderr)
        live_update(sysinfo, all_results)

    # Restore our code
    print("  Restoring improved code...", file=sys.stderr)
    swap_to_improved()

    md = live_update(sysinfo, all_results)
    print(f"\n\n=== DONE ===", file=sys.stderr)
    print(md)


def build_json_report(sysinfo, results):
    methods = ["improved", "vanilla", "original"]
    summary = {}
    for m in methods:
        grounded = sum(1 for r in results if r["results"].get(m, {}).get("grounded", False))
        total_terms = sum(len(r["results"].get(m, {}).get("terms_found", [])) for r in results)
        expected_terms = sum(len(r["verify_terms"]) for r in results)
        avg_ms = sum(r["results"].get(m, {}).get("total_ms", 0) for r in results) / max(len(results), 1)
        summary[m] = {
            "grounded": grounded,
            "total": len(results),
            "grounded_pct": round(grounded / max(len(results), 1) * 100, 1),
            "terms_found": total_terms,
            "terms_expected": expected_terms,
            "terms_pct": round(total_terms / max(expected_terms, 1) * 100, 1),
            "avg_query_ms": round(avg_ms, 0),
        }

    return {
        "meta": {**sysinfo, "benchmark": "apollo11_unified"},
        "document": {"tokens": 370778, "windows": 725},
        "summary": summary,
        "queries": results,
    }


def build_md_report(sysinfo, results):
    methods = ["improved", "vanilla", "original"]
    labels = {"improved": "Our Improved", "vanilla": "Vanilla (no expansion)", "original": "Upstream Original"}
    lines = ["# Apollo 11 Unified Benchmark", ""]
    lines.append(f"**{sysinfo['timestamp']}** | **{sysinfo['model']}** | 370,778 tokens | 725 windows")
    lines.append("")

    # Summary table
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Official CLI | Our Improved | Vanilla Baseline |")
    lines.append("|--------|-------------|-------------|-----------------|")

    for metric_label, key in [("Grounded", "grounded"), ("Terms found", "terms_pct"), ("Avg query", "avg_query_ms")]:
        row = f"| {metric_label} |"
        for m in methods:
            g = sum(1 for r in results if r["results"].get(m, {}).get("grounded", False))
            t = len(results)
            tf = sum(len(r["results"].get(m, {}).get("terms_found", [])) for r in results)
            te = sum(len(r["verify_terms"]) for r in results)
            avg = sum(r["results"].get(m, {}).get("total_ms", 0) for r in results) / max(t, 1)
            if key == "grounded":
                row += f" **{g}/{t}** |"
            elif key == "terms_pct":
                row += f" {tf}/{te} ({tf/max(te,1)*100:.0f}%) |"
            else:
                row += f" {avg/1000:.1f}s |"
        lines.append(row)
    lines.append("")

    # Per-query comparison
    for i, entry in enumerate(results, 1):
        lines.append(f"---")
        lines.append(f"### Query {i}: {entry['query']}")
        lines.append(f"**{entry['category']}** | Verify: {', '.join(entry['verify_terms'])}")
        lines.append("")
        lines.append("**Expected (transcript):**")
        lines.append(f"```\n{entry['expected_verbatim'][:400]}\n```")
        lines.append("")
        for m in methods:
            r = entry["results"].get(m, {})
            status = "GROUNDED" if r.get("grounded") else "WEAK"
            found = r.get("terms_found", [])
            lines.append(f"**{labels[m]}** ({status}, {len(found)}/{len(entry['verify_terms'])} terms, {r.get('total_ms',0)/1000:.1f}s):")
            lines.append(f"> {r.get('output','')[:400]}")
            lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
