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
| **GPU notebook** | **Kaggle Notebooks or Google Colab** | Free accelerator availability is temporary and quota-limited. |
| **No-code app** | **Bubble** | Free is a development environment; production requires payment. |
| **Open-source documentation** | **Read the Docs Community or GitLab Pages** | Read the Docs Community is for open-source docs; GitLab CI minutes are limited on Free. |

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
| **Firebase Hosting** | Static Hosting | Free Plan | Not required | **Allowed** | No | Yes | 10 GB Hosting storage; 10 GB/month CDN data transfer; 2 GB maximum individual file. |
| **GitHub Pages** | Static Hosting | Always Free | Not required | **Restricted** | No | Yes | Published site <= 1 GB; 100 GB/month soft bandwidth limit; 10 builds/hour soft limit for built-in Pages publishing; custom GitHub Actions deployments use Actions limits instead. |
| **GitLab Pages** | Static Hosting | Free Plan | Not required | **Allowed** | No | Yes | 400 compute minutes/month on Free namespaces; 10 GiB repository/LFS storage per project; 200,000 file entries per Pages site; 150 custom domains/site. |
| **Neocities** | Static Hosting | Free Plan | Not required | **Allowed** | No | No | 1 GB storage; 200 GB bandwidth; free account uses a site subdomain; custom domains are supporter-only. |
| **Surge** | Static Hosting | Free Plan | Not required | **No** | No | No | Free publishing with custom domain and basic SSL; production-oriented features such as custom SSL, redirects, CORS, and password protection are paid. |
| **Netlify** | Frontend Platforms | Free Plan | Not required | **Allowed** | Yes | Yes | 300 credits/month; production deploy 15 credits; bandwidth 20 credits/GB; web requests 2 credits/10K requests; compute 10 credits/GB-hour. |
| **Vercel (Hobby Plan)** | Frontend Platforms | Free Plan | Not required | **No** | No | No | 200 projects; 100 deployments/day; 100 builds/hour; 45-minute build time/deployment; 100 MB static file upload; 1 concurrent deployment. |
| **AWS Lambda** | Serverless & Edge Compute | Always Free | Required | **Allowed** | No | Yes | 1 million requests/month and 400,000 GB-seconds/month free for Lambda functions. |
| **Cloudflare Workers** | Serverless & Edge Compute | Always Free | Not required | **Allowed** | No | Yes | 100,000 requests/day on the Workers Free plan; 10 ms CPU time/request. |
| **Deno Deploy** | Serverless & Edge Compute | Free Plan | Not required | **Restricted** | Yes | No | 1M requests/month; 20 GiB egress/month; 10 active CPU hours/month; 5 custom domains; 10 active apps. |
| **Google Cloud Run** | Containers & Full-Stack Cloud | Always Free | Required | **Allowed** | Yes | Yes | 2 million requests/month; 360,000 GiB-seconds memory; 180,000 vCPU-seconds; 1 GB North America outbound transfer/month under the listed free tier. |
| **Koyeb** | Containers & Full-Stack Cloud | Free Plan | Required | **Allowed** | Yes | No | 1 free Service/org in Frankfurt or Washington, D.C.; 512 MB RAM; 0.1 vCPU; 2 GB SSD; no volumes; scale-to-zero after 1 hour. |
| **Render** | Containers & Full-Stack Cloud | Free Plan | Not required | **Allowed** | Yes | No | 750 free instance hours/workspace/month; web services sleep after 15m idle; free Postgres is 1 GB and expires after 30 days. |
| **Appwrite Cloud** | Managed Databases & BaaS | Free Plan | Conditional | **Allowed** | Yes | No | 2 projects; 5 GB bandwidth/month; 2 GB storage; 750K function executions/month; 75K MAU; 1 database, 1 bucket and 2 functions/project. |
| **Cloudflare D1** | Managed Databases & BaaS | Always Free | Not required | **Allowed** | No | No | 10 databases/account; 500 MB/database; 5 GB total free storage; 5M rows read/day; 100K rows written/day; 7-day Time Travel. |
| **MongoDB Atlas (M0)** | Managed Databases & BaaS | Free Plan | Not required | **Allowed** | Yes | No | 0.5 GB storage including indexes; shared RAM/vCPU; one Free cluster per project; free clusters are for small-scale development and are automatically paused after 30 days inactivity. |
| **Neon** | Managed Databases & BaaS | Free Plan | Not required | **Allowed** | Yes | Yes | 1 GB Postgres storage/project; 100 projects; 100 CU-hours/project/month; 10 branches/project; up to 2 CU autoscaling; 5 GB public network transfer/project/month. |
| **Supabase** | Managed Databases & BaaS | Free Plan | Not required | **Allowed** | Yes | Yes | 500 MB database size; 1 GB file storage; 5 GB egress; 2 active projects; 50,000 MAU. |
| **Turso** | Managed Databases & BaaS | Free Plan | Not required | **Allowed** | No | Yes | 100 databases; 5 GB total storage; 500M rows read (scanned)/month; 10M rows written/month; 3 GB syncs/month; 1-day PITR. |
| **Upstash Redis** | Managed Databases & BaaS | Free Plan | Not required | **Allowed** | No | No | 1 free database; 256 MB data; 10 GB monthly bandwidth; 500,000 commands/month. |
| **Backblaze B2** | Object Storage | Always Free | Not required | **Allowed** | No | Yes | First 10 GB storage is always free; free egress up to 3× average monthly stored data; egress above that may be free via supported CDN/compute partners. |
| **Cloudflare R2** | Object Storage | Always Free | Required | **Allowed** | No | Yes | 10 GB-month storage/month; 1M Class A ops/month; 10M Class B ops/month; Internet egress is free. |
| **Google Compute Engine (e2-micro Free Tier)** | Free VPS & Compute | Always Free | Required | **Allowed** | No | Yes | 1 non-preemptible e2-micro VM/month in us-west1/us-central1/us-east1; 30 GB-month standard persistent disk; 1 GB/month North America outbound transfer. |
| **Oracle Cloud Always Free** | Free VPS & Compute | Always Free | Required | **Allowed** | No | Yes | Up to 2 OCPUs and 12 GB RAM on Ampere A1 Always Free allocation; 200 GB total Always Free block volume. |
| **Google Colab** | AI, GPU & Data Apps | Free Plan | Not required | **Restricted** | Yes | No | Ephemeral notebook sessions; GPU/TPU availability is dynamic and not guaranteed. |
| **Hugging Face Spaces** | AI, GPU & Data Apps | Free Plan | Not required | **Restricted** | Yes | No | Static Spaces are free; Gradio/Docker Spaces run on compute and require a paid plan for new deployments; free ZeroGPU access is limited and dynamic. |
| **Kaggle Notebooks** | AI, GPU & Data Apps | Free Plan | Not required | **Restricted** | Yes | No | Free GPU access is available through notebook settings; current documentation notes NVIDIA P100 availability but warns that free GPU capacity can be queued or unavailable at busy times. |
| **Streamlit Community Cloud** | AI, GPU & Data Apps | Free Plan | Not required | **No** | Yes | No | Public apps plus 1 private app; 1 GB RAM/app; current Community Cloud terms restrict certain personal-information use to personal/non-commercial purposes. |
| **AlwaysData** | PHP & Traditional Hosting | Free Plan | Not required | **No** | No | No | 1 GB disk; 256 MB RAM; 1/4 CPU; free plan cannot be used for profit and website address is limited to alwaysdata.net. |
| **Byet.host** | PHP & Traditional Hosting | Free Plan | Not required | **Restricted** | No | No | 5 GB NVMe storage; provider advertises unlimited monthly bandwidth; PHP 8.3; MySQL 8; 10 MB upload limit; 400+ one-click apps. |
| **HelioHost** | PHP & Traditional Hosting | Free Plan | Not required | **Restricted** | No | No | Johnny: 5 domains, 200 GB memory/day and 10k CPU/day with unlimited-bandwidth advertising subject to fair use; Tommy: 10 domains with similar daily memory/CPU ceilings. |
| **InfinityFree** | PHP & Traditional Hosting | Free Plan | Not required | **Allowed** | No | No | 5 GB storage; 50,000 daily hits; 30,000 inodes; shared CPU/resource limits; no built-in free email service. |
| **Serv00** | PHP & Traditional Hosting | Free Plan | Not required | **Allowed** | No | No | 3 GB disk; 512 MB RAM quota; shared CPU limits; periodic account activity required. |
| **Bubble** | No-Code App Builders | Free Development | Not required | **No** | No | No | Development version only; 50K workload units/month; 1 app editor; live website and custom domain are paid-plan features. |
| **Read the Docs** | Documentation Hosting | Free Plan | Not required | **No** | No | Yes | Community tier is for open-source documentation, public repositories, and public docs; it includes advertising and has fewer build resources than paid Business hosting. |

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

#### Firebase Hosting
- **Best for:** Static websites and single-page applications with a global CDN and Firebase integration.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Allowed** — Firebase terms cover business use; the free Hosting quota is separate from paid/billing requirements for other Firebase products.
- **Sleep / pause:** No
- **Reclaim policy:** Sites are disabled after the no-cost monthly Hosting transfer limit is exhausted until the next month unless upgraded.
- **Custom domain:** Yes
- **Production-ready for the free use case:** Yes
- **Hard limit / catch:** 10 GB Hosting storage; 10 GB/month CDN data transfer; 2 GB maximum individual file.
- **Brilliant feature:** Global CDN-backed static hosting with straightforward Firebase CLI deployment.
- **Official source:** [firebase.google.com](https://firebase.google.com/docs/hosting/usage-quotas-pricing)
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

#### GitLab Pages
- **Best for:** Git-based static sites and documentation integrated with GitLab CI/CD.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Allowed** — GitLab Free can be used for commercial projects subject to GitLab terms; Pages is deployed through GitLab CI/CD.
- **Sleep / pause:** No
- **Reclaim policy:** Pages itself has no documented sleep policy; CI/CD and storage quotas still apply.
- **Custom domain:** Yes
- **Production-ready for the free use case:** Yes
- **Hard limit / catch:** 400 compute minutes/month on Free namespaces; 10 GiB repository/LFS storage per project; 200,000 file entries per Pages site; 150 custom domains/site.
- **Brilliant feature:** Native CI/CD-powered static publishing tightly integrated with GitLab projects.
- **Official source:** [docs.gitlab.com](https://docs.gitlab.com/user/project/pages/introduction/)
- **Last verified:** 2026-10-08

#### Neocities
- **Best for:** Personal, artistic, educational, and independent-web static sites.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Allowed** — Current Terms explicitly contemplate commerce by users; the free plan is primarily suited to simple public static sites and does not include supporter-only features such as custom domains.
- **Sleep / pause:** No
- **Reclaim policy:** Accounts remain subject to Neocities Terms and Acceptable Use Policy.
- **Custom domain:** No
- **Production-ready for the free use case:** No
- **Hard limit / catch:** 1 GB storage; 200 GB bandwidth; free account uses a site subdomain; custom domains are supporter-only.
- **Brilliant feature:** A community-oriented static host focused on independent websites without advertising on member sites.
- **Official source:** [neocities.org](https://neocities.org/supporter)
- **Last verified:** 2026-10-08

#### Surge
- **Best for:** Very simple static sites deployed from the command line.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **No** — The current Terms prohibit commercial exploitation of the Surge website/services; the Free product is positioned for simple publishing/testing rather than unlimited production projects.
- **Sleep / pause:** No
- **Reclaim policy:** Surge may terminate projects for unreasonable infrastructure burden or under its current terms.
- **Custom domain:** Yes
- **Production-ready for the free use case:** No
- **Hard limit / catch:** Free publishing with custom domain and basic SSL; production-oriented features such as custom SSL, redirects, CORS, and password protection are paid.
- **Brilliant feature:** Extremely simple CLI deployment: install Surge and publish a folder in one command.
- **Official source:** [surge.sh](https://surge.sh/pricing)
- **Last verified:** 2026-10-08

### Frontend Platforms

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

### Serverless & Edge Compute

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

#### Deno Deploy
- **Best for:** JavaScript and TypeScript edge applications built with Deno.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Restricted** — The current Free plan is described for personal use and smaller projects; use for commercial workloads requires checking Deno terms and plan fit.
- **Sleep / pause:** Yes
- **Reclaim policy:** Idle applications automatically shut down after about 20–30 seconds.
- **Custom domain:** Yes
- **Production-ready for the free use case:** No
- **Hard limit / catch:** 1M requests/month; 20 GiB egress/month; 10 active CPU hours/month; 5 custom domains; 10 active apps.
- **Brilliant feature:** Native Deno/TypeScript deployment with automatic GitHub deployments, previews, and edge execution.
- **Official source:** [deno.com](https://deno.com/deploy/pricing)
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

### Managed Databases & BaaS

#### Appwrite Cloud
- **Best for:** Open-source BaaS with database, authentication, storage, functions, messaging, and sites.
- **Free model:** Free Plan
- **Card requirement:** Conditional
- **Commercial policy:** **Allowed** — The Free plan is for passion projects and small applications; Appwrite's Terms restrict specific misuse and paid verification may be requested.
- **Sleep / pause:** Yes
- **Reclaim policy:** Free projects are paused after 1 week of inactivity.
- **Custom domain:** No
- **Production-ready for the free use case:** No
- **Hard limit / catch:** 2 projects; 5 GB bandwidth/month; 2 GB storage; 750K function executions/month; 75K MAU; 1 database, 1 bucket and 2 functions/project.
- **Brilliant feature:** A broad hosted BaaS with database, auth, storage, functions, realtime and site hosting under one Free plan.
- **Official source:** [appwrite.io](https://appwrite.io/pricing)
- **Last verified:** 2026-10-08

#### Cloudflare D1
- **Best for:** Small SQLite-compatible databases attached to Cloudflare Workers and edge applications.
- **Free model:** Always Free
- **Card requirement:** Not required
- **Commercial policy:** **Allowed** — D1 is included in the Workers Free plan; usage remains subject to Cloudflare terms and daily free limits.
- **Sleep / pause:** No
- **Reclaim policy:** Queries fail after daily free read/write limits are exceeded until the reset.
- **Custom domain:** No
- **Production-ready for the free use case:** No
- **Hard limit / catch:** 10 databases/account; 500 MB/database; 5 GB total free storage; 5M rows read/day; 100K rows written/day; 7-day Time Travel.
- **Brilliant feature:** SQLite-compatible storage directly integrated with Cloudflare Workers.
- **Official source:** [developers.cloudflare.com](https://developers.cloudflare.com/d1/platform/pricing/)
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

### Free VPS & Compute

#### Google Compute Engine (e2-micro Free Tier)
- **Best for:** A small persistent Linux VM with SSH access in a supported US region.
- **Free model:** Always Free
- **Card requirement:** Required
- **Commercial policy:** **Allowed** — Google Cloud commercial use is permitted under its terms; a billing account is required to receive the Always Free allowance.
- **Sleep / pause:** No
- **Reclaim policy:** No inactivity reclamation rule is stated for this free allowance; normal service/account eligibility and quota rules apply.
- **Custom domain:** Yes
- **Production-ready for the free use case:** Yes
- **Hard limit / catch:** 1 non-preemptible e2-micro VM/month in us-west1/us-central1/us-east1; 30 GB-month standard persistent disk; 1 GB/month North America outbound transfer.
- **Brilliant feature:** A real VM with root-level control inside the broader Google Cloud ecosystem.
- **Official source:** [docs.cloud.google.com](https://docs.cloud.google.com/free/docs/free-cloud-features)
- **Last verified:** 2026-10-08

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

#### Kaggle Notebooks
- **Best for:** Machine-learning experiments and notebook-based development with optional GPUs.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Restricted** — This is an interactive notebook platform, not a general production host; review current Kaggle Terms for commercial workloads.
- **Sleep / pause:** Yes
- **Reclaim policy:** Notebook sessions are temporary and hardware availability can place users in a queue.
- **Custom domain:** No
- **Production-ready for the free use case:** No
- **Hard limit / catch:** Free GPU access is available through notebook settings; current documentation notes NVIDIA P100 availability but warns that free GPU capacity can be queued or unavailable at busy times.
- **Brilliant feature:** Preconfigured notebook environments with free GPU access for ML experimentation.
- **Official source:** [www.kaggle.com](https://www.kaggle.com/docs/notebooks)
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

### PHP & Traditional Hosting

#### AlwaysData
- **Best for:** Small personal/non-profit PHP and multi-language projects.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **No** — The Free plan cannot be used for profit purposes and is limited to an alwaysdata.net account address.
- **Sleep / pause:** No
- **Reclaim policy:** No ordinary idle-sleep policy is stated for the Free shared plan.
- **Custom domain:** No
- **Production-ready for the free use case:** No
- **Hard limit / catch:** 1 GB disk; 256 MB RAM; 1/4 CPU; free plan cannot be used for profit and website address is limited to alwaysdata.net.
- **Brilliant feature:** Broad runtime/database support in a tiny free environment.
- **Official source:** [help.alwaysdata.com](https://help.alwaysdata.com/en/docs/admin-billing/billing/public-cloud-prices/)
- **Last verified:** 2026-10-08

#### Byet.host
- **Best for:** WordPress, PHP, MySQL, and traditional shared hosting without a paid VPS.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Restricted** — The provider advertises a broad free hosting offer, but acceptable-use/resource rules still apply; verify suitability for commercial production workloads.
- **Sleep / pause:** No
- **Reclaim policy:** Accounts remain subject to the provider's acceptable-use and resource policies.
- **Custom domain:** Yes
- **Production-ready for the free use case:** No
- **Hard limit / catch:** 5 GB NVMe storage; provider advertises unlimited monthly bandwidth; PHP 8.3; MySQL 8; 10 MB upload limit; 400+ one-click apps.
- **Brilliant feature:** Traditional VistaPanel hosting with PHP/MySQL and one-click application installation.
- **Official source:** [byet.host](https://byet.host/free-hosting)
- **Last verified:** 2026-10-08

#### HelioHost
- **Best for:** PHP and multi-language hosting when you want more than basic shared PHP.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **Restricted** — Johnny and Tommy are intended for non-commercial use; newly launched microbusinesses can be accepted subject to review.
- **Sleep / pause:** No
- **Reclaim policy:** Free-account availability depends on the current server/signup policy; commercial accounts may be required to move to paid hosting.
- **Custom domain:** Yes
- **Production-ready for the free use case:** No
- **Hard limit / catch:** Johnny: 5 domains, 200 GB memory/day and 10k CPU/day with unlimited-bandwidth advertising subject to fair use; Tommy: 10 domains with similar daily memory/CPU ceilings.
- **Brilliant feature:** Long-running community hosting with PHP and broader language support on free servers.
- **Official source:** [heliohost.org](https://heliohost.org/signup/)
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

### No-Code App Builders

#### Bubble
- **Best for:** Visual no-code web and mobile application development.
- **Free model:** Free Development
- **Card requirement:** Not required
- **Commercial policy:** **No** — The Free plan is explicitly for projects under construction; launching a live production application requires a paid plan.
- **Sleep / pause:** No
- **Reclaim policy:** Free projects remain development versions; production capabilities require a paid subscription.
- **Custom domain:** No
- **Production-ready for the free use case:** No
- **Hard limit / catch:** Development version only; 50K workload units/month; 1 app editor; live website and custom domain are paid-plan features.
- **Brilliant feature:** Visual workflows, database logic, API integration, and app UI without traditional coding.
- **Official source:** [bubble.io](https://bubble.io/pricing/compare)
- **Last verified:** 2026-10-08

### Documentation Hosting

#### Read the Docs
- **Best for:** Versioned technical documentation built from public open-source Git repositories.
- **Free model:** Free Plan
- **Card requirement:** Not required
- **Commercial policy:** **No** — Read the Docs Community is free for open-source projects; commercial and non-free documentation uses paid Business plans.
- **Sleep / pause:** No
- **Reclaim policy:** No sleep policy is stated for Community hosting; public docs are subject to Community resource policies.
- **Custom domain:** No
- **Production-ready for the free use case:** Yes
- **Hard limit / catch:** Community tier is for open-source documentation, public repositories, and public docs; it includes advertising and has fewer build resources than paid Business hosting.
- **Brilliant feature:** Automated documentation builds, versioning, search, previews, and CDN hosting for open-source projects.
- **Official source:** [about.readthedocs.com](https://about.readthedocs.com/pricing/)
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
