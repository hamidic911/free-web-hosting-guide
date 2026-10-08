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
  --paper:#EDEAE2;
  --ink:#16181D;
  --blue:#1F4FD8;
  --trap:#E0541B;
  --ok:#2F6F4F;
  --line:#CDC8BB;
  --surface:#F7F5EF;
  --surface-strong:#FFFFFF;
  --muted:#5E615F;
  --soft-blue:#E9EFFC;
  --soft-trap:#FBEDE7;
  --soft-ok:#EAF3ED;
  --focus:rgba(31,79,216,.22);
  --shadow:0 14px 30px rgba(22,24,29,.07);
}
html[data-theme="dark"]{
  --paper:#14171B;
  --ink:#F4F3EE;
  --blue:#7EA2FF;
  --trap:#FF8A55;
  --ok:#73B18D;
  --line:#32363D;
  --surface:#1B1F24;
  --surface-strong:#20252B;
  --muted:#B5B7B4;
  --soft-blue:#202A3D;
  --soft-trap:#3A251D;
  --soft-ok:#1C3025;
  --focus:rgba(126,162,255,.25);
  --shadow:0 16px 34px rgba(0,0,0,.24);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.65 ui-sans-serif,"Space Grotesk","Arial Narrow",Aptos,system-ui,sans-serif;min-height:100vh}
body::before{content:"";display:block;height:4px;background:var(--blue)}
a{color:var(--blue);text-underline-offset:3px}
a:hover{color:var(--ink)}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid var(--focus);outline-offset:3px}
.container{width:min(1180px,calc(100% - 32px));margin-inline:auto}
.hero{padding:58px 0 46px;border-bottom:1px solid var(--line);background:var(--paper)}
.hero-grid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(340px,.85fr);gap:40px;align-items:end}
.eyebrow{display:inline-flex;align-items:center;gap:9px;color:var(--blue);font-size:.78rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase}
.eyebrow::before{content:"";width:9px;height:9px;background:var(--trap);display:inline-block;border-radius:2px}
h1{font-size:clamp(2.45rem,5vw,5.2rem);line-height:.98;letter-spacing:-.055em;margin:.22em 0 .22em;max-width:900px}
h2{line-height:1.15;letter-spacing:-.025em}
.lead{font-size:1.08rem;max-width:760px;color:var(--muted)}
.hero-tool{border:1px solid var(--ink);background:var(--surface-strong);padding:22px;box-shadow:var(--shadow);align-self:stretch;display:flex;flex-direction:column;justify-content:center}
.hero-tool-label{font-weight:800;margin-bottom:10px}
.architecture-picker{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:clamp(1.15rem,2vw,1.45rem);line-height:1.35}
.architecture-picker select{font:inherit;font-weight:800;color:var(--blue);background:var(--surface);border:1px solid var(--line);padding:8px 34px 8px 10px;border-radius:8px}
.hero-note{color:var(--muted);font-size:.9rem;margin:12px 0 0}
.theme-toggle{margin-top:14px;align-self:flex-start;display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line);background:var(--paper);color:var(--ink);padding:8px 11px;border-radius:8px;font-weight:700;cursor:pointer}
.icon{width:17px;height:17px;display:inline-block;flex:none}
.nav-wrap{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--paper) 93%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.nav{display:flex;gap:18px;overflow:auto;padding:12px 0;scrollbar-width:thin}
.nav a{white-space:nowrap;text-decoration:none;color:var(--muted);font-size:.88rem;font-weight:700;padding-block:3px;border-bottom:2px solid transparent}
.nav a:hover{color:var(--blue);border-color:var(--blue)}
main{padding:42px 0 72px}
.section-kicker{color:var(--blue);font-size:.78rem;font-weight:900;text-transform:uppercase;letter-spacing:.1em}
.section-head{display:flex;justify-content:space-between;gap:20px;align-items:end;margin-bottom:14px}
.section-head h2{margin:5px 0 0;font-size:clamp(1.7rem,3vw,2.35rem)}
.meta-line{color:var(--muted);font-size:.9rem}
.architecture-results{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:18px 0 44px}
.condition-card{background:var(--surface-strong);border:1px solid var(--line);padding:18px;position:relative;min-height:190px}
.condition-card::before{content:"";position:absolute;inset-block:0 auto 0;inset-inline-start:0;width:4px;background:var(--ok)}
.condition-card.has-trap::before{background:var(--trap)}
.condition-top{display:flex;justify-content:space-between;gap:10px;align-items:start;margin-bottom:10px}
.condition-top h3{margin:0;font-size:1.08rem;line-height:1.2}
.micro{font-size:.74rem;color:var(--muted);font-family:"JetBrains Mono","IBM Plex Mono","Cascadia Mono",monospace;white-space:nowrap}
.limit{font:800 1.03rem/1.45 "JetBrains Mono","IBM Plex Mono","Cascadia Mono",monospace;letter-spacing:-.02em;margin:8px 0 12px}
.conditions{display:grid;grid-template-columns:1fr 1fr;gap:7px 12px;margin-top:10px}
.condition-line{font-size:.78rem;color:var(--muted);display:flex;gap:7px;align-items:center}
.condition-dot{width:7px;height:7px;background:var(--ok);flex:none}
.condition-line.alert .condition-dot{background:var(--trap)}
.condition-line strong{color:var(--ink)}
.filter-bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:16px 0 18px}
.search-wrap{flex:1;min-width:260px;position:relative}
.search-wrap input{width:100%;background:var(--surface-strong);border:1px solid var(--line);color:var(--ink);padding:13px 15px;border-radius:8px;font:inherit}
.filter-btn{border:1px solid var(--line);background:var(--surface);color:var(--ink);padding:10px 12px;border-radius:8px;font-weight:800;cursor:pointer}
.filter-btn.active{border-color:var(--blue);background:var(--soft-blue);color:var(--blue)}
.filter-btn:hover{border-color:var(--blue)}
.table-wrap{overflow:auto;border:1px solid var(--line);background:var(--surface-strong)}
.matrix{width:100%;border-collapse:separate;border-spacing:0;min-width:1080px}
th,td{border-bottom:1px solid var(--line);padding:14px 14px;text-align:left;vertical-align:top}
th{background:var(--ink);color:var(--paper);font-size:.76rem;letter-spacing:.08em;text-transform:uppercase;position:sticky;top:0;z-index:1}
tr:last-child td{border-bottom:0}
tbody tr:hover td{background:color-mix(in srgb,var(--blue) 3%,var(--surface-strong))}
.service-name{font-weight:900}
.service-name small{display:block;color:var(--muted);font-size:.75rem;font-weight:700;margin-top:3px}
.badge{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:var(--surface);padding:4px 8px;border-radius:7px;font-size:.78rem;font-weight:800;white-space:nowrap}
.badge.ok{color:var(--ok);background:var(--soft-ok);border-color:color-mix(in srgb,var(--ok) 30%,var(--line))}
.badge.trap{color:var(--trap);background:var(--soft-trap);border-color:color-mix(in srgb,var(--trap) 30%,var(--line))}
.badge.blue{color:var(--blue);background:var(--soft-blue);border-color:color-mix(in srgb,var(--blue) 28%,var(--line))}
.source-link{font-weight:800;white-space:nowrap}
.mono{font-family:"JetBrains Mono","IBM Plex Mono","Cascadia Mono",monospace}
.mobile-results{display:none}
.card{border:1px solid var(--line);background:var(--surface-strong);padding:22px;margin:18px 0;box-shadow:var(--shadow)}
.card h2{margin-top:0}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:9px;margin:15px 0}
.fact{border:1px solid var(--line);background:var(--surface);padding:10px 12px}
.fact strong{display:block;font-size:.78rem;text-transform:uppercase;letter-spacing:.05em}
footer{border-top:1px solid var(--line);padding:28px 0 55px;color:var(--muted);font-size:.9rem}
code{font-family:"JetBrains Mono","IBM Plex Mono","Cascadia Mono",monospace;background:var(--soft-blue);padding:2px 5px}
.category-header{padding-bottom:26px;border-bottom:1px solid var(--line)}
.category-header h1{margin-bottom:.12em}
.category-header .lead{max-width:800px}
.trap-note{border-inline-start:4px solid var(--trap);padding:10px 13px;background:var(--soft-trap);margin:16px 0}
@media (max-width:900px){
  .hero-grid{grid-template-columns:1fr;gap:22px}
  .architecture-results{grid-template-columns:1fr}
  .hero{padding:46px 0 34px}
}
@media (max-width:800px){
  .container{width:min(100% - 22px,1180px)}
  .hero h1{font-size:clamp(2.35rem,12vw,4rem)}
  .section-head{display:block}
  .table-wrap{display:none}
  .mobile-results{display:grid;gap:12px}
  .mobile-card{background:var(--surface-strong);border:1px solid var(--line);padding:17px;position:relative}
  .mobile-card::before{content:"";position:absolute;inset-block:0;inset-inline-start:0;width:4px;background:var(--ok)}
  .mobile-card.has-trap::before{background:var(--trap)}
  .mobile-head{display:flex;justify-content:space-between;gap:12px;align-items:start}
  .mobile-name{font-weight:900;line-height:1.25}
  .mobile-category{font-size:.75rem;color:var(--muted);margin-top:3px}
  .mobile-limit{font:800 .96rem/1.5 "JetBrains Mono","IBM Plex Mono","Cascadia Mono",monospace;margin:13px 0}
  .mobile-conditions{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:12px}
  .mobile-condition{font-size:.78rem;border:1px solid var(--line);padding:7px 8px;background:var(--surface)}
  .mobile-condition.alert{border-color:color-mix(in srgb,var(--trap) 35%,var(--line));background:var(--soft-trap)}
  .mobile-source{font-size:.8rem;font-weight:800}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""

APP = r"""document.addEventListener('DOMContentLoaded', () => {
  const body = document.querySelector('#servicesBody');
  const mobileBody = document.querySelector('#mobileServicesBody');
  const search = document.querySelector('#searchInput');
  const status = document.querySelector('#resultStatus');
  const themeToggle = document.querySelector('#themeToggle');
  const architectureSelect = document.querySelector('#architectureSelect');
  const recommendationArea = document.querySelector('#recommendationArea');
  const filterButtons = [...document.querySelectorAll('[data-filter]')];

  const iconMoon = '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M20.5 14.5A8.5 8.5 0 0 1 9.5 3.5 8.5 8.5 0 1 0 20.5 14.5Z"/></svg>';
  const iconSun = '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="3.5"/><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.65 17.65l1.42 1.42M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.65 6.35l1.42-1.42"/></svg>';
  const setTheme = (theme) => {
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem('fwg-theme', theme); } catch (_) {}
    if (themeToggle) themeToggle.innerHTML = `${theme === 'dark' ? iconSun : iconMoon}<span>${theme === 'dark' ? 'Light mode' : 'Dark mode'}</span>`;
  };
  let savedTheme = null;
  try { savedTheme = localStorage.getItem('fwg-theme'); } catch (_) {}
  setTheme(savedTheme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
  if (themeToggle) themeToggle.addEventListener('click', () => setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'));

  const policyClass = (value) => value === 'Allowed' ? 'ok' : value === 'Restricted' ? 'trap' : 'trap';
  const cardLabel = (value) => value === 'Required' ? 'Required' : value === 'Conditional' ? 'Conditional' : 'No';
  const cardAlert = (value) => value === 'Required' || value === 'Conditional';
  const sleepText = (service) => service.sleeps ? 'Yes' : 'No';
  const productionText = (service) => service.production_ready ? 'Yes' : 'No';
  const hasTrap = (service) => cardAlert(service.card_requirement) || service.commercial_policy !== 'Allowed' || service.sleeps || !service.production_ready || (service.reclaim_policy && service.reclaim_policy.toLowerCase() !== 'none' && service.reclaim_policy.toLowerCase() !== 'none stated.');

  const conditionMarkup = (service) => {
    const rows = [
      ['Card', cardLabel(service.card_requirement), cardAlert(service.card_requirement)],
      ['Commercial', service.commercial_policy, service.commercial_policy !== 'Allowed'],
      ['Sleeps', sleepText(service), service.sleeps],
      ['Production', productionText(service), !service.production_ready]
    ];
    return rows.map(([label, value, alert]) => `<div class="condition-line${alert ? ' alert' : ''}"><span class="condition-dot"></span><span>${label}: <strong>${value}</strong></span></div>`).join('');
  };

  const conditionBadges = (service) => {
    const items = [
      ['Card', cardLabel(service.card_requirement), cardAlert(service.card_requirement)],
      ['Commercial', service.commercial_policy, service.commercial_policy !== 'Allowed'],
      ['Sleeps', sleepText(service), service.sleeps],
      ['Production', productionText(service), !service.production_ready]
    ];
    return items.map(([label, value, alert]) => `<div class="mobile-condition${alert ? ' alert' : ''}">${label}: <strong>${value}</strong></div>`).join('');
  };

  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

  const recommendationMap = {
    wordpress: ['infinityfree','byet-host','heliohost'],
    api: ['cloudflare-workers','gcp-cloud-run','deno-deploy'],
    nextjs: ['vercel-hobby','netlify','cloudflare-pages'],
    database: ['neon','supabase','turso'],
    ai: ['hugging-face-spaces','streamlit-community-cloud','google-colab'],
    docker: ['gcp-cloud-run','koyeb','render'],
    static: ['cloudflare-pages','github-pages','firebase-hosting'],
    storage: ['cloudflare-r2','backblaze-b2'],
    vps: ['oracle-cloud','google-cloud'],
    docs: ['github-pages','read-the-docs','gitlab-pages'],
    nocode: ['bubble']
  };

  const renderRecommendations = (services) => {
    if (!recommendationArea || !architectureSelect) return;
    const ids = recommendationMap[architectureSelect.value] || [];
    const selected = ids.map(id => services.find(s => s.id === id)).filter(Boolean);
    recommendationArea.replaceChildren();
    for (const service of selected.slice(0, 3)) {
      const card = document.createElement('article');
      card.className = `condition-card${hasTrap(service) ? ' has-trap' : ''}`;
      card.innerHTML = `
        <div class="condition-top"><h3>${esc(service.name)}</h3><span class="micro">${esc(service.last_verified)}</span></div>
        <div class="limit">${esc(service.hard_limit)}</div>
        <div class="conditions">${conditionMarkup(service)}</div>
        <a class="source-link" href="${esc(service.official_source)}" target="_blank" rel="noopener">Official source ↗</a>`;
      recommendationArea.appendChild(card);
    }
  };

  const load = async () => {
    try {
      const response = await fetch('services.json', {cache:'no-store'});
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      const services = Array.isArray(data.services) ? data.services : [];
      if (architectureSelect) architectureSelect.addEventListener('change', () => renderRecommendations(services));
      renderRecommendations(services);

      const render = () => {
        const q = (search?.value || '').trim().toLowerCase();
        const activeFilters = new Set(filterButtons.filter(b => b.classList.contains('active')).map(b => b.dataset.filter));
        const matches = services.filter(service => {
          const haystack = [service.name,service.category,service.free_class,service.card_requirement,service.commercial_policy,service.commercial_note,service.hard_limit,service.best_for,service.brilliant_feature].join(' ').toLowerCase();
          if (q && !haystack.includes(q)) return false;
          if (activeFilters.has('no-card') && service.card_requirement !== 'Not required') return false;
          if (activeFilters.has('no-sleep') && service.sleeps) return false;
          if (activeFilters.has('commercial') && service.commercial_policy !== 'Allowed') return false;
          return true;
        });
        if (body) {
          body.replaceChildren();
          for (const service of matches) {
            const row = document.createElement('tr');
            const policy = `<span class="badge ${policyClass(service.commercial_policy)}">${esc(service.commercial_policy)}</span>`;
            const conditions = `<div class="conditions">${conditionMarkup(service)}</div>`;
            row.innerHTML = `
              <td><div class="service-name">${esc(service.name)}<small>${esc(service.category)}</small></div></td>
              <td><span class="badge blue">${esc(service.free_class)}</span></td>
              <td>${policy}</td>
              <td><span class="badge ${cardAlert(service.card_requirement) ? 'trap' : 'ok'}">${esc(cardLabel(service.card_requirement))}</span></td>
              <td>${conditions}</td>
              <td class="limit">${esc(service.hard_limit)}</td>
              <td><span class="micro">${esc(service.last_verified)}</span></td>
              <td><a class="source-link" href="${esc(service.official_source)}" target="_blank" rel="noopener">Official ↗</a></td>`;
            body.appendChild(row);
          }
        }
        if (mobileBody) {
          mobileBody.replaceChildren();
          for (const service of matches) {
            const article = document.createElement('article');
            article.className = `mobile-card${hasTrap(service) ? ' has-trap' : ''}`;
            article.innerHTML = `
              <div class="mobile-head"><div><div class="mobile-name">${esc(service.name)}</div><div class="mobile-category">${esc(service.category)} · ${esc(service.free_class)}</div></div><span class="micro">${esc(service.last_verified)}</span></div>
              <div class="mobile-limit">${esc(service.hard_limit)}</div>
              <div class="mobile-conditions">${conditionBadges(service)}</div>
              <a class="mobile-source" href="${esc(service.official_source)}" target="_blank" rel="noopener">Official source ↗</a>`;
            mobileBody.appendChild(article);
          }
        }
        if (status) status.textContent = `${matches.length} of ${services.length} services shown`;
      };
      search?.addEventListener('input', render);
      filterButtons.forEach(button => button.addEventListener('click', () => { button.classList.toggle('active'); render(); }));
      render();
    } catch (error) {
      if (body) body.innerHTML = '<tr><td colspan="8">Unable to load services.json. Check the deployed data artifact.</td></tr>';
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


def write_index(data: dict) -> None:
    services = data["services"]
    nav = "".join(f'<a href="{esc(k)}.html">{esc(v)}</a>' for k, v in CATEGORIES.items())
    count = len(services)
    index = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Free Web Hosting &amp; Cloud 2026 | Verified Free-Tier Directory</title>
<meta name="description" content="Verified 2026 directory of free web hosting, serverless compute, managed databases, object storage, VPS and AI/data platforms. Limits and the catch are shown together.">
<link rel="canonical" href="https://hamidic911.github.io/free-web-hosting-guide/">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="hero"><div class="container hero-grid">
<div>
<div class="eyebrow">Primary-source directory · checked {esc(data['metadata']['last_updated'])}</div>
<h1>Every free host has a catch. We put it beside the quota.</h1>
<p class="lead">A practical, community-maintained directory of free hosting and cloud services. Compare the policy, card requirement, sleep behavior, production suitability and hard limit before you deploy.</p>
<button class="theme-toggle" id="themeToggle" type="button" aria-label="Toggle color theme"></button>
</div>
<section class="hero-tool" aria-labelledby="architectureHeading">
<div id="architectureHeading" class="hero-tool-label">I want to build a</div>
<div class="architecture-picker"><span>service for</span> <select id="architectureSelect" aria-label="Choose what you want to build"><option value="static">static site</option><option value="wordpress">WordPress / PHP site</option><option value="nextjs">Next.js app</option><option value="api">API</option><option value="docker">Docker app</option><option value="database">database</option><option value="storage">object storage</option><option value="vps">VPS / server</option><option value="ai">AI demo</option><option value="docs">documentation</option><option value="nocode">no-code app</option></select></div>
<p class="hero-note">Three starting points, with their conditions visible immediately.</p>
</section>
</div></header>
<nav class="nav-wrap"><div class="container nav" aria-label="Categories">{nav}</div></nav>
<main class="container">
<section>
<div class="section-head"><div><div class="section-kicker">Start here</div><h2>Choose by what you are building</h2></div><div class="meta-line">{count} verified services · {len(CATEGORIES)} categories</div></div>
<div id="recommendationArea" class="architecture-results" aria-live="polite"></div>
</section>
<section id="matrix">
<div class="section-head"><div><div class="section-kicker">Verified comparison</div><h2>The conditions table</h2><p class="meta-line">The headline number is never the whole story.</p></div></div>
<div class="filter-bar">
<div class="search-wrap"><input id="searchInput" type="search" placeholder="Search provider, category, database, limit…" autocomplete="off" aria-label="Search verified services"></div>
<button class="filter-btn" type="button" data-filter="no-card">No card</button>
<button class="filter-btn" type="button" data-filter="no-sleep">Doesn’t sleep</button>
<button class="filter-btn" type="button" data-filter="commercial">Commercial allowed</button>
</div>
<p id="resultStatus" class="meta-line" aria-live="polite">Loading services…</p>
<div class="table-wrap"><table class="matrix"><thead><tr><th>Service</th><th>Free model</th><th>Commercial</th><th>Card</th><th>Conditions</th><th>Hard limit / catch</th><th>Verified</th><th>Source</th></tr></thead><tbody id="servicesBody"></tbody></table></div>
<div id="mobileServicesBody" class="mobile-results"></div>
</section>
</main>
<footer><div class="container">Official provider sources · checked dates · community-maintained · canonical data in <code>services.yml</code> · MIT License</div></footer>
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
            alerts = []
            if s["card_requirement"] in {"Required", "Conditional"}: alerts.append(f"Card: {s['card_requirement']}")
            if s["commercial_policy"] != "Allowed": alerts.append(f"Commercial: {s['commercial_policy']}")
            if s["sleeps"]: alerts.append("Sleeps / pauses")
            if not s["production_ready"]: alerts.append("Not production-ready")
            alert_text = " · ".join(alerts) if alerts else "No major condition flag"
            cards.append(f'''<article class="card">
<div class="section-kicker">{esc(s['free_class'])} · verified {esc(s['last_verified'])}</div>
<h2>{esc(s['name'])}</h2>
<p>{esc(s['best_for'])}</p>
<p class="limit">{esc(s['hard_limit'])}</p>
<div class="facts">
<div class="fact"><strong>Card</strong><br>{esc(s['card_requirement'])}</div>
<div class="fact"><strong>Commercial</strong><br>{esc(s['commercial_policy'])}</div>
<div class="fact"><strong>Sleeps</strong><br>{'Yes' if s['sleeps'] else 'No'}</div>
<div class="fact"><strong>Production</strong><br>{'Yes' if s['production_ready'] else 'No'}</div>
<div class="fact"><strong>Custom domain</strong><br>{'Yes' if s['custom_domain'] else 'No'}</div>
</div>
<div class="trap-note"><strong>Conditions:</strong> {esc(alert_text)}<br><span class="muted">Reclaim: {esc(s['reclaim_policy'])}</span></div>
<p><strong>Feature:</strong> {esc(s['brilliant_feature'])}</p>
<p><a class="source-link" href="{esc(s['official_source'])}" target="_blank" rel="noopener">Official source ↗</a></p>
</article>''' )
        page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Free {esc(title)} 2026 | Verified Limits &amp; Conditions</title>
<meta name="description" content="Verified 2026 {esc(title.lower())} services with free-tier limits, card requirements, commercial policies, and sleep/reclaim conditions.">
<link rel="canonical" href="https://hamidic911.github.io/free-web-hosting-guide/{esc(category)}.html">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="hero"><div class="container category-header">
<div class="eyebrow">Category guide · checked {esc(data['metadata']['last_updated'])}</div>
<h1>Free {esc(title)} in 2026</h1>
<p class="lead">The important condition is shown beside the quota, not buried below it.</p>
<button class="theme-toggle" id="themeToggle" type="button" aria-label="Toggle color theme"></button>
</div></header>
<nav class="nav-wrap"><div class="container nav" aria-label="Categories">{nav}</div></nav>
<main class="container">{''.join(cards) if cards else '<div class="card"><p>No verified services in this category yet.</p></div>'}</main>
<footer><div class="container">Official provider sources · checked dates · <a href="index.html">Back to directory</a> · MIT License</div></footer>
<script src="app.js"></script>
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
    write_index(data)
    write_category_pages(data)
    write_sitemap(data)
    (SITE / "style.css").write_text(STYLE, encoding="utf-8")
    (SITE / "app.js").write_text(APP, encoding="utf-8")
    print(f"Generated repository artifacts for {len(data['services'])} services.")


if __name__ == "__main__":
    main()
