#!/usr/bin/env node
/**
 * md2html.js — Convert benchmark JSON runs to WSJ-style HTML pages.
 *
 * Supports two JSON formats:
 *   - Skill routing benchmarks (have routing.queries)
 *   - Apollo/document benchmarks (have queries[] with grounded/terms)
 *
 * Style: Tailwind CSS, Wall Street Journal inspired.
 * Usage: node docs/md2html.js
 */

const fs = require("fs");
const path = require("path");

const RUNS_DIR = path.join(__dirname, "..", "benchmark", "runs");
const DOCS_DIR = path.join(__dirname);

// ── Collect runs ────────────────────────────────────────────────────

const runFiles = fs.readdirSync(RUNS_DIR).filter((f) => f.endsWith(".json")).sort();

const runs = runFiles.map((f) => {
  const json = JSON.parse(fs.readFileSync(path.join(RUNS_DIR, f), "utf-8"));
  const label = f.replace(".json", "");
  const type = json.routing ? "skill" : json.document ? "apollo" : "unknown";
  return { filename: f, label, json, type };
});

if (runs.length === 0) { console.error("No runs found."); process.exit(1); }

// ── Shared HTML ─────────────────────────────────────────────────────

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
            wsj: { bg:'#F8F5F0', text:'#333', muted:'#666', accent:'#0274B6',
                   green:'#27752B', red:'#BF2600', border:'#D4CBC2', highlight:'#FFF8E7' }
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
    .bar { transition: width 0.6s ease-out; }
    blockquote { border-left: 3px solid #D4CBC2; padding-left: 1rem; color: #555; font-style: italic; }
  </style>
</head>`;

function kpi(label, value, unit = "") {
  return `<div class="metric-card bg-white border border-wsj-border rounded-lg p-5 shadow-sm">
    <div class="text-xs uppercase tracking-wider text-wsj-muted font-sans mb-1">${label}</div>
    <div class="text-3xl font-serif font-bold text-wsj-text">${value}<span class="text-lg text-wsj-muted ml-1">${unit}</span></div>
  </div>`;
}

function timingBar(label, ms, maxMs) {
  const pct = Math.min((ms / maxMs) * 100, 100);
  return `<div class="flex items-center gap-3 mb-2">
    <div class="w-24 text-xs text-wsj-muted text-right">${label}</div>
    <div class="flex-1 bg-gray-100 rounded-full h-5 overflow-hidden">
      <div class="bar bg-wsj-accent h-full rounded-full" style="width:${pct}%"></div>
    </div>
    <div class="w-16 text-xs font-mono text-right">${ms.toFixed(0)}ms</div>
  </div>`;
}

function navBar(runs, idx) {
  const prev = idx > 0 ? runs[idx - 1].label : null;
  const next = idx < runs.length - 1 ? runs[idx + 1].label : null;
  return `<div class="flex justify-between items-center mb-8 border-b-2 border-wsj-text pb-4">
    <div>${prev ? `<a href="${prev}.html" class="text-wsj-accent hover:underline text-sm">&larr; ${prev.replace(/_/g," ")}</a>` : '<span class="text-wsj-muted text-sm">&larr;</span>'}</div>
    <div class="text-center">
      <div class="text-xs uppercase tracking-widest text-wsj-muted font-sans">Run ${idx+1} of ${runs.length}</div>
      <h1 class="text-2xl font-serif font-bold text-wsj-text mt-1">${runs[idx].label.replace(/_/g," ").replace(/\b\w/g,c=>c.toUpperCase())}</h1>
    </div>
    <div>${next ? `<a href="${next}.html" class="text-wsj-accent hover:underline text-sm">${next.replace(/_/g," ")} &rarr;</a>` : '<span class="text-wsj-muted text-sm">&rarr;</span>'}</div>
  </div>
  <script>document.addEventListener('keydown',e=>{
    ${prev?`if(e.key==='ArrowLeft')window.location.href='${prev}.html';`:''}
    ${next?`if(e.key==='ArrowRight')window.location.href='${next}.html';`:''}
  });</script>`;
}

// ── Skill benchmark page ────────────────────────────────────────────

function renderSkillPage(run, idx) {
  const d = run.json, r = d.routing, a = d.append;
  return `${HEAD}<title>${run.label} | Benchmark</title></head>
<body class="font-serif text-wsj-text">
<div class="max-w-5xl mx-auto px-6 py-8">
  ${navBar(runs, idx)}
  <div class="text-xs text-wsj-muted mb-6">${d.meta.platform} &middot; ${d.meta.model.split("/").pop()} &middot; ${d.meta.timestamp}</div>

  <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
    ${kpi("Accuracy", r.accuracy+"%")} ${kpi("Avg Query", r.avg_query_ms, "ms")}
    ${kpi("Avg Append", a.avg_time_per_skill_s, "s")} ${kpi("Memory", d.model.rss_mb, "MB")}
  </div>

  <h2 class="text-lg font-serif font-bold border-b border-wsj-border pb-2 mb-4">Routing Accuracy</h2>
  <div class="grid grid-cols-3 gap-4 mb-8">
    ${["easy","medium","hard"].map(diff=>{
      const dd=r.by_difficulty[diff]; const pct=dd.total>0?((dd.correct/dd.total)*100).toFixed(0):0;
      const color=pct==100?"text-wsj-green":pct>=50?"text-wsj-text":"text-wsj-red";
      return `<div class="bg-white border border-wsj-border rounded-lg p-4 text-center shadow-sm">
        <div class="text-xs uppercase tracking-wider text-wsj-muted mb-1">${diff}</div>
        <div class="text-2xl font-bold ${color}">${dd.correct}/${dd.total}</div></div>`;
    }).join("")}
  </div>

  <h2 class="text-lg font-serif font-bold border-b border-wsj-border pb-2 mb-4">Query Details</h2>
  <div class="overflow-x-auto mb-8"><table class="w-full text-left"><thead>
    <tr class="border-b-2 border-wsj-text"><th class="py-2 px-3">#</th><th class="py-2 px-3">Diff</th><th class="py-2 px-3">Query</th><th class="py-2 px-3">Expected</th><th class="py-2 px-3">Got</th><th class="py-2 px-3 text-center">OK</th><th class="py-2 px-3 text-right">Time</th></tr>
  </thead><tbody>
    ${r.queries.map((q,i)=>{
      const cls=q.correct?"correct":"wrong"; const icon=q.correct?"&#10003;":"&#10007;";
      const sq=q.query.length>45?q.query.slice(0,45)+"...":q.query;
      return `<tr class="hover:bg-wsj-highlight"><td class="py-2 px-3 font-mono text-xs">${i+1}</td><td class="py-2 px-3 text-xs uppercase">${q.difficulty}</td><td class="py-2 px-3 text-sm">${sq}</td><td class="py-2 px-3 font-mono text-xs">${q.expected}</td><td class="py-2 px-3 font-mono text-xs ${cls}">${q.got}</td><td class="py-2 px-3 text-center ${cls} text-lg">${icon}</td><td class="py-2 px-3 font-mono text-xs text-right">${q.total_ms.toFixed(0)}</td></tr>`;
    }).join("")}
  </tbody></table></div>

  <h2 class="text-lg font-serif font-bold border-b border-wsj-border pb-2 mb-4">Average Query Timing</h2>
  <div class="bg-white border border-wsj-border rounded-lg p-6 mb-8 shadow-sm">
    ${timingBar("Expansion", r.avg_expansion_ms, r.avg_query_ms)}
    ${timingBar("Route", r.avg_route_ms, r.avg_query_ms)}
    ${timingBar("Prefill", r.avg_prefill_ms, r.avg_query_ms)}
    ${timingBar("Generate", r.avg_generate_ms, r.avg_query_ms)}
  </div>

  <h2 class="text-lg font-serif font-bold border-b border-wsj-border pb-2 mb-4">Skill Append Performance</h2>
  <div class="overflow-x-auto mb-8"><table class="w-full text-left"><thead>
    <tr class="border-b-2 border-wsj-text"><th class="py-2 px-3">#</th><th class="py-2 px-3">Skill</th><th class="py-2 px-3 text-right">Tokens</th><th class="py-2 px-3 text-right">Win</th><th class="py-2 px-3 text-right">Entries</th><th class="py-2 px-3 text-right">Time</th></tr>
  </thead><tbody>
    ${a.skills.map((s,i)=>`<tr class="hover:bg-wsj-highlight"><td class="py-2 px-3 font-mono text-xs">${i+1}</td><td class="py-2 px-3 text-sm">${s.name}</td><td class="py-2 px-3 font-mono text-xs text-right">${s.tokens}</td><td class="py-2 px-3 font-mono text-xs text-right">${s.windows}</td><td class="py-2 px-3 font-mono text-xs text-right">${s.entries}</td><td class="py-2 px-3 font-mono text-xs text-right">${s.time_s.toFixed(2)}s</td></tr>`).join("")}
  </tbody></table></div>

  <div class="text-center text-xs text-wsj-muted border-t border-wsj-border pt-4 mt-8">
    <a href="index.html" class="text-wsj-accent hover:underline">All Runs</a>
  </div>
</div></body></html>`;
}

// ── Apollo benchmark page ───────────────────────────────────────────

function renderApolloPage(run, idx) {
  const d = run.json, s = d.summary, doc = d.document;
  const maxMs = Math.max(...d.queries.map(q => q.total_ms));

  function groundedBadge(q) {
    if (q.grounded) return '<span class="inline-block px-2 py-0.5 rounded text-xs font-bold bg-green-100 text-wsj-green">GROUNDED</span>';
    return '<span class="inline-block px-2 py-0.5 rounded text-xs font-bold bg-red-50 text-wsj-red">WEAK</span>';
  }

  function termsPill(found, total) {
    const pct = total > 0 ? (found / total * 100) : 0;
    const color = pct >= 75 ? "bg-green-100 text-wsj-green" : pct >= 50 ? "bg-yellow-50 text-yellow-700" : "bg-red-50 text-wsj-red";
    return `<span class="inline-block px-2 py-0.5 rounded text-xs font-mono ${color}">${found}/${total}</span>`;
  }

  const categories = ["verbatim", "factual", "interpretive"];

  return `${HEAD}<title>${run.label} | Apollo 11 Benchmark</title></head>
<body class="font-serif text-wsj-text">
<div class="max-w-5xl mx-auto px-6 py-8">
  ${navBar(runs, idx)}

  <!-- Masthead -->
  <div class="text-center mb-8">
    <div class="text-xs uppercase tracking-widest text-wsj-muted font-sans">Apollo 11 Air-to-Ground Transcript</div>
    <h2 class="text-xl font-bold mt-1">370,778 Tokens Compressed to Markov Boundaries</h2>
    <div class="text-sm text-wsj-muted mt-2">${doc.windows} windows &middot; ${doc.entries.toLocaleString()} entries &middot; ${doc.idf_tokens.toLocaleString()} IDF tokens &middot; Gemma 3 4B</div>
  </div>

  <!-- KPI cards -->
  <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
    ${kpi("Grounded", s.grounded+"/"+s.total)}
    ${kpi("Terms Found", s.terms_pct+"%")}
    ${kpi("Avg Query", (s.avg_query_ms/1000).toFixed(1), "s")}
    ${kpi("Model Load", s.model_load_s, "s")}
  </div>

  <!-- By category -->
  <h2 class="text-lg font-serif font-bold border-b border-wsj-border pb-2 mb-4">Grounding by Category</h2>
  <div class="grid grid-cols-3 gap-4 mb-8">
    ${categories.map(cat => {
      const qs = d.queries.filter(q => q.category === cat);
      const g = qs.filter(q => q.grounded).length;
      const t = qs.length;
      if (t === 0) return '';
      const pct = (g/t*100).toFixed(0);
      const color = pct >= 75 ? "text-wsj-green" : pct >= 50 ? "text-wsj-text" : "text-wsj-red";
      return `<div class="bg-white border border-wsj-border rounded-lg p-4 text-center shadow-sm">
        <div class="text-xs uppercase tracking-wider text-wsj-muted mb-1">${cat}</div>
        <div class="text-2xl font-bold ${color}">${g}/${t}</div></div>`;
    }).join("")}
  </div>

  <!-- Query results table -->
  <h2 class="text-lg font-serif font-bold border-b border-wsj-border pb-2 mb-4">Query Results</h2>
  <div class="overflow-x-auto mb-8"><table class="w-full text-left"><thead>
    <tr class="border-b-2 border-wsj-text">
      <th class="py-2 px-3">#</th><th class="py-2 px-3">Category</th><th class="py-2 px-3">Query</th>
      <th class="py-2 px-3 text-center">Status</th><th class="py-2 px-3 text-center">Terms</th><th class="py-2 px-3 text-right">Time</th>
    </tr>
  </thead><tbody>
    ${d.queries.map((q,i) => {
      const sq = q.query.length > 55 ? q.query.slice(0,55)+"..." : q.query;
      return `<tr class="hover:bg-wsj-highlight">
        <td class="py-2 px-3 font-mono text-xs">${i+1}</td>
        <td class="py-2 px-3 text-xs uppercase tracking-wider">${q.category}</td>
        <td class="py-2 px-3 text-sm">${sq}</td>
        <td class="py-2 px-3 text-center">${groundedBadge(q)}</td>
        <td class="py-2 px-3 text-center">${termsPill(q.terms_found.length, q.terms_found.length + q.terms_missing.length)}</td>
        <td class="py-2 px-3 font-mono text-xs text-right">${(q.total_ms/1000).toFixed(1)}s</td>
      </tr>`;
    }).join("")}
  </tbody></table></div>

  <!-- Timing -->
  <h2 class="text-lg font-serif font-bold border-b border-wsj-border pb-2 mb-4">Average Query Timing</h2>
  <div class="bg-white border border-wsj-border rounded-lg p-6 mb-8 shadow-sm">
    ${timingBar("Expansion", d.queries.reduce((a,q)=>a+q.expansion_ms,0)/d.queries.length, s.avg_query_ms)}
    ${timingBar("Route", d.queries.reduce((a,q)=>a+q.route_ms,0)/d.queries.length, s.avg_query_ms)}
    ${timingBar("Prefill", d.queries.reduce((a,q)=>a+q.prefill_ms,0)/d.queries.length, s.avg_query_ms)}
    ${timingBar("Generate", d.queries.reduce((a,q)=>a+q.generate_ms,0)/d.queries.length, s.avg_query_ms)}
  </div>

  <!-- Full query outputs -->
  <h2 class="text-lg font-serif font-bold border-b border-wsj-border pb-2 mb-4">Full Query Outputs</h2>
  ${d.queries.map((q, i) => {
    const termsHtml = q.terms_found.length > 0
      ? `<span class="text-wsj-green text-xs">Found: ${q.terms_found.join(", ")}</span>`
      : '';
    const missingHtml = q.terms_missing.length > 0
      ? `<span class="text-wsj-red text-xs ml-2">Missing: ${q.terms_missing.join(", ")}</span>`
      : '';
    // Escape HTML in output
    const safeOutput = q.output.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\n/g,'<br>');
    const expectedRaw = q.expected_verbatim || "";
    const safeExpected = expectedRaw.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\n/g,'<br>');

    return `
    <div class="bg-white border border-wsj-border rounded-lg p-5 mb-4 shadow-sm">
      <div class="flex items-start justify-between mb-3">
        <div>
          <span class="font-mono text-xs text-wsj-muted mr-2">#${i+1}</span>
          <span class="text-xs uppercase tracking-wider text-wsj-muted mr-3">${q.category}</span>
          ${groundedBadge(q)}
        </div>
        <div class="font-mono text-xs text-wsj-muted">Windows: ${q.routed_windows.join(", ")} &middot; ${(q.total_ms/1000).toFixed(1)}s</div>
      </div>
      <h3 class="font-bold text-sm mb-2">${q.query}</h3>
      <div class="mb-3">${termsHtml}${missingHtml}</div>
      ${safeExpected ? `
      <div class="mb-4">
        <div class="text-xs uppercase tracking-wider text-wsj-muted font-sans mb-1">Expected (from transcript)</div>
        <div class="bg-wsj-highlight border border-yellow-200 rounded p-3 font-mono text-xs leading-relaxed text-wsj-text">${safeExpected}</div>
      </div>` : ''}
      <div>
        <div class="text-xs uppercase tracking-wider text-wsj-muted font-sans mb-1">Model Output</div>
        <blockquote class="text-sm leading-relaxed">${safeOutput}</blockquote>
      </div>
    </div>`;
  }).join("")}

  <div class="text-center text-xs text-wsj-muted border-t border-wsj-border pt-4 mt-8">
    <a href="index.html" class="text-wsj-accent hover:underline">All Runs</a> &middot; Gaucho AI
  </div>
</div></body></html>`;
}

// ── Generate pages ──────────────────────────────────────────────────

runs.forEach((run, idx) => {
  const html = run.type === "skill" ? renderSkillPage(run, idx) : renderApolloPage(run, idx);
  fs.writeFileSync(path.join(DOCS_DIR, `${run.label}.html`), html);
  console.log(`  Generated: docs/${run.label}.html (${run.type})`);
});

// ── Index page ──────────────────────────────────────────────────────

const indexHtml = `${HEAD}<title>Benchmark Timeline | RAG Experiment</title></head>
<body class="font-serif text-wsj-text">
<div class="max-w-6xl mx-auto px-6 py-8">
  <div class="border-b-2 border-wsj-text pb-4 mb-8">
    <div class="text-xs uppercase tracking-widest text-wsj-muted font-sans">RAG Experiment</div>
    <h1 class="text-3xl font-bold mt-1">Benchmark Timeline</h1>
    <p class="text-sm text-wsj-muted mt-2">Navigate with <kbd class="bg-gray-200 px-1.5 py-0.5 rounded text-xs font-mono">&larr;</kbd> <kbd class="bg-gray-200 px-1.5 py-0.5 rounded text-xs font-mono">&rarr;</kbd> arrow keys on individual pages</p>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    ${runs.map((r, i) => {
      if (r.type === "skill") {
        const acc = r.json.routing.accuracy;
        return `<a href="${r.label}.html" class="block bg-white border border-wsj-border rounded-lg p-5 shadow-sm hover:shadow-md transition-shadow">
          <div class="text-xs text-wsj-muted mb-1">Skill Routing &middot; Run ${i+1}</div>
          <div class="font-bold text-lg mb-2">${r.label.replace(/_/g," ")}</div>
          <div class="flex justify-between text-sm">
            <span>Accuracy: <strong class="${acc===100?"text-wsj-green":""}">${acc}%</strong></span>
            <span class="text-wsj-muted">${r.json.routing.avg_query_ms.toFixed(0)}ms/query</span>
          </div>
        </a>`;
      } else {
        const s = r.json.summary;
        return `<a href="${r.label}.html" class="block bg-white border border-wsj-border rounded-lg p-5 shadow-sm hover:shadow-md transition-shadow">
          <div class="text-xs text-wsj-muted mb-1">Document RAG &middot; Run ${i+1}</div>
          <div class="font-bold text-lg mb-2">${r.label.replace(/_/g," ").replace(/\b\w/g,c=>c.toUpperCase())}</div>
          <div class="flex justify-between text-sm">
            <span>Grounded: <strong>${s.grounded}/${s.total}</strong> (${s.grounded_pct}%)</span>
            <span class="text-wsj-muted">${(s.avg_query_ms/1000).toFixed(1)}s/query</span>
          </div>
          <div class="text-xs text-wsj-muted mt-1">${r.json.document.tokens.toLocaleString()} tokens &middot; ${r.json.document.windows} windows</div>
        </a>`;
      }
    }).join("")}
  </div>

  <div class="text-center text-xs text-wsj-muted border-t border-wsj-border pt-4 mt-8">
    RAG Experiment &middot; Gaucho AI
  </div>
</div></body></html>`;

fs.writeFileSync(path.join(DOCS_DIR, "index.html"), indexHtml);
console.log(`  Generated: docs/index.html`);
console.log(`\nDone! ${runs.length} run(s) processed.`);
