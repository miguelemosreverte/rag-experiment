#!/usr/bin/env node
/**
 * md2html.js — Convert benchmark JSON + Markdown runs to a WSJ-style HTML timeline.
 *
 * Reads all .json files from benchmark/runs/, generates:
 *   - Individual HTML pages per run
 *   - An index.html with timeline navigation (arrow keys)
 *
 * Style: Tailwind CSS, Wall Street Journal inspired (serif headlines,
 * clean data tables, muted palette, emphasis on numbers).
 *
 * Usage: node docs/md2html.js
 */

const fs = require("fs");
const path = require("path");

const RUNS_DIR = path.join(__dirname, "..", "benchmark", "runs");
const DOCS_DIR = path.join(__dirname);

// ── Collect runs ────────────────────────────────────────────────────

const runFiles = fs
  .readdirSync(RUNS_DIR)
  .filter((f) => f.endsWith(".json"))
  .sort();

const runs = runFiles.map((f) => {
  const json = JSON.parse(fs.readFileSync(path.join(RUNS_DIR, f), "utf-8"));
  const md = fs.readFileSync(
    path.join(RUNS_DIR, f.replace(".json", ".md")),
    "utf-8"
  );
  return { filename: f, label: f.replace(".json", ""), json, md };
});

if (runs.length === 0) {
  console.error("No runs found in benchmark/runs/");
  process.exit(1);
}

// ── HTML helpers ────────────────────────────────────────────────────

const HEAD = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            serif: ['Georgia', 'Cambria', '"Times New Roman"', 'Times', 'serif'],
            mono: ['"JetBrains Mono"', '"Fira Code"', 'Consolas', 'monospace'],
          },
          colors: {
            wsj: {
              bg: '#F8F5F0',
              text: '#333333',
              muted: '#666666',
              accent: '#0274B6',
              green: '#27752B',
              red: '#BF2600',
              border: '#D4CBC2',
              highlight: '#FFF8E7',
            }
          }
        }
      }
    }
  </script>
  <style>
    body { background: #F8F5F0; }
    .metric-card { transition: transform 0.15s; }
    .metric-card:hover { transform: translateY(-2px); }
    table { border-collapse: collapse; }
    th { text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.7rem; }
    td, th { border-bottom: 1px solid #D4CBC2; }
    .correct { color: #27752B; }
    .wrong { color: #BF2600; font-weight: 700; }
    .bar { transition: width 0.6s ease-out; }
  </style>
</head>`;

function kpi(label, value, unit = "", trend = "") {
  const trendHtml = trend
    ? `<span class="${trend === "up" ? "text-wsj-green" : "text-wsj-red"} text-xs ml-1">${trend === "up" ? "&#9650;" : "&#9660;"}</span>`
    : "";
  return `
    <div class="metric-card bg-white border border-wsj-border rounded-lg p-5 shadow-sm">
      <div class="text-xs uppercase tracking-wider text-wsj-muted font-sans mb-1">${label}</div>
      <div class="text-3xl font-serif font-bold text-wsj-text">${value}<span class="text-lg text-wsj-muted ml-1">${unit}</span>${trendHtml}</div>
    </div>`;
}

function queryRow(q, i) {
  const cls = q.correct ? "correct" : "wrong";
  const icon = q.correct ? "&#10003;" : "&#10007;";
  const shortQ = q.query.length > 45 ? q.query.slice(0, 45) + "..." : q.query;
  return `
    <tr class="hover:bg-wsj-highlight">
      <td class="py-2 px-3 font-mono text-xs">${i}</td>
      <td class="py-2 px-3 text-xs uppercase tracking-wider">${q.difficulty}</td>
      <td class="py-2 px-3 text-sm">${shortQ}</td>
      <td class="py-2 px-3 font-mono text-xs">${q.expected}</td>
      <td class="py-2 px-3 font-mono text-xs ${cls}">${q.got}</td>
      <td class="py-2 px-3 text-center ${cls} text-lg">${icon}</td>
      <td class="py-2 px-3 font-mono text-xs text-right">${q.total_ms.toFixed(0)}</td>
    </tr>`;
}

function appendRow(s, i) {
  return `
    <tr class="hover:bg-wsj-highlight">
      <td class="py-2 px-3 font-mono text-xs">${i}</td>
      <td class="py-2 px-3 text-sm">${s.name}</td>
      <td class="py-2 px-3 font-mono text-xs text-right">${s.tokens}</td>
      <td class="py-2 px-3 font-mono text-xs text-right">${s.windows}</td>
      <td class="py-2 px-3 font-mono text-xs text-right">${s.entries}</td>
      <td class="py-2 px-3 font-mono text-xs text-right">${s.time_s.toFixed(2)}</td>
    </tr>`;
}

function timingBar(label, ms, maxMs) {
  const pct = Math.min((ms / maxMs) * 100, 100);
  return `
    <div class="flex items-center gap-3 mb-2">
      <div class="w-24 text-xs text-wsj-muted text-right">${label}</div>
      <div class="flex-1 bg-gray-100 rounded-full h-5 overflow-hidden">
        <div class="bar bg-wsj-accent h-full rounded-full" style="width:${pct}%"></div>
      </div>
      <div class="w-16 text-xs font-mono text-right">${ms.toFixed(0)}ms</div>
    </div>`;
}

// ── Generate per-run pages ──────────────────────────────────────────

runs.forEach((run, idx) => {
  const d = run.json;
  const r = d.routing;
  const a = d.append;
  const prevLabel = idx > 0 ? runs[idx - 1].label : null;
  const nextLabel = idx < runs.length - 1 ? runs[idx + 1].label : null;

  const maxQueryMs = Math.max(...r.queries.map((q) => q.total_ms));

  const nav = `
    <div class="flex justify-between items-center mb-8 border-b-2 border-wsj-text pb-4">
      <div>
        ${prevLabel ? `<a href="${prevLabel}.html" class="text-wsj-accent hover:underline text-sm">&larr; ${prevLabel}</a>` : '<span class="text-wsj-muted text-sm">&larr; (first run)</span>'}
      </div>
      <div class="text-center">
        <div class="text-xs uppercase tracking-widest text-wsj-muted font-sans">Run ${idx + 1} of ${runs.length}</div>
        <h1 class="text-2xl font-serif font-bold text-wsj-text mt-1">${run.label.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase())}</h1>
      </div>
      <div>
        ${nextLabel ? `<a href="${nextLabel}.html" class="text-wsj-accent hover:underline text-sm">${nextLabel} &rarr;</a>` : '<span class="text-wsj-muted text-sm">(latest) &rarr;</span>'}
      </div>
    </div>`;

  const html = `${HEAD}
<title>${run.label} | Benchmark</title>
</head>
<body class="font-serif text-wsj-text">
  <div class="max-w-5xl mx-auto px-6 py-8">
    ${nav}

    <div class="text-xs text-wsj-muted mb-6">
      ${d.meta.platform} &middot; ${d.meta.model.split("/").pop()} &middot; ${d.meta.timestamp}
    </div>

    <!-- KPI cards -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
      ${kpi("Accuracy", r.accuracy + "%", "")}
      ${kpi("Avg Query", r.avg_query_ms, "ms")}
      ${kpi("Avg Append", a.avg_time_per_skill_s, "s")}
      ${kpi("Memory", d.model.rss_mb, "MB")}
    </div>

    <!-- Accuracy by difficulty -->
    <h2 class="text-lg font-serif font-bold border-b border-wsj-border pb-2 mb-4">Routing Accuracy</h2>
    <div class="grid grid-cols-3 gap-4 mb-8">
      ${["easy", "medium", "hard"]
        .map((diff) => {
          const dd = r.by_difficulty[diff];
          const pct = dd.total > 0 ? ((dd.correct / dd.total) * 100).toFixed(0) : 0;
          const color = pct == 100 ? "text-wsj-green" : pct >= 50 ? "text-wsj-text" : "text-wsj-red";
          return `<div class="bg-white border border-wsj-border rounded-lg p-4 text-center shadow-sm">
            <div class="text-xs uppercase tracking-wider text-wsj-muted mb-1">${diff}</div>
            <div class="text-2xl font-bold ${color}">${dd.correct}/${dd.total}</div>
          </div>`;
        })
        .join("")}
    </div>

    <!-- Query details -->
    <h2 class="text-lg font-serif font-bold border-b border-wsj-border pb-2 mb-4">Query Details</h2>
    <div class="overflow-x-auto mb-8">
      <table class="w-full text-left">
        <thead>
          <tr class="border-b-2 border-wsj-text">
            <th class="py-2 px-3">#</th>
            <th class="py-2 px-3">Diff</th>
            <th class="py-2 px-3">Query</th>
            <th class="py-2 px-3">Expected</th>
            <th class="py-2 px-3">Got</th>
            <th class="py-2 px-3 text-center">OK</th>
            <th class="py-2 px-3 text-right">Time</th>
          </tr>
        </thead>
        <tbody>
          ${r.queries.map((q, i) => queryRow(q, i + 1)).join("")}
        </tbody>
      </table>
    </div>

    <!-- Timing breakdown -->
    <h2 class="text-lg font-serif font-bold border-b border-wsj-border pb-2 mb-4">Average Query Timing</h2>
    <div class="bg-white border border-wsj-border rounded-lg p-6 mb-8 shadow-sm">
      ${timingBar("Expansion", r.avg_expansion_ms, r.avg_query_ms)}
      ${timingBar("Route", r.avg_route_ms, r.avg_query_ms)}
      ${timingBar("Prefill", r.avg_prefill_ms, r.avg_query_ms)}
      ${timingBar("Generate", r.avg_generate_ms, r.avg_query_ms)}
    </div>

    <!-- Append performance -->
    <h2 class="text-lg font-serif font-bold border-b border-wsj-border pb-2 mb-4">Skill Append Performance</h2>
    <div class="overflow-x-auto mb-8">
      <table class="w-full text-left">
        <thead>
          <tr class="border-b-2 border-wsj-text">
            <th class="py-2 px-3">#</th>
            <th class="py-2 px-3">Skill</th>
            <th class="py-2 px-3 text-right">Tokens</th>
            <th class="py-2 px-3 text-right">Win</th>
            <th class="py-2 px-3 text-right">Entries</th>
            <th class="py-2 px-3 text-right">Time (s)</th>
          </tr>
        </thead>
        <tbody>
          ${a.skills.map((s, i) => appendRow(s, i + 1)).join("")}
        </tbody>
      </table>
    </div>

    <!-- Footer -->
    <div class="text-center text-xs text-wsj-muted border-t border-wsj-border pt-4 mt-8">
      Generated by <span class="font-mono">md2html.js</span> &middot;
      <a href="index.html" class="text-wsj-accent hover:underline">All Runs</a>
    </div>
  </div>

  <script>
    document.addEventListener('keydown', (e) => {
      ${prevLabel ? `if (e.key === 'ArrowLeft') window.location.href = '${prevLabel}.html';` : ""}
      ${nextLabel ? `if (e.key === 'ArrowRight') window.location.href = '${nextLabel}.html';` : ""}
    });
  </script>
</body>
</html>`;

  fs.writeFileSync(path.join(DOCS_DIR, `${run.label}.html`), html);
  console.log(`  Generated: docs/${run.label}.html`);
});

// ── Generate index.html (timeline overview) ─────────────────────────

function compareKpi(runs, accessor, label, unit, better = "higher") {
  const values = runs.map(accessor);
  const best =
    better === "higher" ? Math.max(...values) : Math.min(...values);
  return runs
    .map((r, i) => {
      const v = values[i];
      const isBest = v === best && runs.length > 1;
      return `
      <td class="py-3 px-4 font-mono text-right ${isBest ? "font-bold text-wsj-green" : ""}">
        ${typeof v === "number" ? (Number.isInteger(v) ? v : v.toFixed(1)) : v}${unit}
      </td>`;
    })
    .join("");
}

const indexHtml = `${HEAD}
<title>Benchmark Timeline | RAG Experiment</title>
</head>
<body class="font-serif text-wsj-text">
  <div class="max-w-6xl mx-auto px-6 py-8">
    <div class="border-b-2 border-wsj-text pb-4 mb-8">
      <div class="text-xs uppercase tracking-widest text-wsj-muted font-sans">RAG Experiment</div>
      <h1 class="text-3xl font-bold mt-1">Benchmark Timeline</h1>
      <p class="text-sm text-wsj-muted mt-2">Navigate with <kbd class="bg-gray-200 px-1.5 py-0.5 rounded text-xs font-mono">&larr;</kbd> <kbd class="bg-gray-200 px-1.5 py-0.5 rounded text-xs font-mono">&rarr;</kbd> arrow keys on individual run pages</p>
    </div>

    <!-- Comparison table -->
    <div class="overflow-x-auto">
      <table class="w-full text-left">
        <thead>
          <tr class="border-b-2 border-wsj-text">
            <th class="py-2 px-4 w-40">Metric</th>
            ${runs.map((r) => `<th class="py-2 px-4 text-right"><a href="${r.label}.html" class="text-wsj-accent hover:underline">${r.label.replace(/_/g, " ")}</a></th>`).join("")}
          </tr>
        </thead>
        <tbody>
          <tr class="hover:bg-wsj-highlight">
            <td class="py-3 px-4 text-sm font-sans uppercase tracking-wider text-wsj-muted">Accuracy</td>
            ${compareKpi(runs, (r) => r.json.routing.accuracy, "Accuracy", "%", "higher")}
          </tr>
          <tr class="hover:bg-wsj-highlight">
            <td class="py-3 px-4 text-sm font-sans uppercase tracking-wider text-wsj-muted">Avg Query</td>
            ${compareKpi(runs, (r) => r.json.routing.avg_query_ms, "Query", "ms", "lower")}
          </tr>
          <tr class="hover:bg-wsj-highlight">
            <td class="py-3 px-4 text-sm font-sans uppercase tracking-wider text-wsj-muted">Avg Expansion</td>
            ${compareKpi(runs, (r) => r.json.routing.avg_expansion_ms, "Expansion", "ms", "lower")}
          </tr>
          <tr class="hover:bg-wsj-highlight">
            <td class="py-3 px-4 text-sm font-sans uppercase tracking-wider text-wsj-muted">Avg Route</td>
            ${compareKpi(runs, (r) => r.json.routing.avg_route_ms, "Route", "ms", "lower")}
          </tr>
          <tr class="hover:bg-wsj-highlight">
            <td class="py-3 px-4 text-sm font-sans uppercase tracking-wider text-wsj-muted">Avg Append</td>
            ${compareKpi(runs, (r) => r.json.append.avg_time_per_skill_s, "Append", "s", "lower")}
          </tr>
          <tr class="hover:bg-wsj-highlight">
            <td class="py-3 px-4 text-sm font-sans uppercase tracking-wider text-wsj-muted">Memory</td>
            ${compareKpi(runs, (r) => r.json.model.rss_mb, "Memory", "MB", "lower")}
          </tr>
          <tr class="hover:bg-wsj-highlight">
            <td class="py-3 px-4 text-sm font-sans uppercase tracking-wider text-wsj-muted">Easy</td>
            ${runs.map((r) => {
              const d = r.json.routing.by_difficulty.easy;
              return `<td class="py-3 px-4 font-mono text-right">${d.correct}/${d.total}</td>`;
            }).join("")}
          </tr>
          <tr class="hover:bg-wsj-highlight">
            <td class="py-3 px-4 text-sm font-sans uppercase tracking-wider text-wsj-muted">Medium</td>
            ${runs.map((r) => {
              const d = r.json.routing.by_difficulty.medium;
              return `<td class="py-3 px-4 font-mono text-right">${d.correct}/${d.total}</td>`;
            }).join("")}
          </tr>
          <tr class="hover:bg-wsj-highlight">
            <td class="py-3 px-4 text-sm font-sans uppercase tracking-wider text-wsj-muted">Hard</td>
            ${runs.map((r) => {
              const d = r.json.routing.by_difficulty.hard;
              return `<td class="py-3 px-4 font-mono text-right">${d.correct}/${d.total}</td>`;
            }).join("")}
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Run cards -->
    <h2 class="text-lg font-serif font-bold border-b border-wsj-border pb-2 mb-4 mt-10">Runs</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      ${runs
        .map(
          (r, i) => `
        <a href="${r.label}.html" class="block bg-white border border-wsj-border rounded-lg p-5 shadow-sm hover:shadow-md transition-shadow">
          <div class="text-xs text-wsj-muted mb-1">Run ${i + 1}</div>
          <div class="font-bold text-lg mb-2">${r.label.replace(/_/g, " ")}</div>
          <div class="flex justify-between text-sm">
            <span>Accuracy: <strong class="${r.json.routing.accuracy === 100 ? "text-wsj-green" : ""}">${r.json.routing.accuracy}%</strong></span>
            <span class="text-wsj-muted">${r.json.routing.avg_query_ms.toFixed(0)}ms/query</span>
          </div>
        </a>`
        )
        .join("")}
    </div>

    <div class="text-center text-xs text-wsj-muted border-t border-wsj-border pt-4 mt-8">
      RAG Experiment &middot; Gaucho AI
    </div>
  </div>
</body>
</html>`;

fs.writeFileSync(path.join(DOCS_DIR, "index.html"), indexHtml);
console.log(`  Generated: docs/index.html`);
console.log(`\nDone! ${runs.length} run(s) processed.`);
