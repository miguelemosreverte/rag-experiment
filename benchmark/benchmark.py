#!/usr/bin/env python3
"""
Benchmark: Dynamic Skill Append + Query Routing

Tests the full pipeline:
1. Initialize store with base state from system prompt
2. Append 10 skills one by one, measuring timing/memory/CPU per append
3. Run 10 queries with ramping difficulty, verify routing accuracy
4. Output a Markdown report with all metrics
"""

from __future__ import annotations

import gc
import json
import os
import platform
import resource
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# ── Add chuk-lazarus to path ─────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LAZARUS_SRC = PROJECT_ROOT / "chuk-lazarus" / "src"
sys.path.insert(0, str(LAZARUS_SRC))


# ── Metrics collection ───────────────────────────────────────────────

def get_memory_mb() -> float:
    """Get current process RSS in MB."""
    ru = resource.getrusage(resource.RUSAGE_SELF)
    return ru.ru_maxrss / (1024 * 1024)  # macOS reports bytes


def get_metal_memory_mb() -> float:
    """Get MLX Metal memory usage in MB."""
    try:
        import mlx.core as mx
        info = mx.metal.device_info()
        # Try to get current allocated memory
        peak = mx.metal.get_peak_memory() / (1024 * 1024)
        return peak
    except Exception:
        return 0.0


@dataclass
class AppendMetrics:
    skill_name: str
    skill_file: str
    num_tokens: int = 0
    num_windows: int = 0
    num_entries: int = 0
    elapsed_s: float = 0.0
    rss_before_mb: float = 0.0
    rss_after_mb: float = 0.0
    metal_peak_mb: float = 0.0


@dataclass
class QueryMetrics:
    query: str
    expected_skill: str
    difficulty: str  # "easy", "medium", "hard"
    routed_windows: list[int] = field(default_factory=list)
    routed_skill: str = ""
    correct: bool = False
    expansion_ms: float = 0.0
    route_ms: float = 0.0
    prefill_ms: float = 0.0
    generate_ms: float = 0.0
    total_ms: float = 0.0
    output_snippet: str = ""


# ── Skill definitions ────────────────────────────────────────────────

SKILLS = [
    ("01_weather_api.md", "weather_api"),
    ("02_sql_query.md", "sql_query"),
    ("03_image_generation.md", "image_generation"),
    ("04_calendar.md", "calendar"),
    ("05_file_converter.md", "file_converter"),
    ("06_git_operations.md", "git_operations"),
    ("07_email_sender.md", "email_sender"),
    ("08_notification_service.md", "notification_service"),
    ("09_data_visualization.md", "data_visualization"),
    ("10_deployment_pipeline.md", "deployment_pipeline"),
]

# ── Queries with expected routing and difficulty ─────────────────────
# Easy: unambiguous, single clear skill
# Medium: could match 2 skills but one is clearly better
# Hard: deliberately ambiguous, overlapping skills

QUERIES = [
    # Easy — distinct skills
    {
        "query": "What's the temperature in Tokyo right now?",
        "expected": "weather_api",
        "difficulty": "easy",
    },
    {
        "query": "Show me all users who signed up last week from the database",
        "expected": "sql_query",
        "difficulty": "easy",
    },
    {
        "query": "Generate a watercolor painting of a mountain landscape at sunrise",
        "expected": "image_generation",
        "difficulty": "easy",
    },
    {
        "query": "Schedule a meeting with the design team next Thursday at 2pm",
        "expected": "calendar",
        "difficulty": "easy",
    },
    {
        "query": "Convert this DOCX report to PDF with A4 page size",
        "expected": "file_converter",
        "difficulty": "easy",
    },
    {
        "query": "Create a new git branch called feature/payments and switch to it",
        "expected": "git_operations",
        "difficulty": "easy",
    },
    # Medium — one is clearly better but another is plausible
    {
        "query": "Send an email to the client with the monthly report PDF attached",
        "expected": "email_sender",
        "difficulty": "medium",
        # Could match notification_service (which also does email) but email_sender is more specific
    },
    {
        "query": "Create a bar chart showing revenue by month from the sales database",
        "expected": "data_visualization",
        "difficulty": "medium",
        # Could match sql_query (it queries a database) but visualization is the primary intent
    },
    # Hard — deliberately ambiguous
    {
        "query": "Send a notification to the team that the deploy succeeded and include a link",
        "expected": "notification_service",
        "difficulty": "hard",
        # Overlaps with: email_sender (sends messages), deployment_pipeline (has notifications),
        # and notification_service (the actual notification hub)
    },
    {
        "query": "After deploying to staging, email the QA team and send a Slack alert to engineering",
        "expected": "deployment_pipeline",
        "difficulty": "hard",
        # Overlaps with: deployment_pipeline (deploys + notifies), notification_service (multi-channel),
        # email_sender (email). The deployment context should win.
    },
]


# ── Main benchmark ───────────────────────────────────────────────────

def run_benchmark(model_path: str) -> str:
    """Run the full benchmark and return a Markdown report."""
    import mlx.core as mx

    from chuk_lazarus.inference.context.knowledge import ArchitectureConfig
    from chuk_lazarus.inference.context.knowledge.append import (
        append_skill,
        build_base_state,
    )
    from chuk_lazarus.inference.context.knowledge.store import KnowledgeStore
    from chuk_lazarus.inference.context.knowledge.route import TFIDFRouter
    from chuk_lazarus.cli.commands.knowledge._common import load_model

    skills_dir = Path(__file__).parent / "skills"
    store_path = Path(__file__).parent / "bench_store"
    system_prompt_path = Path(__file__).parent / "system_prompt.txt"

    # Clean previous run
    if store_path.exists():
        import shutil
        shutil.rmtree(store_path)

    # ── System info ───────────────────────────────────────────────────
    sysinfo = {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "python": platform.python_version(),
        "model": model_path,
        "timestamp": datetime.now().isoformat(),
    }

    # ── Load model (once) ─────────────────────────────────────────────
    print("\n=== Loading model ===", file=sys.stderr)
    t_model = time.monotonic()
    pipeline, kv_gen, tokenizer = load_model(model_path)
    model_load_s = time.monotonic() - t_model
    ac = ArchitectureConfig.from_model_config(pipeline.config)
    rss_after_model = get_memory_mb()

    print(f"  Model loaded in {model_load_s:.1f}s, RSS: {rss_after_model:.0f} MB",
          file=sys.stderr)

    # ── Phase 1: Init base state ──────────────────────────────────────
    print("\n=== Initializing base state ===", file=sys.stderr)
    system_prompt = system_prompt_path.read_text()
    t_init = time.monotonic()
    build_base_state(kv_gen, tokenizer, system_prompt, ac, store_path)
    init_s = time.monotonic() - t_init
    print(f"  Base state created in {init_s:.2f}s", file=sys.stderr)

    # ── Phase 2: Append skills ────────────────────────────────────────
    print("\n=== Appending skills ===", file=sys.stderr)
    append_metrics: list[AppendMetrics] = []

    for filename, skill_name in SKILLS:
        filepath = skills_dir / filename
        if not filepath.exists():
            print(f"  SKIP: {filename} not found", file=sys.stderr)
            continue

        m = AppendMetrics(skill_name=skill_name, skill_file=filename)
        m.rss_before_mb = get_memory_mb()

        try:
            mx.metal.reset_peak_memory()
        except Exception:
            pass

        print(f"\n  --- Appending: {filename} ---", file=sys.stderr)
        t0 = time.monotonic()

        result = append_skill(
            kv_gen=kv_gen,
            tokenizer=tokenizer,
            store_path=store_path,
            new_doc_path=filepath,
            config=ac,
        )

        m.elapsed_s = time.monotonic() - t0
        m.rss_after_mb = get_memory_mb()
        m.metal_peak_mb = get_metal_memory_mb()
        m.num_tokens = result["num_new_tokens"]
        m.num_windows = result["num_new_windows"]
        m.num_entries = result["num_new_entries"]
        append_metrics.append(m)

    # ── Phase 3: Query routing ────────────────────────────────────────
    print("\n\n=== Running queries ===", file=sys.stderr)

    store = KnowledgeStore.load(store_path)
    store.reload_index()

    # Build a mapping: window_id → skill_name
    # Each skill's windows are contiguous, so we track ranges
    window_skill_map: dict[int, str] = {}
    wid = 0
    for filename, skill_name in SKILLS:
        filepath = skills_dir / filename
        text = filepath.read_text()
        tokens = tokenizer.encode(text, add_special_tokens=False)
        n_windows = max(1, -(-len(tokens) // ac.window_size))
        for w in range(n_windows):
            window_skill_map[wid] = skill_name
            wid += 1

    # Note: window 0 offset — base state init doesn't create windows,
    # appended skills start at window 0
    # Let's re-derive from the store's actual window_token_lists
    # The skills were appended in order, so windows are sequential

    query_metrics: list[QueryMetrics] = []

    for qdef in QUERIES:
        qm = QueryMetrics(
            query=qdef["query"],
            expected_skill=qdef["expected"],
            difficulty=qdef["difficulty"],
        )

        t0 = time.monotonic()

        routing_method = os.environ.get("BENCH_ROUTING_METHOD", "tfidf_expansion")

        if routing_method == "cosine":
            # Cosine similarity routing — no expansion needed
            qm.expansion_ms = 0.0
            t_route = time.monotonic()
            window_ids = store.route_cosine(
                qdef["query"], tokenizer, kv_gen, k=3
            )
            qm.route_ms = (time.monotonic() - t_route) * 1000
        else:
            # TF-IDF + expansion routing
            expansion_ids = KnowledgeStore._expand_query(qdef["query"], tokenizer, kv_gen)
            qm.expansion_ms = (time.monotonic() - t0) * 1000

            sw = store._build_stopword_ids(tokenizer)
            exp_words = sorted({tokenizer.decode([t]).strip().lower()
                               for t in expansion_ids
                               if store.idf.get(t, 0.0) > 0 and t not in sw
                               and len(tokenizer.decode([t]).strip()) >= 2})
            print(f"    Expansion: {exp_words[:10]}", file=sys.stderr)

            t_route = time.monotonic()
            window_ids = store.route_top_k(
                qdef["query"], tokenizer, k=3, expansion_ids=expansion_ids
            )
            qm.route_ms = (time.monotonic() - t_route) * 1000

        qm.routed_windows = window_ids

        # Determine which skill was routed to
        if window_ids:
            primary_wid = window_ids[0]
            qm.routed_skill = window_skill_map.get(primary_wid, f"unknown_window_{primary_wid}")
            # Correct if expected skill appears in ANY of the top-k windows
            routed_skills = [window_skill_map.get(w, "") for w in window_ids]
            qm.correct = qdef["expected"] in routed_skills

        # Full query with generation
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
                h = kv_gen.prefill_to_layer(
                    ctx_mx, target_layer=store.config.crystal_layer,
                    initial_residual=boundary,
                )
                logits, _ = kv_gen.prefill_from_layer(h, start_layer=store.config.crystal_layer + 1)
                mx.eval(logits)
                _, kv_store = kv_gen.prefill(ctx_mx)
                mx.eval(*[t for p in kv_store for t in p])
                seq_len = ctx_mx.shape[1] + 1
            else:
                logits, kv_store = kv_gen.prefill(ctx_mx)
                mx.eval(logits)
                seq_len = ctx_mx.shape[1]

            qm.prefill_ms = (time.monotonic() - t_prefill) * 1000

            # Generate
            t_gen = time.monotonic()
            generated = []
            for _ in range(100):
                token = int(mx.argmax(logits[0, -1]).item())
                eos = tokenizer.eos_token_id
                if eos is not None and token == eos:
                    break
                generated.append(token)
                logits, kv_store = kv_gen.step_uncompiled(
                    mx.array([[token]]), kv_store, seq_len=seq_len
                )
                seq_len += 1

            qm.generate_ms = (time.monotonic() - t_gen) * 1000

        qm.total_ms = (time.monotonic() - t0) * 1000
        qm.output_snippet = tokenizer.decode(generated, skip_special_tokens=True)[:200] if window_ids else "(no route)"

        status = "correct" if qm.correct else "WRONG"
        print(f"  [{qm.difficulty:6s}] {status:7s} | expected={qm.expected_skill:24s} "
              f"got={qm.routed_skill:24s} | {qm.total_ms:.0f}ms",
              file=sys.stderr)
        query_metrics.append(qm)

    # ── Generate reports ────────────────────────────────────────────────
    report_md = generate_report(sysinfo, model_load_s, rss_after_model, init_s,
                                append_metrics, query_metrics, ac, store)
    report_json = generate_json_report(sysinfo, model_load_s, rss_after_model, init_s,
                                       append_metrics, query_metrics, ac, store)
    return report_md, report_json


def generate_report(
    sysinfo: dict,
    model_load_s: float,
    rss_after_model: float,
    init_s: float,
    append_metrics: list[AppendMetrics],
    query_metrics: list[QueryMetrics],
    config,
    store: "KnowledgeStore",
) -> str:
    """Generate a comprehensive Markdown report."""
    lines = []

    lines.append("# Dynamic Skill Append Benchmark Report")
    lines.append("")
    lines.append(f"**Generated:** {sysinfo['timestamp']}")
    lines.append(f"**Platform:** {sysinfo['platform']}")
    lines.append(f"**Processor:** {sysinfo['processor']}")
    lines.append(f"**Python:** {sysinfo['python']}")
    lines.append(f"**Model:** `{sysinfo['model']}`")
    lines.append(f"**Crystal Layer:** L{config.crystal_layer} | **Window Size:** {config.window_size}")
    lines.append("")

    # ── Model loading ─────────────────────────────────────────────────
    lines.append("## 1. Model Loading")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Load time | {model_load_s:.1f}s |")
    lines.append(f"| RSS after load | {rss_after_model:.0f} MB |")
    lines.append(f"| Base state init | {init_s:.2f}s |")
    lines.append("")

    # ── Append metrics ────────────────────────────────────────────────
    lines.append("## 2. Skill Append Performance")
    lines.append("")
    lines.append("| # | Skill | Tokens | Windows | Entries | Time (s) | RSS Delta (MB) | Metal Peak (MB) |")
    lines.append("|---|-------|--------|---------|---------|----------|----------------|-----------------|")

    total_append_s = 0.0
    total_tokens = 0
    total_windows = 0
    total_entries = 0

    for i, m in enumerate(append_metrics, 1):
        rss_delta = m.rss_after_mb - m.rss_before_mb
        lines.append(
            f"| {i} | {m.skill_name} | {m.num_tokens} | {m.num_windows} | "
            f"{m.num_entries} | {m.elapsed_s:.2f} | {rss_delta:+.1f} | {m.metal_peak_mb:.0f} |"
        )
        total_append_s += m.elapsed_s
        total_tokens += m.num_tokens
        total_windows += m.num_windows
        total_entries += m.num_entries

    lines.append("")
    lines.append("### Append Summary")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total skills | {len(append_metrics)} |")
    lines.append(f"| Total tokens | {total_tokens:,} |")
    lines.append(f"| Total windows | {total_windows} |")
    lines.append(f"| Total entries | {total_entries:,} |")
    lines.append(f"| Total append time | {total_append_s:.1f}s |")
    avg = total_append_s / len(append_metrics) if append_metrics else 0
    lines.append(f"| Avg time per skill | {avg:.2f}s |")
    lines.append(f"| Avg tokens/second | {total_tokens / total_append_s:.0f} |" if total_append_s > 0 else "")
    lines.append("")

    # ── Query routing ─────────────────────────────────────────────────
    lines.append("## 3. Query Routing Accuracy")
    lines.append("")

    correct = sum(1 for q in query_metrics if q.correct)
    total = len(query_metrics)
    accuracy = correct / total * 100 if total else 0

    lines.append(f"**Overall accuracy: {correct}/{total} ({accuracy:.0f}%)**")
    lines.append("")

    # By difficulty
    for diff in ["easy", "medium", "hard"]:
        subset = [q for q in query_metrics if q.difficulty == diff]
        if subset:
            c = sum(1 for q in subset if q.correct)
            t = len(subset)
            lines.append(f"- **{diff.capitalize()}:** {c}/{t} ({c/t*100:.0f}%)")
    lines.append("")

    lines.append("### Query Details")
    lines.append("")
    lines.append("| # | Difficulty | Query | Expected | Got | Correct | Total (ms) |")
    lines.append("|---|-----------|-------|----------|-----|---------|------------|")

    for i, q in enumerate(query_metrics, 1):
        icon = "yes" if q.correct else "**NO**"
        query_short = q.query[:50] + "..." if len(q.query) > 50 else q.query
        lines.append(
            f"| {i} | {q.difficulty} | {query_short} | {q.expected_skill} | "
            f"{q.routed_skill} | {icon} | {q.total_ms:.0f} |"
        )
    lines.append("")

    # ── Query timing breakdown ────────────────────────────────────────
    lines.append("### Query Timing Breakdown")
    lines.append("")
    lines.append("| # | Expansion (ms) | Route (ms) | Prefill (ms) | Generate (ms) | Total (ms) |")
    lines.append("|---|---------------|------------|-------------|--------------|------------|")

    for i, q in enumerate(query_metrics, 1):
        lines.append(
            f"| {i} | {q.expansion_ms:.0f} | {q.route_ms:.0f} | "
            f"{q.prefill_ms:.0f} | {q.generate_ms:.0f} | {q.total_ms:.0f} |"
        )
    lines.append("")

    avg_total = sum(q.total_ms for q in query_metrics) / len(query_metrics) if query_metrics else 0
    avg_route = sum(q.route_ms for q in query_metrics) / len(query_metrics) if query_metrics else 0
    lines.append(f"**Average query time:** {avg_total:.0f}ms (routing: {avg_route:.0f}ms)")
    lines.append("")

    # ── Misrouted queries detail ──────────────────────────────────────
    wrong = [q for q in query_metrics if not q.correct]
    if wrong:
        lines.append("### Misrouted Queries")
        lines.append("")
        for q in wrong:
            lines.append(f"**Query:** {q.query}")
            lines.append(f"- Expected: `{q.expected_skill}`, Got: `{q.routed_skill}`")
            lines.append(f"- Routed to windows: {q.routed_windows}")
            lines.append(f"- Output: _{q.output_snippet[:150]}..._")
            lines.append("")

    # ── Store stats ───────────────────────────────────────────────────
    lines.append("## 4. Store Statistics")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Store version | v{12} |")
    lines.append(f"| Total windows | {store.num_windows} |")
    lines.append(f"| Total entries | {len(store.entries):,} |")
    lines.append(f"| IDF table size | {len(store.idf):,} tokens |")
    lines.append(f"| Keywords | {sum(len(v) for v in store.keywords.values())} total |")
    lines.append("")

    # ── Query output samples ──────────────────────────────────────────
    lines.append("## 5. Sample Query Outputs")
    lines.append("")
    for i, q in enumerate(query_metrics, 1):
        lines.append(f"### Query {i}: {q.query}")
        lines.append(f"- **Routed to:** `{q.routed_skill}` (windows {q.routed_windows})")
        lines.append(f"- **Output:**")
        lines.append(f"> {q.output_snippet}")
        lines.append("")

    return "\n".join(lines)


def generate_json_report(
    sysinfo: dict,
    model_load_s: float,
    rss_after_model: float,
    init_s: float,
    append_metrics: list[AppendMetrics],
    query_metrics: list[QueryMetrics],
    config,
    store: "KnowledgeStore",
) -> dict:
    """Generate a structured JSON report."""
    correct = sum(1 for q in query_metrics if q.correct)
    total = len(query_metrics)
    total_append_s = sum(m.elapsed_s for m in append_metrics)
    total_tokens = sum(m.num_tokens for m in append_metrics)

    return {
        "meta": {
            **sysinfo,
            "routing_method": os.environ.get("BENCH_ROUTING_METHOD", "tfidf_expansion"),
            "run_id": sysinfo["timestamp"].replace(":", "-").replace(".", "-"),
        },
        "model": {
            "load_time_s": round(model_load_s, 2),
            "rss_mb": round(rss_after_model, 0),
            "base_state_init_s": round(init_s, 3),
            "crystal_layer": config.crystal_layer,
            "window_size": config.window_size,
        },
        "append": {
            "total_skills": len(append_metrics),
            "total_tokens": total_tokens,
            "total_windows": sum(m.num_windows for m in append_metrics),
            "total_entries": sum(m.num_entries for m in append_metrics),
            "total_time_s": round(total_append_s, 2),
            "avg_time_per_skill_s": round(total_append_s / max(len(append_metrics), 1), 2),
            "tokens_per_second": round(total_tokens / max(total_append_s, 0.01), 0),
            "skills": [
                {
                    "name": m.skill_name,
                    "tokens": m.num_tokens,
                    "windows": m.num_windows,
                    "entries": m.num_entries,
                    "time_s": round(m.elapsed_s, 3),
                    "rss_delta_mb": round(m.rss_after_mb - m.rss_before_mb, 1),
                    "metal_peak_mb": round(m.metal_peak_mb, 0),
                }
                for m in append_metrics
            ],
        },
        "routing": {
            "accuracy": round(correct / max(total, 1) * 100, 1),
            "correct": correct,
            "total": total,
            "by_difficulty": {
                diff: {
                    "correct": sum(1 for q in query_metrics if q.difficulty == diff and q.correct),
                    "total": sum(1 for q in query_metrics if q.difficulty == diff),
                }
                for diff in ["easy", "medium", "hard"]
            },
            "avg_query_ms": round(sum(q.total_ms for q in query_metrics) / max(total, 1), 0),
            "avg_expansion_ms": round(sum(q.expansion_ms for q in query_metrics) / max(total, 1), 0),
            "avg_route_ms": round(sum(q.route_ms for q in query_metrics) / max(total, 1), 0),
            "avg_prefill_ms": round(sum(q.prefill_ms for q in query_metrics) / max(total, 1), 0),
            "avg_generate_ms": round(sum(q.generate_ms for q in query_metrics) / max(total, 1), 0),
            "queries": [
                {
                    "query": q.query,
                    "expected": q.expected_skill,
                    "got": q.routed_skill,
                    "correct": q.correct,
                    "difficulty": q.difficulty,
                    "windows": q.routed_windows,
                    "expansion_ms": round(q.expansion_ms, 1),
                    "route_ms": round(q.route_ms, 1),
                    "prefill_ms": round(q.prefill_ms, 1),
                    "generate_ms": round(q.generate_ms, 1),
                    "total_ms": round(q.total_ms, 1),
                    "output_snippet": q.output_snippet[:300],
                }
                for q in query_metrics
            ],
        },
        "store": {
            "version": 12,
            "total_windows": store.num_windows,
            "total_entries": len(store.entries),
            "idf_table_size": len(store.idf),
            "total_keywords": sum(len(v) for v in store.keywords.values()),
        },
    }


# ── Entry point ──────────────────────────────────────────────────────

if __name__ == "__main__":
    model_path = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Desktop/gemma-3-4b-it")
    run_label = os.environ.get("BENCH_ROUTING_METHOD", "tfidf_expansion")

    print(f"Starting benchmark with model: {model_path}", file=sys.stderr)
    report_md, report_json = run_benchmark(model_path)

    # Write reports
    runs_dir = Path(__file__).parent / "runs"
    runs_dir.mkdir(exist_ok=True)

    run_id = report_json["meta"]["run_id"]
    md_path = runs_dir / f"{run_label}.md"
    json_path = runs_dir / f"{run_label}.json"

    md_path.write_text(report_md)
    json_path.write_text(json.dumps(report_json, indent=2) + "\n")

    # Also write latest to root
    (Path(__file__).parent / "BENCHMARK_REPORT.md").write_text(report_md)

    print(f"\n\nReports written to:", file=sys.stderr)
    print(f"  {md_path}", file=sys.stderr)
    print(f"  {json_path}", file=sys.stderr)

    print(report_md)
