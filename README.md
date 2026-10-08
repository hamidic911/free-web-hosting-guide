# Awesome Free Web Hosting & Cloud 2026

A community-maintained directory of free-tier web hosting, serverless compute, managed databases, object storage, virtual machines, and AI/data application platforms.

This guide is intentionally factual: no star ratings, no S/A/B tiers, and no affiliate rankings. Each service exposes the pricing model, card requirement, commercial policy, sleep/reclaim behavior, production suitability, hard limit, and primary provider source.

**Last verified:** 2026-10-08  
**Canonical source:** `services.yml`  
**Generated outputs:** `services.json`, `site/services.json`, the site pages, sitemap, and this README.  

## Start Here: choose by architecture

| What are you building? | Starting point | Main catch |
|---|---|---|
| **Static site / docs** | **Cloudflare Pages or GitHub Pages** | GitHub Pages is restricted for online business, e-commerce, and commercial SaaS. |
| **Next.js / frontend** | **Netlify or Vercel Hobby** | Vercel Hobby is non-commercial; Netlify uses monthly credits. |
| **Docker app / API** | **Google Cloud Run, Koyeb, or Render** | Cloud Run needs billing; Koyeb requires a card; Render free instances are not for production. |
| **Edge API** | **Cloudflare Workers** | 100,000 requests/day and 10 ms CPU/request on the Free plan. |
| **PostgreSQL** | **Neon or Supabase** | Neon has per-project quotas; Supabase may pause low-activity free projects. |
| **SQLite at the edge** | **Turso** | 5 GB total storage plus row-operation quotas. |
| **Object storage** | **Cloudflare R2 or Backblaze B2** | Finite free storage allowances; R2 requires billing setup. |
| **Free VPS** | **Oracle Cloud Always Free** | Billing verification and an idle-resource policy apply. |
| **AI/data demo** | **Hugging Face Spaces or Streamlit Community Cloud** | Free compute and commercial/data-use rules are more restrictive than ordinary hosting. |

## How to read the guide

The labels below describe the **pricing model**, not quality. Commercial policy, card requirement, sleep/pause, reclaim, custom domain, and production suitability are separate fields.

| Label | Meaning |
|---|---|
| **Always Free** | A permanent no-cost allowance subject to published limits; billing setup may still be required. |
| **Free Plan** | A permanent $0 plan with defined resource and feature limits. |
| **Free Development** | Free mainly for staging/development; production requires payment. |
| **Free Credits** | A spend-down or time-limited monetary credit balance. |
| **Trial** | Time-limited access that eventually ends or requires a paid plan. |

## Commercial policy

- **Allowed:** the provider's current terms permit commercial use of the relevant service/free allowance, subject to its limits.
- **Restricted:** commercial use is limited by service scope or provider terms; the service needs closer inspection before deployment.
- **No:** the relevant free plan is explicitly non-commercial.

## Comparison matrix

| Service | Category | Free model | Card | Commercial | Sleeps | Production | Hard limit / catch |
|---|---|---|---|---|---|---|---|
| **Cloudflare Pages** | Static Hosting | Always Free | Not required | **Allowed** | No | Yes | 500 builds/month; 20,000 files/site; 25 MiB maximum single asset; Pages Functions use Workers quotas. |
| **GitHub Pages** | Static Hosting | Always Free | Not required | **Restricted** | No | Yes | Published site <= 1 GB; 100 GB/month soft bandwidth limit; 10 builds/hour soft limit for built-in Pages publishing; custom GitHub Actions deployments use Actions limits instead. |
| **Vercel (Hobby Plan)** | Frontend Platforms | Free Plan | Not required | **No** | No | No | 200 projects; 100 deployments/day; 100 builds/hour; 45-minute build time/deployment; 100 MB static file upload; 1 concurrent deployment. |
| **Netlify** | Frontend Platforms | Free Plan | Not required | **Allowed** | Yes | Yes | 300 credits/month; production deploy 15 credits; bandwidth 20 credits/GB; web requests 2 credits/10K requests; compute 10 credits/GB-hour. |
| **Cloudflare Workers** | Serverless & Edge Compute | Always Free | Not required | **Allowed** | No | Yes | 100,000 requests/day on the Workers Free plan; 10 ms CPU time/request. |
| **AWS Lambda** | Serverless & Edge Compute | Always Free | Required | **Allowed** | No | Yes | 1 million requests/month and 400,000 GB-seconds/month free for Lambda functions. |
| **Google Cloud Run** | Containers & Full-Stack Cloud | Always Free | Required | **Allowed** | Yes | Yes | 2 million requests/month; 360,000 GiB-seconds memory; 180,000 vCPU-seconds; 1 GB North America outbound transfer/month under the listed free tier. |
| **Render** | Containers & Full-Stack Cloud | Free Plan | Not required | **Allowed** | Yes | No | 750 free instance hours/workspace/month; web services sleep after 15m idle; free Postgres is 1 GB and expires after 30 days. |
| **Koyeb** | Containers & Full-Stack Cloud | Free Plan | Required | **Allowed** | Yes | No | 1 free Service/org in Frankfurt or Washington, D.C.; 512 MB RAM; 0.1 vCPU; 2 GB SSD; no volumes; scale-to-zero after 1 hour. |
| **Supabase** | Managed Databases & BaaS | Free Plan | Not required | **Allowed** | Yes | Yes | 500 MB database size; 1 GB file storage; 5 GB egress; 2 active projects; 50,000 MAU. |
| **Neon** | Managed Databases & BaaS | Free Plan | Not required | **Allowed** | Yes | Yes | 1 GB Postgres storage/project; 100 projects; 100 CU-hours/project/month; 10 branches/project; up to 2 CU autoscaling; 5 GB public network transfer/project/month. |
| **Turso** | Managed Databases & BaaS | Free Plan | Not required | **Allowed** | No | Yes | 100 databases; 5 GB total storage; 500M rows read (scanned)/month; 10M rows written/month; 3 GB syncs/month; 1-day PITR. |
| **MongoDB Atlas (M0)** | Managed Databases & BaaS | Free Plan | Not required | **Allowed** | Yes | No | 0.5 GB storage including indexes; shared RAM/vCPU; one Free cluster per project; free clusters are for small-scale development and are automatically paused after 30 days inactivity. |
| **Upstash Redis** | Managed Databases & BaaS | Free Plan | Not required | **Allowed** | No | No | 1 free database; 256 MB data; 10 GB monthly bandwidth; 500,000 commands/month. |
| **Cloudflare R2** | Object Storage | Always Free | Required | **Allowed** | No | Yes | 10 GB-month storage/month; 1M Class A ops/month; 10M Class B ops/month; Internet egress is free. |
| **Backblaze B2** | Object Storage | Always Free | Not required | **Allowed** | No | Yes | First 10 GB storage is always free; free egress up to 3× average monthly stored data; egress above that may be free via supported CDN/compute partners. |
| **Oracle Cloud Always Free** | Free VPS & Compute | Always Free | Required | **Allowed** | No | Yes | Up to 2 OCPUs and 12 GB RAM on Ampere A1 Always Free allocation; 200 GB total Always Free block volume. |
| **Hugging Face Spaces** | AI, GPU & Data Apps | Free Plan | Not required | **Restricted** | Yes | No | Static Spaces are free; Gradio/Docker Spaces run on compute and require a paid plan for new deployments; free ZeroGPU access is limited and dynamic. |
| **Streamlit Community Cloud** | AI, GPU & Data Apps | Free Plan | Not required | **No** | Yes | No | Public apps plus 1 private app; 1 GB RAM/app; current Community Cloud terms restrict certain personal-information use to personal/non-commercial purposes. |
| **Google Colab** | AI, GPU & Data Apps | Free Plan | Not required | **Restricted** | Yes | No | Ephemeral notebook sessions; GPU/TPU availability is dynamic and not guaranteed. |
| **Serv00** | PHP & Traditional Hosting | Free Plan | Not required | **Allowed** | No | No | 3 GB disk; 512 MB RAM quota; shared CPU limits; periodic account activity required. |
| **InfinityFree** | PHP & Traditional Hosting | Free Plan | Not required | **Allowed** | No | No | 5 GB storage; 50,000 daily hits; 30,000 inodes; shared CPU/resource limits; no built-in free email service. |

## Service details

### Static Hosting

#### Cloudflare Pages
- **Best for:** Static sites, documentation, portfolios, and Jamstack frontends.
- **Free model:** Always Free
- **Card requirement:** Not required
- **Commercial policy:** **Allowed** — Commercial use is subject to Cloudflare terms and plan-specific limits.
- **Sleep / pause:** No
- **Reclaim policy:** None stated for the free Pages allowance.
- **Custom domain:** Yes
- **Production-ready for the free use case:** Yes
- **Hard limit / catch:** 500 builds/month; 20,000 files/site; 25 MiB maximum single asset; Pages Functions use Workers quotas.
- **Brilliant feature:** Static asset requests are free and unlimited; Functions can extend the site with edge logic.
- **Official source:** [developers.cloudflare.com](https://developers.cloudflare.com/pages/platform/limits/)
- **Last verified:** 2026-10-08

#### GitHub Pages
- **Best for:** Open-source project documentation, portfolios, blogs, and static informational sites.
- **Free model:** Always Free
- **Card requirement:** Not required
- **Commercial policy:** **Restricted** — Not intended or allowed as free web hosting for online business, e-commerce, or commercial SaaS.
- **Sleep / pause:** No
- **Reclaim policy:** None stated.
- **Custom domain:** Yes
- **Production-ready for the free use case:** Yes
- **Hard limit / catch:** Published site <= 1 GB; 100 GB/month soft bandwidth limit; 10 builds/hour soft limit for built-in Pages publishing; custom GitHub Actions deployments use Actions limits instead.
- **Brilliant feature:** Versioned static publishing directly from Git repositories.
- **Official source:** [docs.github.com](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- **Last verified:** 2026-10-08

### Frontend Platforms

#### Vercel (Hobby Plan)
- **Best for:** Personal, non-commercial Next.js and frontend previews.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **No** — Hobby is for personal, non-commercial use under the current Terms.
- **Sleep / pause:** No
- **Reclaim policy:** Projects may be disabled or removed under current platform terms.
- **Custom domain:** Yes
- **Production-ready for the free use case:** No
- **Hard limit / catch:** 200 projects; 100 deployments/day; 100 builds/hour; 45-minute build time/deployment; 100 MB static file upload; 1 concurrent deployment.
- **Brilliant feature:** Deep integration with Next.js and Git-based preview deployments.
- **Official source:** [vercel.com](https://vercel.com/docs/limits/usage/plan-resource-limits)
- **Last verified:** 2026-10-08

#### Netlify
- **Best for:** Frontend sites, Jamstack builds, forms, redirects, and lightweight serverless features.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Allowed** — Commercial use is subject to Netlify terms and the current credit-based Free plan.
- **Sleep / pause:** Yes
- **Reclaim policy:** Sites pause when the monthly included credit allowance is exhausted.
- **Custom domain:** Yes
- **Production-ready for the free use case:** Yes
- **Hard limit / catch:** 300 credits/month; production deploy 15 credits; bandwidth 20 credits/GB; web requests 2 credits/10K requests; compute 10 credits/GB-hour.
- **Brilliant feature:** Credit-based platform with integrated deploy previews, forms, and frontend workflow.
- **Official source:** [www.netlify.com](https://www.netlify.com/pricing/)
- **Last verified:** 2026-10-08

### Serverless & Edge Compute

#### Cloudflare Workers
- **Best for:** Edge APIs, request routing, webhooks, and lightweight backend logic.
- **Free model:** Always Free
- **Card requirement:** Not required
- **Commercial policy:** **Allowed** — Subject to Cloudflare terms and the free usage allowance.
- **Sleep / pause:** No
- **Reclaim policy:** None stated.
- **Custom domain:** Yes
- **Production-ready for the free use case:** Yes
- **Hard limit / catch:** 100,000 requests/day on the Workers Free plan; 10 ms CPU time/request.
- **Brilliant feature:** Runs server-side logic close to users on Cloudflare’s global network.
- **Official source:** [developers.cloudflare.com](https://developers.cloudflare.com/workers/platform/limits/)
- **Last verified:** 2026-10-08

#### AWS Lambda
- **Best for:** Event-driven APIs, jobs, automation, and AWS integrations.
- **Free model:** Always Free
- **Card requirement:** Required
- **Commercial policy:** **Allowed** — Commercial use is permitted subject to AWS terms and any applicable charges beyond the free allowance.
- **Sleep / pause:** No
- **Reclaim policy:** None stated; event-driven execution is on demand.
- **Custom domain:** Yes
- **Production-ready for the free use case:** Yes
- **Hard limit / catch:** 1 million requests/month and 400,000 GB-seconds/month free for Lambda functions.
- **Brilliant feature:** Mature event-driven compute integrated across AWS services.
- **Official source:** [aws.amazon.com](https://aws.amazon.com/lambda/pricing/)
- **Last verified:** 2026-10-08

### Containers & Full-Stack Cloud

#### Google Cloud Run
- **Best for:** Stateless containerized APIs and web apps.
- **Free model:** Always Free
- **Card requirement:** Required
- **Commercial policy:** **Allowed** — Commercial workloads are permitted under Google Cloud terms; a billing account is required.
- **Sleep / pause:** Yes
- **Reclaim policy:** Scales instances to zero when idle.
- **Custom domain:** Yes
- **Production-ready for the free use case:** Yes
- **Hard limit / catch:** 2 million requests/month; 360,000 GiB-seconds memory; 180,000 vCPU-seconds; 1 GB North America outbound transfer/month under the listed free tier.
- **Brilliant feature:** Runs arbitrary containers while handling deployment and autoscaling.
- **Official source:** [docs.cloud.google.com](https://docs.cloud.google.com/free/docs/free-cloud-features)
- **Last verified:** 2026-10-08

#### Render
- **Best for:** Prototypes, hobby projects, and testing Node.js, Python, Docker, and other web services.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Allowed** — Commercial use is not prohibited by the free-instance documentation, but free instances are explicitly not for production applications.
- **Sleep / pause:** Yes
- **Reclaim policy:** Free web services spin down after 15 minutes without inbound traffic; free Postgres expires after 30 days.
- **Custom domain:** Yes
- **Production-ready for the free use case:** No
- **Hard limit / catch:** 750 free instance hours/workspace/month; web services sleep after 15m idle; free Postgres is 1 GB and expires after 30 days.
- **Brilliant feature:** Simple Git-to-deploy workflow for apps and containers.
- **Official source:** [render.com](https://render.com/docs/free)
- **Last verified:** 2026-10-08

#### Koyeb
- **Best for:** Hobby microservices and testing in Frankfurt or Washington, D.C.
- **Free model:** Free Plan
- **Card requirement:** Required
- **Commercial policy:** **Allowed** — Free usage is available subject to Koyeb terms; a credit card is required for account validation.
- **Sleep / pause:** Yes
- **Reclaim policy:** Scales the free service to zero after 1 hour without traffic.
- **Custom domain:** Yes
- **Production-ready for the free use case:** No
- **Hard limit / catch:** 1 free Service/org in Frankfurt or Washington, D.C.; 512 MB RAM; 0.1 vCPU; 2 GB SSD; no volumes; scale-to-zero after 1 hour.
- **Brilliant feature:** A real container service with Git-driven deployment and a persistent free allowance.
- **Official source:** [www.koyeb.com](https://www.koyeb.com/docs/faqs/pricing)
- **Last verified:** 2026-10-08

### Managed Databases & BaaS

#### Supabase
- **Best for:** PostgreSQL, authentication, storage, realtime features, and APIs.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Allowed** — Commercial use is subject to Supabase terms and free-plan limits.
- **Sleep / pause:** Yes
- **Reclaim policy:** Free projects may be paused after low activity over a 7-day period.
- **Custom domain:** No
- **Production-ready for the free use case:** Yes
- **Hard limit / catch:** 500 MB database size; 1 GB file storage; 5 GB egress; 2 active projects; 50,000 MAU.
- **Brilliant feature:** Managed Postgres with Auth, Storage, Realtime, and API layers in one platform.
- **Official source:** [supabase.com](https://supabase.com/pricing)
- **Last verified:** 2026-10-08

#### Neon
- **Best for:** Serverless PostgreSQL and branch-based development workflows.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Allowed** — Commercial use is subject to Neon terms and plan limits.
- **Sleep / pause:** Yes
- **Reclaim policy:** Compute scales to zero after inactivity; current free-plan compute allowance is usage based.
- **Custom domain:** No
- **Production-ready for the free use case:** Yes
- **Hard limit / catch:** 1 GB Postgres storage/project; 100 projects; 100 CU-hours/project/month; 10 branches/project; up to 2 CU autoscaling; 5 GB public network transfer/project/month.
- **Brilliant feature:** Branchable Postgres infrastructure designed for isolated environments.
- **Official source:** [neon.com](https://neon.com/blog/neon-free-plan-1-gb-per-project)
- **Last verified:** 2026-10-08

#### Turso
- **Best for:** Edge-replicated SQLite/libSQL applications and lightweight SQL workloads.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Allowed** — Commercial use is subject to Turso terms and free-plan limits.
- **Sleep / pause:** No
- **Reclaim policy:** None stated.
- **Custom domain:** No
- **Production-ready for the free use case:** Yes
- **Hard limit / catch:** 100 databases; 5 GB total storage; 500M rows read (scanned)/month; 10M rows written/month; 3 GB syncs/month; 1-day PITR.
- **Brilliant feature:** SQLite-compatible database designed for globally distributed applications.
- **Official source:** [turso.tech](https://turso.tech/pricing)
- **Last verified:** 2026-10-08

#### MongoDB Atlas (M0)
- **Best for:** Managed MongoDB document databases and flexible JSON-style schemas.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Allowed** — Commercial use is subject to MongoDB terms.
- **Sleep / pause:** Yes
- **Reclaim policy:** Free clusters are automatically paused after 30 days of inactivity and can be resumed; one Free cluster per project.
- **Custom domain:** No
- **Production-ready for the free use case:** No
- **Hard limit / catch:** 0.5 GB storage including indexes; shared RAM/vCPU; one Free cluster per project; free clusters are for small-scale development and are automatically paused after 30 days inactivity.
- **Brilliant feature:** Managed MongoDB without operating the database server yourself.
- **Official source:** [www.mongodb.com](https://www.mongodb.com/pricing)
- **Last verified:** 2026-10-08

#### Upstash Redis
- **Best for:** Serverless caching, rate limiting, sessions, and small key-value workloads.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Allowed** — Commercial use is subject to Upstash terms and free-plan limits.
- **Sleep / pause:** No
- **Reclaim policy:** None for claimed free databases.
- **Custom domain:** No
- **Production-ready for the free use case:** No
- **Hard limit / catch:** 1 free database; 256 MB data; 10 GB monthly bandwidth; 500,000 commands/month.
- **Brilliant feature:** REST-compatible Redis designed for serverless and edge applications.
- **Official source:** [upstash.com](https://upstash.com/pricing/redis)
- **Last verified:** 2026-10-08

### Object Storage

#### Cloudflare R2
- **Best for:** S3-compatible object storage where outbound Internet egress cost matters.
- **Free model:** Always Free
- **Card requirement:** Required
- **Commercial policy:** **Allowed** — Commercial use is subject to Cloudflare terms; R2 requires billing/payment setup.
- **Sleep / pause:** No
- **Reclaim policy:** None stated.
- **Custom domain:** Yes
- **Production-ready for the free use case:** Yes
- **Hard limit / catch:** 10 GB-month storage/month; 1M Class A ops/month; 10M Class B ops/month; Internet egress is free.
- **Brilliant feature:** No Internet egress bandwidth charge on stored objects.
- **Official source:** [developers.cloudflare.com](https://developers.cloudflare.com/r2/pricing/)
- **Last verified:** 2026-10-08

#### Backblaze B2
- **Best for:** Object storage, backups, media, and application assets.
- **Free model:** Always Free
- **Card requirement:** Not required
- **Commercial policy:** **Allowed** — Commercial use is subject to Backblaze terms.
- **Sleep / pause:** No
- **Reclaim policy:** None stated.
- **Custom domain:** Yes
- **Production-ready for the free use case:** Yes
- **Hard limit / catch:** First 10 GB storage is always free; free egress up to 3× average monthly stored data; egress above that may be free via supported CDN/compute partners.
- **Brilliant feature:** Simple object storage with generous built-in free egress allowances.
- **Official source:** [www.backblaze.com](https://www.backblaze.com/cloud-storage/pricing)
- **Last verified:** 2026-10-08

### Free VPS & Compute

#### Oracle Cloud Always Free
- **Best for:** Self-hosted Linux servers, Docker, utilities, and persistent services.
- **Free model:** Always Free
- **Card requirement:** Required
- **Commercial policy:** **Allowed** — Commercial use is subject to Oracle Cloud terms and tenancy policies.
- **Sleep / pause:** No
- **Reclaim policy:** Oracle may reclaim idle Always Free compute instances under its current idle-resource policy.
- **Custom domain:** Yes
- **Production-ready for the free use case:** Yes
- **Hard limit / catch:** Up to 2 OCPUs and 12 GB RAM on Ampere A1 Always Free allocation; 200 GB total Always Free block volume.
- **Brilliant feature:** A relatively large persistent VM allocation for a permanently free tier.
- **Official source:** [www.oracle.com](https://www.oracle.com/cloud/free/)
- **Last verified:** 2026-10-08

### AI, GPU & Data Apps

#### Hugging Face Spaces
- **Best for:** AI demos and static model showcases hosted as Spaces.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Restricted** — Static Spaces are free for everyone; new Gradio and Docker compute Spaces require a paid plan. Review the current service terms before commercial deployment.
- **Sleep / pause:** Yes
- **Reclaim policy:** Free compute availability depends on hardware/plan; static Spaces remain free.
- **Custom domain:** No
- **Production-ready for the free use case:** No
- **Hard limit / catch:** Static Spaces are free; Gradio/Docker Spaces run on compute and require a paid plan for new deployments; free ZeroGPU access is limited and dynamic.
- **Brilliant feature:** Tight integration with the open ML model ecosystem and Spaces UI.
- **Official source:** [huggingface.co](https://huggingface.co/docs/hub/spaces-overview)
- **Last verified:** 2026-10-08

#### Streamlit Community Cloud
- **Best for:** Public data apps and Python dashboards connected to GitHub.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **No** — Community Cloud content that processes personal information is limited to personal and non-commercial use; the service is intended for evaluation, educational, and household use in those cases.
- **Sleep / pause:** Yes
- **Reclaim policy:** Apps can sleep when inactive and can be restarted from their public URL.
- **Custom domain:** No
- **Production-ready for the free use case:** No
- **Hard limit / catch:** Public apps plus 1 private app; 1 GB RAM/app; current Community Cloud terms restrict certain personal-information use to personal/non-commercial purposes.
- **Brilliant feature:** Turns Python data applications into shareable web UIs with almost no infrastructure work.
- **Official source:** [docs.streamlit.io](https://docs.streamlit.io/deploy/streamlit-community-cloud)
- **Last verified:** 2026-10-08

#### Google Colab
- **Best for:** Interactive Python notebooks, experiments, and ML research.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Restricted** — Not a general web-hosting service; free compute is ephemeral and governed by Google Colab terms and availability.
- **Sleep / pause:** Yes
- **Reclaim policy:** Sessions are ephemeral and may terminate because of idle/runtime limits or resource availability.
- **Custom domain:** No
- **Production-ready for the free use case:** No
- **Hard limit / catch:** Ephemeral notebook sessions; GPU/TPU availability is dynamic and not guaranteed.
- **Brilliant feature:** Browser-based Jupyter environment with optional accelerator access.
- **Official source:** [colab.research.google.com](https://colab.research.google.com/)
- **Last verified:** 2026-10-08

### PHP & Traditional Hosting

#### Serv00
- **Best for:** PHP sites, FreeBSD/SSH learning, cron jobs, and small personal projects.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Allowed** — Commercial websites are not generally prohibited; account resale/rental and prohibited resource-intensive or unlawful uses are disallowed.
- **Sleep / pause:** No
- **Reclaim policy:** Free accounts require periodic control-panel login; inactivity can lead to account removal.
- **Custom domain:** Yes
- **Production-ready for the free use case:** No
- **Hard limit / catch:** 3 GB disk; 512 MB RAM quota; shared CPU limits; periodic account activity required.
- **Brilliant feature:** Traditional hosting with SSH access, cron, and developer-oriented tooling.
- **Official source:** [www.serv00.com](https://www.serv00.com/)
- **Last verified:** 2026-10-08

#### InfinityFree
- **Best for:** Learning PHP, WordPress testing, and non-critical websites.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Allowed** — Commercial websites and payment processing are allowed; reselling InfinityFree hosting requires permission. WooCommerce is technically allowed but the free shared environment is not recommended for serious production stores.
- **Sleep / pause:** No
- **Reclaim policy:** Accounts can be suspended for exceeding resource limits or violating terms.
- **Custom domain:** Yes
- **Production-ready for the free use case:** No
- **Hard limit / catch:** 5 GB storage; 50,000 daily hits; 30,000 inodes; shared CPU/resource limits; no built-in free email service.
- **Brilliant feature:** Free PHP hosting with control-panel tooling and one-click app installation.
- **Official source:** [www.infinityfree.com](https://www.infinityfree.com/terms/)
- **Last verified:** 2026-10-08

## Self-hosted PaaS control planes

> These are software you install on a server you already control. They are not hosting providers themselves.

- **Coolify** — self-hosted Docker-oriented PaaS/control plane.
- **Dokploy** — lightweight self-hosted deployment platform.
- **CapRover** — self-hosted PaaS with a simple app deployment model.
- **Dokku** — lightweight Heroku-style self-hosted platform.

## Free-Tier Graveyard

| Service | Status |
|---|---|
| **000WebHost** | Shut down; not a current free-hosting option. |
| **Heroku Free Dynos** | Permanent free dyno tier removed. |
| **PlanetScale Hobby Free** | Permanent free tier removed. |
| **Railway Free** | Credit/trial-based for new accounts rather than a permanent free plan. |
| **Fly.io Free** | Legacy allowances are not a current general free plan for new organizations. |
| **Glitch hosting** | No longer a current general hosting recommendation. |

## Before you deploy

Check what happens at the quota, whether a payment method is required, whether the service sleeps or pauses, whether inactive resources are deleted or reclaimed, whether the free plan permits your commercial use, whether storage is persistent, and whether the region/custom-domain/email/backups you need are included.

## Maintenance

`services.yml` is the single source of truth. Run `python scripts/build_site.py` after changing provider data. Then run `python scripts/validate_repo.py`. CI performs the same build-and-validate sequence before deployment.

No affiliate links. No star ratings. No S/A/B rankings. No unqualified "unlimited", "best", or "free forever" claims.
