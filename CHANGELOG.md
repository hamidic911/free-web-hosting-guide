## [2.3.1] - 2026-10-08

### Visual Refresh
- Reworked the static site with a brighter indigo/cyan/teal visual system, layered backgrounds, polished cards, badges, sticky category navigation, and improved table styling.
- Added an accessible light/dark theme toggle across the site with local preference persistence.
- Improved mobile responsiveness and reduced-motion handling.
- Kept the site dependency-free by using system fonts and plain HTML/CSS/JavaScript.

## [2.3.0] - 2026-10-08

### Expanded
- Restored 14 current services from the earlier catalogue after fresh official-source verification: Deno Deploy, Firebase Hosting, Cloudflare D1, Google Compute Engine e2-micro, GitLab Pages, Byet.host, HelioHost, AlwaysData, Surge, Neocities, Appwrite Cloud, Kaggle Notebooks, Bubble, and Read the Docs.
- Expanded the canonical taxonomy with No-Code App Builders and Documentation Hosting.
- Regenerated README, JSON, category pages, sitemap, and robots.txt from `services.yml`.

### Guardrails
- Preserved the v2 schema and commercial/card enums.
- Kept self-hosted PaaS tools separate from hosting-provider records.
- Added cross-field assertions for the newly restored providers.

# Changelog

## 2.2.0 — 2026-10-08

### Changed
- Replaced `commercial_allowed` with `commercial_policy`.
- Replaced `card_required` with `card_requirement`.
- Restored a structured category taxonomy.
- Made `services.yml` the sole source of truth and generated `services.json` and `site/services.json`.
- Added a real schema validator and static-site generator.
- Corrected current 2026 provider limits and policy traps for Koyeb, Neon, Turso, GitHub Pages, InfinityFree, R2, Upstash, Netlify, Vercel, Backblaze B2, Oracle Cloud, Hugging Face Spaces, and Streamlit Community Cloud.
- Removed subjective star and tier rankings from the public guide.
