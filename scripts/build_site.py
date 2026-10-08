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
]

STYLE = r""":root{--bg:#0b1020;--panel:#11182b;--panel2:#0e1526;--text:#e8eefc;--muted:#aebbd4;--border:#24304a;--accent:#7aa2ff;--good:#55d187;--warn:#f3c969;--bad:#ff7b7b}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
a{color:var(--accent)}
.container{width:min(1240px,calc(100% - 32px));margin:auto}
.hero{padding:52px 0 30px;border-bottom:1px solid var(--border)}
h1{font-size:clamp(2rem,4vw,3.5rem);line-height:1.08;margin:.1em 0}
h2{line-height:1.2}
.lead{color:var(--muted);max-width:980px;font-size:1.08rem}
.nav{display:flex;flex-wrap:wrap;gap:10px;padding:20px 0}
.nav a{border:1px solid var(--border);background:var(--panel);border-radius:999px;padding:7px 13px;text-decoration:none;color:var(--text)}
.nav a:hover{border-color:var(--accent)}
main{padding:28px 0 64px}
.card{background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:20px;margin:16px 0}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin:14px 0}
.fact{background:var(--panel2);border:1px solid var(--border);padding:12px;border-radius:10px}
.tools{display:flex;gap:12px;flex-wrap:wrap;margin:16px 0}
.tools input{flex:1;min-width:260px;background:var(--panel);color:var(--text);border:1px solid var(--border);border-radius:10px;padding:12px}
.table-wrap{overflow:auto;border:1px solid var(--border);border-radius:12px}
.matrix{width:100%;border-collapse:collapse;min-width:1120px;background:var(--panel2)}
th,td{border-bottom:1px solid var(--border);padding:12px;text-align:left;vertical-align:top}
th{background:var(--panel);position:sticky;top:0;z-index:1}
.badge{display:inline-block;border:1px solid var(--border);border-radius:999px;padding:3px 9px;font-size:.86rem;background:var(--panel2)}
.muted{color:var(--muted)}
.small{font-size:.92rem}
.notice{border-left:4px solid var(--warn)}
footer{border-top:1px solid var(--border);padding:24px 0 50px;color:var(--muted)}
code{background:#080d19;padding:2px 5px;border-radius:5px}
"""

APP = r"""document.addEventListener('DOMContentLoaded', () => {
  const body = document.querySelector('#servicesBody');
  const search = document.querySelector('#searchInput');
  const status = document.querySelector('#resultStatus');
  if (!body || !search) return;

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
          const haystack = [
            service.name, service.category, service.free_class,
            service.card_requirement, service.commercial_policy,
            service.commercial_note, service.hard_limit,
            service.best_for, service.brilliant_feature
          ].join(' ').toLowerCase();
          if (q && !haystack.includes(q)) continue;

          const row = document.createElement('tr');
          const cells = [
            service.name,
            service.category,
            service.free_class,
            service.card_requirement,
            service.commercial_policy,
            service.sleeps ? 'Yes' : 'No',
            service.production_ready ? 'Yes' : 'No',
            service.hard_limit
          ];
          cells.forEach((value, index) => {
            const cell = document.createElement('td');
            if (index === 0) {
              const strong = document.createElement('strong');
              strong.textContent = value;
              cell.appendChild(strong);
            } else {
              cell.textContent = value;
            }
            row.appendChild(cell);
          });

          const sourceCell = document.createElement('td');
          const link = document.createElement('a');
          link.href = service.official_source;
          link.target = '_blank';
          link.rel = 'noopener';
          link.textContent = 'Official';
          sourceCell.appendChild(link);
          row.appendChild(sourceCell);
          body.appendChild(row);
          count += 1;
        }
        if (status) status.textContent = `${count} of ${services.length} services shown`;
      };

      search.addEventListener('input', render);
      render();
    } catch (error) {
      body.innerHTML = '<tr><td colspan="9">Unable to load services.json. Check the deployed data artifact.</td></tr>';
      if (status) status.textContent = 'Data load failed';
      console.error(error);
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
<header class="hero"><div class="container">
<h1>Awesome Free Web Hosting &amp; Cloud 2026</h1>
<p class="lead">A factual, community-maintained directory of free-tier hosting and cloud infrastructure. The catch is shown beside the quota so you can choose by architecture instead of marketing language.</p>
</div></header>
<nav class="container nav" aria-label="Categories">{nav}</nav>
<main class="container">
<section class="card"><h2>Start Here</h2>
<p>Choose the architecture first, then check the commercial policy, card requirement, sleep/reclaim behavior, production suitability and hard limit.</p>
<div class="facts">
<div class="fact"><strong>Static</strong><br>Cloudflare Pages / GitHub Pages</div>
<div class="fact"><strong>Frontend</strong><br>Netlify / Vercel Hobby</div>
<div class="fact"><strong>Containers</strong><br>Cloud Run / Koyeb / Render</div>
<div class="fact"><strong>Databases</strong><br>Neon / Supabase / Turso / Atlas</div>
<div class="fact"><strong>Storage</strong><br>R2 / B2</div>
<div class="fact"><strong>VPS</strong><br>Oracle Cloud Always Free</div>
</div></section>
<section>
<h2>Verified Service Matrix</h2>
<p id="resultStatus" class="muted small" aria-live="polite">Loading services…</p>
<div class="tools"><input id="searchInput" type="search" placeholder="Search provider, category, database, limit, policy…" autocomplete="off"></div>
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
    # Remove previously generated category HTML pages, preventing obsolete pages from surviving a rename.
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
            cards.append(
                f'''<article class="card">
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
<p><a href="{esc(s['official_source'])}" target="_blank" rel="noopener">Official source</a> · Verified {esc(s['last_verified'])}</p>
</article>'''
            )
        page = f'''<!doctype html>
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
<header class="hero"><div class="container"><h1>Free {esc(title)} (2026)</h1><p class="lead">Provider limits and policy traps are shown directly beside each service.</p></div></header>
<main class="container"><p><a href="index.html">← Back to directory</a></p>{''.join(cards)}</main>
<footer><div class="container">Last verified: 2026-10-08 · MIT License</div></footer>
</body>
</html>
'''
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
