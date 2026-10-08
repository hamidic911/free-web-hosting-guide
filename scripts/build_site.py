#!/usr/bin/env python3
"""Generate all derived repository artifacts from services.yml."""
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
import html
import json
import shutil
import yaml

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DATA_FILE = ROOT / "services.yml"

CATEGORIES = {
    "static-hosting": "Static Hosting",
    "frontend-platforms": "Frontend Platforms",
    "serverless-edge": "Serverless & Edge Compute",
    "containers-cloud": "Containers & Full-Stack Cloud",
    "databases-baas": "Managed Databases & BaaS",
    "object-storage": "Object Storage",
    "free-vps": "Free VPS & Compute",
    "ai-gpu-apps": "AI, GPU & Data Apps",
    "php-traditional": "PHP & Traditional Hosting",
    "no-code": "No-Code App Builders",
    "documentation": "Documentation Hosting",
}

FREE_CLASSES = {
    "Always Free": "A permanent no-cost allowance subject to published limits; billing setup may still be required.",
    "Free Plan": "A permanent $0 plan with defined resource and feature limits.",
    "Free Development": "Free mainly for staging/development; production requires payment.",
    "Free Credits": "A spend-down or time-limited monetary credit balance.",
    "Trial": "Time-limited access that eventually ends or requires a paid plan.",
}

START_ROWS = [
    ("Static site / docs", "Cloudflare Pages or GitHub Pages", "GitHub Pages is restricted for online business, e-commerce, and commercial SaaS."),
    ("Next.js / frontend", "Netlify or Vercel Hobby", "Vercel Hobby is non-commercial; Netlify uses monthly credits."),
    ("Docker app / API", "Google Cloud Run, Koyeb, or Render", "Cloud Run needs billing; Koyeb requires a card; Render free instances are not for production."),
    ("Edge API", "Cloudflare Workers", "100,000 requests/day and 10 ms CPU/request on the Free plan."),
    ("PostgreSQL", "Neon or Supabase", "Neon has per-project quotas; Supabase may pause low-activity free projects."),
    ("SQLite at the edge", "Turso", "5 GB total storage plus row-operation quotas."),
    ("Object storage", "Cloudflare R2 or Backblaze B2", "Finite free storage allowances; R2 requires billing setup."),
    ("Free VPS", "Oracle Cloud Always Free", "Billing verification and an idle-resource policy apply."),
    ("AI/data demo", "Hugging Face Spaces or Streamlit Community Cloud", "Free compute and commercial/data-use rules are more restrictive than ordinary hosting."),
    ("GPU notebook", "Kaggle Notebooks or Google Colab", "Free accelerator availability is temporary and quota-limited."),
    ("No-code app", "Bubble", "Free is a development environment; production requires payment."),
    ("Open-source documentation", "Read the Docs Community or GitLab Pages", "Read the Docs Community is for open-source docs; GitLab CI minutes are limited on Free."),
]

STYLE = r""":root{
  --bg:#f4f7fb; --bg-soft:#eef3ff; --surface:#ffffff; --surface-2:#f8faff;
  --text:#172033; --muted:#64748b; --border:#dce4f1;
  --primary:#4f46e5; --primary-2:#6366f1; --cyan:#0ea5e9; --teal:#10b981;
  --amber:#f59e0b; --red:#ef4444; --shadow:0 14px 40px rgba(42,58,100,.10);
  --shadow-soft:0 6px 18px rgba(42,58,100,.07);
}
html[data-theme="dark"]{
  --bg:#0b1220; --bg-soft:#101a2d; --surface:#111b30; --surface-2:#0e1729;
  --text:#edf2ff; --muted:#aab8d1; --border:#24324d;
  --primary:#818cf8; --primary-2:#6366f1; --cyan:#38bdf8; --teal:#34d399;
  --amber:#fbbf24; --red:#fb7185; --shadow:0 18px 45px rgba(0,0,0,.28); --shadow-soft:0 8px 22px rgba(0,0,0,.20);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:linear-gradient(180deg,var(--bg) 0%,var(--bg-soft) 44%,var(--bg) 100%);color:var(--text);font:16px/1.65 ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;min-height:100vh}
body::before{content:"";position:fixed;inset:-25vh -10vw auto auto;width:55vw;height:55vw;background:radial-gradient(circle,rgba(99,102,241,.13),transparent 62%);pointer-events:none;z-index:-1}
body::after{content:"";position:fixed;inset:auto auto -25vh -15vw;width:55vw;height:55vw;background:radial-gradient(circle,rgba(14,165,233,.10),transparent 64%);pointer-events:none;z-index:-1}
a{color:var(--primary);text-decoration:none} a:hover{text-decoration:underline}
.container{width:min(1240px,calc(100% - 36px));margin:auto}
.hero{position:relative;overflow:hidden;padding:72px 0 54px;background:linear-gradient(135deg,#312e81 0%,#4f46e5 38%,#0ea5e9 100%);color:#fff;box-shadow:0 18px 50px rgba(49,46,129,.22)}
.hero::after{content:"";position:absolute;right:-8%;top:-55%;width:48vw;height:48vw;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.22),transparent 66%)}
.hero-inner{position:relative;z-index:1}
.eyebrow{display:inline-flex;align-items:center;gap:8px;padding:7px 12px;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.12);backdrop-filter:blur(8px);border-radius:999px;font-size:.82rem;font-weight:700;letter-spacing:.02em}
.eyebrow::before{content:"";width:8px;height:8px;border-radius:50%;background:#34d399;box-shadow:0 0 0 5px rgba(52,211,153,.15)}
h1{font-size:clamp(2.25rem,5vw,4.25rem);line-height:1.02;letter-spacing:-.04em;margin:.25em 0 .18em;max-width:920px}
h2{line-height:1.18;letter-spacing:-.02em}
.lead{color:rgba(255,255,255,.88);max-width:920px;font-size:1.12rem}
.hero-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}
.button{display:inline-flex;align-items:center;justify-content:center;gap:8px;border-radius:12px;padding:10px 15px;font-weight:700;text-decoration:none;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.12);color:#fff;backdrop-filter:blur(8px);cursor:pointer}
.button:hover{background:rgba(255,255,255,.20);text-decoration:none}
.button.primary{background:#fff;color:#3730a3;border-color:#fff}
.theme-toggle{cursor:pointer}
.nav-wrap{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--surface) 88%,transparent);backdrop-filter:blur(14px);border-bottom:1px solid var(--border)}
.nav{display:flex;flex-wrap:wrap;gap:9px;padding:14px 0}
.nav a{border:1px solid var(--border);background:var(--surface);border-radius:999px;padding:7px 12px;text-decoration:none;color:var(--text);font-size:.9rem;font-weight:600;box-shadow:0 2px 8px rgba(31,41,55,.04)}
.nav a:hover{border-color:var(--primary);color:var(--primary);transform:translateY(-1px)}
main{padding:34px 0 70px}
.section-kicker{color:var(--primary);font-size:.82rem;font-weight:800;text-transform:uppercase;letter-spacing:.08em}
.card{background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:24px;margin:18px 0;box-shadow:var(--shadow-soft);transition:transform .18s ease,box-shadow .18s ease}
.card:hover{box-shadow:var(--shadow);transform:translateY(-1px)}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(175px,1fr));gap:11px;margin:16px 0}
.fact{background:linear-gradient(180deg,var(--surface-2),var(--surface));border:1px solid var(--border);padding:12px 14px;border-radius:14px}
.fact strong{display:block;color:var(--text);font-size:.87rem}
.tools{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0}
.tools input{flex:1;min-width:260px;background:var(--surface);color:var(--text);border:1px solid var(--border);border-radius:14px;padding:14px 16px;box-shadow:var(--shadow-soft);outline:none}
.tools input:focus{border-color:var(--primary);box-shadow:0 0 0 4px color-mix(in srgb,var(--primary) 15%,transparent)}
.table-wrap{overflow:auto;border:1px solid var(--border);border-radius:18px;background:var(--surface);box-shadow:var(--shadow-soft)}
.matrix{width:100%;border-collapse:separate;border-spacing:0;min-width:1120px;background:var(--surface)}
th,td{border-bottom:1px solid var(--border);padding:13px 14px;text-align:left;vertical-align:top}
th{background:linear-gradient(135deg,#eef2ff,#eff6ff);color:#27324b;position:sticky;top:0;z-index:1;font-size:.83rem;text-transform:uppercase;letter-spacing:.05em}
html[data-theme="dark"] th{background:linear-gradient(135deg,#17213a,#10233a);color:#dbe6ff}
tr:last-child td{border-bottom:0}
tbody tr:hover td{background:color-mix(in srgb,var(--primary) 4%,var(--surface))}
.badge{display:inline-flex;align-items:center;border:1px solid var(--border);border-radius:999px;padding:4px 9px;font-size:.82rem;background:var(--surface-2);font-weight:700}
.badge.success,.policy-allowed{color:#047857;background:#ecfdf5;border-color:#a7f3d0}.badge.warning,.policy-restricted{color:#a16207;background:#fffbeb;border-color:#fde68a}.badge.danger,.policy-no{color:#b91c1c;background:#fef2f2;border-color:#fecaca}
html[data-theme="dark"] .badge.success,html[data-theme="dark"] .policy-allowed{color:#6ee7b7;background:#07362a;border-color:#0f6b54}html[data-theme="dark"] .badge.warning,html[data-theme="dark"] .policy-restricted{color:#fcd34d;background:#3b2b08;border-color:#70520a}html[data-theme="dark"] .badge.danger,html[data-theme="dark"] .policy-no{color:#fda4af;background:#43131b;border-color:#6f2432}
.status-yes{color:#047857;font-weight:800}.status-no{color:#b91c1c;font-weight:800}
.muted{color:var(--muted)}.small{font-size:.92rem}
.notice{border-left:4px solid var(--amber)}
footer{border-top:1px solid var(--border);padding:28px 0 55px;color:var(--muted)}
code{background:color-mix(in srgb,var(--primary) 8%,var(--surface));padding:3px 6px;border-radius:7px}
.category-header{margin-bottom:24px}.category-header h1{color:var(--text);margin-bottom:.15em}.category-header .lead{color:var(--muted)}
.pill-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
@media (max-width:800px){.container{width:min(100% - 22px,1240px)}.hero{padding:52px 0 42px}.nav{overflow-x:auto;flex-wrap:nowrap;padding-bottom:12px}.nav a{white-space:nowrap}.card{padding:18px;border-radius:16px}.matrix{min-width:980px}}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}.card,.nav a:hover{transform:none}}
"""

APP = r"""document.addEventListener('DOMContentLoaded', () => {
  const body = document.querySelector('#servicesBody');
  const search = document.querySelector('#searchInput');
  const status = document.querySelector('#resultStatus');
  const themeToggle = document.querySelector('#themeToggle');

  const setTheme = (theme) => {
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem('fwg-theme', theme); } catch (_) {}
    if (themeToggle) themeToggle.textContent = theme === 'dark' ? '☀️ Light mode' : '🌙 Dark mode';
  };
  let savedTheme = null;
  try { savedTheme = localStorage.getItem('fwg-theme'); } catch (_) {}
  const preferredTheme = savedTheme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  setTheme(preferredTheme);
  if (themeToggle) themeToggle.addEventListener('click', () => setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'));

  const policyClass = (value) => value === 'Allowed' ? 'success' : value === 'Restricted' ? 'warning' : 'danger';
  const cardLabel = (value) => value === 'Required' ? 'Card required' : value === 'Conditional' ? 'Card conditional' : 'No card';

  const load = async () => {
    try {
      const response = await fetch('services.json', {cache: 'no-store'});
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      const services = Array.isArray(data.services) ? data.services : [];
      const render = () => {
        const q = (search.value || '').trim().toLowerCase();
        body.replaceChildren();
        let count = 0;
        for (const service of services) {
          const haystack = [service.name, service.category, service.free_class, service.card_requirement, service.commercial_policy, service.commercial_note, service.hard_limit, service.best_for, service.brilliant_feature].join(' ').toLowerCase();
          if (q && !haystack.includes(q)) continue;
          const row = document.createElement('tr');
          const cells = [
            {value: service.name, type: 'name'},
            {value: service.category},
            {value: service.free_class, type: 'badge'},
            {value: cardLabel(service.card_requirement), type: 'card'},
            {value: service.commercial_policy, type: 'policy'},
            {value: service.sleeps ? 'Yes' : 'No', type: 'bool'},
            {value: service.production_ready ? 'Yes' : 'No', type: 'bool'},
            {value: service.hard_limit}
          ];
          cells.forEach(({value, type}) => {
            const cell = document.createElement('td');
            if (type === 'name') { const strong = document.createElement('strong'); strong.textContent = value; cell.appendChild(strong); }
            else if (type === 'badge' || type === 'card') { const badge = document.createElement('span'); badge.className = 'badge'; badge.textContent = value; cell.appendChild(badge); }
            else if (type === 'policy') { const badge = document.createElement('span'); badge.className = `badge policy-${policyClass(value)}`; badge.textContent = value; cell.appendChild(badge); }
            else if (type === 'bool') { cell.textContent = value; cell.className = value === 'Yes' ? 'status-yes' : 'status-no'; }
            else cell.textContent = value;
            row.appendChild(cell);
          });
          const sourceCell = document.createElement('td');
          const link = document.createElement('a'); link.href = service.official_source; link.target = '_blank'; link.rel = 'noopener'; link.textContent = 'Official ↗';
          sourceCell.appendChild(link); row.appendChild(sourceCell); body.appendChild(row); count += 1;
        }
        if (status) status.textContent = `${count} of ${services.length} services shown`;
      };
      search.addEventListener('input', render); render();
    } catch (error) {
      body.innerHTML = '<tr><td colspan="9">Unable to load services.json. Check the deployed data artifact.</td></tr>';
      if (status) status.textContent = 'Data load failed'; console.error(error);
    }
  };
  load();
});
"""


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def official_host(url: str) -> str:
    return urlparse(url).netloc


def write_json(data: dict) -> None:
    payload = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    (ROOT / "services.json").write_text(payload, encoding="utf-8")
    (SITE / "services.json").write_text(payload, encoding="utf-8")


def write_readme(data: dict) -> None:
    services = data["services"]
    lines = [
        f"# {data['metadata']['title']}",
        "",
        "A community-maintained directory of free-tier web hosting, serverless compute, managed databases, object storage, virtual machines, and AI/data application platforms.",
        "",
        "This guide is intentionally factual: no star ratings, no S/A/B tiers, and no affiliate rankings. Each service exposes the pricing model, card requirement, commercial policy, sleep/reclaim behavior, production suitability, hard limit, and primary provider source.",
        "",
        f"**Last verified:** {data['metadata']['last_updated']}  ",
        "**Canonical source:** `services.yml`  ",
        "**Generated outputs:** `services.json`, `site/services.json`, the site pages, sitemap, and this README.  ",
        "",
        "## Start Here: choose by architecture",
        "",
        "| What are you building? | Starting point | Main catch |",
        "|---|---|---|",
    ]
    lines.extend(f"| **{a}** | **{b}** | {c} |" for a, b, c in START_ROWS)
    lines += [
        "",
        "## How to read the guide",
        "",
        "The labels below describe the **pricing model**, not quality. Commercial policy, card requirement, sleep/pause, reclaim, custom domain, and production suitability are separate fields.",
        "",
        "| Label | Meaning |",
        "|---|---|",
    ]
    lines.extend(f"| **{k}** | {v} |" for k, v in FREE_CLASSES.items())
    lines += [
        "",
        "## Commercial policy",
        "",
        "- **Allowed:** the provider's current terms permit commercial use of the relevant service/free allowance, subject to its limits.",
        "- **Restricted:** commercial use is limited by service scope or provider terms; the service needs closer inspection before deployment.",
        "- **No:** the relevant free plan is explicitly non-commercial.",
        "",
        "## Comparison matrix",
        "",
        "| Service | Category | Free model | Card | Commercial | Sleeps | Production | Hard limit / catch |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for s in services:
        lines.append(
            f"| **{s['name']}** | {CATEGORIES[s['category']]} | {s['free_class']} | {s['card_requirement']} | **{s['commercial_policy']}** | {'Yes' if s['sleeps'] else 'No'} | {'Yes' if s['production_ready'] else 'No'} | {s['hard_limit']} |"
        )
    lines += ["", "## Service details", ""]
    for category, title in CATEGORIES.items():
        subset = [s for s in services if s["category"] == category]
        if not subset:
            continue
        lines += [f"### {title}", ""]
        for s in subset:
            lines += [
                f"#### {s['name']}",
                f"- **Best for:** {s['best_for']}",
                f"- **Free model:** {s['free_class']}",
                f"- **Card requirement:** {s['card_requirement']}",
                f"- **Commercial policy:** **{s['commercial_policy']}** — {s['commercial_note']}",
                f"- **Sleep / pause:** {'Yes' if s['sleeps'] else 'No'}",
                f"- **Reclaim policy:** {s['reclaim_policy']}",
                f"- **Custom domain:** {'Yes' if s['custom_domain'] else 'No'}",
                f"- **Production-ready for the free use case:** {'Yes' if s['production_ready'] else 'No'}",
                f"- **Hard limit / catch:** {s['hard_limit']}",
                f"- **Brilliant feature:** {s['brilliant_feature']}",
                f"- **Official source:** [{official_host(s['official_source'])}]({s['official_source']})",
                f"- **Last verified:** {s['last_verified']}",
                "",
            ]
    lines += [
        "## Self-hosted PaaS control planes",
        "",
        "> These are software you install on a server you already control. They are not hosting providers themselves.",
        "",
        "- **Coolify** — self-hosted Docker-oriented PaaS/control plane.",
        "- **Dokploy** — lightweight self-hosted deployment platform.",
        "- **CapRover** — self-hosted PaaS with a simple app deployment model.",
        "- **Dokku** — lightweight Heroku-style self-hosted platform.",
        "",
        "## Free-Tier Graveyard",
        "",
        "| Service | Status |",
        "|---|---|",
        "| **000WebHost** | Shut down; not a current free-hosting option. |",
        "| **Heroku Free Dynos** | Permanent free dyno tier removed. |",
        "| **PlanetScale Hobby Free** | Permanent free tier removed. |",
        "| **Railway Free** | Credit/trial-based for new accounts rather than a permanent free plan. |",
        "| **Fly.io Free** | Legacy allowances are not a current general free plan for new organizations. |",
        "| **Glitch hosting** | No longer a current general hosting recommendation. |",
        "",
        "## Before you deploy",
        "",
        "Check what happens at the quota, whether a payment method is required, whether the service sleeps or pauses, whether inactive resources are deleted or reclaimed, whether the free plan permits your commercial use, whether storage is persistent, and whether the region/custom-domain/email/backups you need are included.",
        "",
        "## Maintenance",
        "",
        "`services.yml` is the single source of truth. Run `python scripts/build_site.py` after changing provider data. Then run `python scripts/validate_repo.py`. CI performs the same build-and-validate sequence before deployment.",
        "",
        "No affiliate links. No star ratings. No S/A/B rankings. No unqualified \"unlimited\", \"best\", or \"free forever\" claims.",
        "",
    ]
    (ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def write_index() -> None:
    nav = "".join(f'<a href="{esc(k)}.html">{esc(v)}</a>' for k, v in CATEGORIES.items())
    index = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Free Web Hosting &amp; Cloud 2026 | Verified Free-Tier Directory</title>
<meta name="description" content="Verified 2026 directory of free web hosting, serverless compute, managed databases, object storage, VPS and AI/data platforms. Limits, commercial policies and signup requirements are shown clearly.">
<link rel="canonical" href="https://hamidic911.github.io/free-web-hosting-guide/">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="hero"><div class="container hero-inner">
<div class="eyebrow">Primary-source directory · Checked October 2026</div>
<h1>Free Hosting Without the Hype.</h1>
<p class="lead">A practical, community-maintained directory of genuinely free web hosting and cloud infrastructure. We put the catch beside the quota so you can choose by architecture, policy, and real limits.</p>
<div class="hero-actions">
<a class="button primary" href="#matrix">Browse verified services ↓</a>
<button class="button theme-toggle" id="themeToggle" type="button" aria-label="Toggle color theme">🌙 Dark mode</button>
</div>
</div></header>
<nav class="nav-wrap"><div class="container nav" aria-label="Categories">{nav}</div></nav>
<main class="container">
<section class="card">
<div class="section-kicker">Start here</div>
<h2>Choose the architecture first</h2>
<p>Then check the commercial policy, card requirement, sleep/reclaim behavior, production suitability and hard limit. A bigger quota is not automatically a better fit.</p>
<div class="facts">
<div class="fact"><strong>Coverage</strong><br>36 current services</div>
<div class="fact"><strong>Static</strong><br>Cloudflare Pages · GitHub Pages · Firebase</div>
<div class="fact"><strong>Frontend</strong><br>Netlify · Vercel Hobby</div>
<div class="fact"><strong>Containers</strong><br>Cloud Run · Koyeb · Render</div>
<div class="fact"><strong>Databases</strong><br>Neon · Supabase · Turso · Atlas</div>
<div class="fact"><strong>Storage</strong><br>R2 · B2</div>
<div class="fact"><strong>VPS</strong><br>Oracle · Google Cloud</div>
<div class="fact"><strong>Docs / No-code</strong><br>Read the Docs · Bubble</div>
</div>
</section>
<section id="matrix">
<div class="section-kicker">Verified comparison</div>
<h2>Service matrix</h2>
<p id="resultStatus" class="muted small" aria-live="polite">Loading services…</p>
<div class="tools"><input id="searchInput" type="search" placeholder="Search provider, category, database, limit, policy…" autocomplete="off" aria-label="Search verified services"></div>
<div class="table-wrap"><table class="matrix"><thead><tr>
<th>Service</th><th>Category</th><th>Free model</th><th>Card</th><th>Commercial</th><th>Sleeps</th><th>Production</th><th>Hard limit / catch</th><th>Source</th>
</tr></thead><tbody id="servicesBody"></tbody></table></div>
</section>
</main>
<footer><div class="container">Canonical data: <code>services.yml</code> · Last verified: {esc('2026-10-08')} · MIT License</div></footer>
<script src="app.js"></script>
</body>
</html>
'''
    (SITE / "index.html").write_text(index, encoding="utf-8")


def write_category_pages(data: dict) -> None:
    services = data["services"]
    nav = "".join(f'<a href="{esc(k)}.html">{esc(v)}</a>' for k, v in CATEGORIES.items())
    allowed = {"index.html"}
    for category in CATEGORIES:
        allowed.add(f"{category}.html")
    for path in SITE.glob("*.html"):
        if path.name not in allowed:
            path.unlink()

    for category, title in CATEGORIES.items():
        subset = [s for s in services if s["category"] == category]
        cards = []
        for s in subset:
            card = f"""<article class="card">
<h2>{esc(s['name'])}</h2>
<p>{esc(s['best_for'])}</p>
<div class="facts">
<div class="fact"><strong>Free model</strong><br>{esc(s['free_class'])}</div>
<div class="fact"><strong>Card</strong><br>{esc(s['card_requirement'])}</div>
<div class="fact"><strong>Commercial</strong><br>{esc(s['commercial_policy'])}</div>
<div class="fact"><strong>Sleep / pause</strong><br>{'Yes' if s['sleeps'] else 'No'}</div>
<div class="fact"><strong>Custom domain</strong><br>{'Yes' if s['custom_domain'] else 'No'}</div>
<div class="fact"><strong>Production</strong><br>{'Yes' if s['production_ready'] else 'No'}</div>
</div>
<p><strong>Limit:</strong> {esc(s['hard_limit'])}</p>
<p><strong>Catch:</strong> {esc(s['reclaim_policy'])} {esc(s['commercial_note'])}</p>
<p><strong>Feature:</strong> {esc(s['brilliant_feature'])}</p>
<p><a href="{esc(s['official_source'])}" target="_blank" rel="noopener">Official source ↗</a> · Verified {esc(s['last_verified'])}</p>
</article>"""
            cards.append(card)
        page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Free {esc(title)} 2026 | Verified Limits</title>
<meta name="description" content="Verified 2026 free {esc(title.lower())} services, limits, commercial policies, card requirements, and sleep/reclaim rules.">
<link rel="canonical" href="https://hamidic911.github.io/free-web-hosting-guide/{esc(category)}.html">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="hero"><div class="container hero-inner"><div class="eyebrow">Verified category · October 2026</div><h1>Free {esc(title)} (2026)</h1><p class="lead">Provider limits and policy traps are shown directly beside each service.</p><div class="hero-actions"><a class="button primary" href="index.html">← Directory</a><button class="button theme-toggle" id="themeToggle" type="button" aria-label="Toggle color theme">🌙 Dark mode</button></div></div></header>
<nav class="nav-wrap"><div class="container nav" aria-label="Categories">{nav}</div></nav>
<main class="container"><div class="section-kicker">Category guide</div>{''.join(cards)}</main>
<footer><div class="container">Last verified: 2026-10-08 · MIT License</div></footer>
<script src="app.js"></script>
</body>
</html>
"""
        (SITE / f"{category}.html").write_text(page, encoding="utf-8")


def write_sitemap(data: dict) -> None:
    urls = [
        "https://hamidic911.github.io/free-web-hosting-guide/",
        *[f"https://hamidic911.github.io/free-web-hosting-guide/{category}.html" for category in CATEGORIES],
    ]
    body = "".join(f"  <url><loc>{u}</loc><lastmod>{esc(data['metadata']['last_updated'])}</lastmod></url>\n" for u in urls)
    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}</urlset>\n",
        encoding="utf-8",
    )
    (SITE / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        "Sitemap: https://hamidic911.github.io/free-web-hosting-guide/sitemap.xml\n",
        encoding="utf-8",
    )


def main() -> None:
    SITE.mkdir(parents=True, exist_ok=True)
    data = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("services"), list):
        raise SystemExit("services.yml does not contain a services list")
    write_json(data)
    write_readme(data)
    write_index()
    write_category_pages(data)
    write_sitemap(data)
    (SITE / "style.css").write_text(STYLE, encoding="utf-8")
    (SITE / "app.js").write_text(APP, encoding="utf-8")
    print(f"Generated repository artifacts for {len(data['services'])} services.")


if __name__ == "__main__":
    main()
