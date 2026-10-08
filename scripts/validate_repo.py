#!/usr/bin/env python3
"""Validate canonical data and every generated repository artifact."""
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
import json
import re
import sys
import xml.etree.ElementTree as ET
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "services.yml"

POLICIES = {"Allowed", "Restricted", "No"}
CARDS = {"Required", "Conditional", "Not required"}
CLASSES = {"Always Free", "Free Plan", "Free Development", "Free Credits", "Trial"}
CATEGORIES = (
    "static-hosting", "frontend-platforms", "serverless-edge", "containers-cloud",
    "databases-baas", "object-storage", "free-vps", "ai-gpu-apps", "php-traditional",
    "no-code", "documentation",
)
REQUIRED_FIELDS = [
    "id", "name", "category", "free_class", "card_requirement", "commercial_policy",
    "commercial_note", "sleeps", "reclaim_policy", "custom_domain", "production_ready",
    "best_for", "hard_limit", "brilliant_feature", "official_source", "last_verified",
]
STALE_STRINGS = [
    "10,000 commands per day", "10,000 commands/day",
    "1 GB daily egress", "CPU utilization < 2%", "CPU <2%",
    "100 GB bandwidth/mo", "100 GB bandwidth/month",
    "125,000 function invocations", "100 build execution hours",
    "commercial_allowed:", "card_required:", "free CPU Basic",
    "2.5 GB disk", "500 databases", "1 billion row reads",
    "0.5 GB storage limit per project", "1 project allowance", "always-on container hosting",
]
BASE_SITE_FILES = {
    "index.html", "app.js", "style.css", "services.json", "sitemap.xml", "robots.txt",
    *[f"{c}.html" for c in CATEGORIES],
}


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="strict")


def validate_schema(data: dict) -> set[str]:
    if not isinstance(data, dict):
        fail("services.yml root must be a mapping")
    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        fail("metadata is missing")
    if metadata.get("schema_version") != 2:
        fail("schema_version must be 2")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(metadata.get("version", ""))):
        fail("metadata.version must use semantic versioning")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(metadata.get("last_updated", ""))):
        fail("metadata.last_updated must be YYYY-MM-DD")

    services = data.get("services")
    if not isinstance(services, list) or not services:
        fail("services.yml has no services")

    ids: set[str] = set()
    for index, service in enumerate(services):
        sid = service.get("id", f"index-{index}") if isinstance(service, dict) else f"index-{index}"
        if not isinstance(service, dict):
            fail(f"[{sid}] record must be a mapping")
        for field in REQUIRED_FIELDS:
            if field not in service:
                fail(f"[{sid}] missing required field: {field}")
        if sid in ids:
            fail(f"duplicate service id: {sid}")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(sid)):
            fail(f"[{sid}] id must be lowercase kebab-case")
        ids.add(sid)
        if service["category"] not in CATEGORIES:
            fail(f"[{sid}] invalid category: {service['category']}")
        if service["free_class"] not in CLASSES:
            fail(f"[{sid}] invalid free_class: {service['free_class']}")
        if service["commercial_policy"] not in POLICIES:
            fail(f"[{sid}] invalid commercial_policy: {service['commercial_policy']}")
        if service["card_requirement"] not in CARDS:
            fail(f"[{sid}] invalid card_requirement: {service['card_requirement']}")
        for field in ("commercial_note", "reclaim_policy", "best_for", "hard_limit", "brilliant_feature"):
            if not isinstance(service[field], str) or not service[field].strip():
                fail(f"[{sid}] {field} must be a non-empty string")
        for field in ("sleeps", "custom_domain", "production_ready"):
            if not isinstance(service[field], bool):
                fail(f"[{sid}] {field} must be boolean")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(service["last_verified"])):
            fail(f"[{sid}] last_verified must be YYYY-MM-DD")
        source = str(service["official_source"])
        parsed = urlparse(source)
        if parsed.scheme != "https" or not parsed.netloc:
            fail(f"[{sid}] official_source must be a valid HTTPS URL")
        if parsed.query or parsed.fragment:
            fail(f"[{sid}] official_source must not contain tracking/query/fragment parameters")
    return ids


def validate_generated_json(data: dict) -> None:
    for path in (ROOT / "services.json", ROOT / "site/services.json"):
        if not path.exists():
            fail(f"missing generated JSON: {path.relative_to(ROOT)}")
        try:
            actual = json.loads(read_text(path))
        except Exception as exc:
            fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
        if actual != data:
            fail(f"{path.relative_to(ROOT)} differs from services.yml")


def validate_site_files() -> None:
    for relative in BASE_SITE_FILES:
        if not (ROOT / "site" / relative).exists():
            fail(f"missing site artifact: site/{relative}")

    expected_html = {"index.html", *[f"{c}.html" for c in CATEGORIES]}
    actual_html = {p.name for p in (ROOT / "site").glob("*.html")}
    if actual_html != expected_html:
        fail(f"site HTML mismatch: expected {sorted(expected_html)}, found {sorted(actual_html)}")


def validate_relative_links() -> None:
    site = ROOT / "site"
    pattern = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']", re.I)
    for page in site.glob("*.html"):
        for target in pattern.findall(read_text(page)):
            if target.startswith(("http://", "https://", "#", "mailto:", "tel:", "data:", "javascript:")):
                continue
            clean = target.split("#", 1)[0].split("?", 1)[0]
            if not clean:
                continue
            target_path = (site / clean).resolve()
            if site.resolve() not in target_path.parents and target_path != site.resolve():
                fail(f"unsafe relative link in site/{page.name}: {target}")
            if not target_path.exists():
                fail(f"broken relative link in site/{page.name}: {target}")


def validate_sitemap() -> None:
    sitemap = ROOT / "site/sitemap.xml"
    try:
        tree = ET.parse(sitemap)
    except Exception as exc:
        fail(f"invalid sitemap XML: {exc}")
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text for loc in tree.getroot().findall("sm:url/sm:loc", ns) if loc.text]
    expected = [
        "https://hamidic911.github.io/free-web-hosting-guide/",
        *[f"https://hamidic911.github.io/free-web-hosting-guide/{c}.html" for c in CATEGORIES],
    ]
    if urls != expected:
        fail("sitemap URLs do not exactly match generated site pages")
    for url in urls:
        rel = url.split("/free-web-hosting-guide/", 1)[-1] or "index.html"
        if not (ROOT / "site" / rel).exists():
            fail(f"sitemap target missing: {rel}")
    robots = read_text(ROOT / "site/robots.txt")
    if "Sitemap: https://hamidic911.github.io/free-web-hosting-guide/sitemap.xml" not in robots:
        fail("robots.txt does not reference the canonical sitemap")


def validate_stale_strings() -> None:
    extensions = {".yml", ".yaml", ".json", ".md", ".html", ".js", ".py", ".yml"}
    validator_path = Path(__file__).resolve()
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path == validator_path or path.suffix.lower() not in extensions:
            continue
        text = read_text(path).lower()
        for stale in STALE_STRINGS:
            if stale.lower() in text:
                fail(f"stale string {stale!r} found in {path.relative_to(ROOT)}")


def validate_workflow() -> None:
    workflow = read_text(ROOT / ".github/workflows/deploy-pages.yml")
    required_fragments = [
        "actions/checkout@v7",
        "actions/setup-python@v7",
        "actions/configure-pages@v6",
        "actions/upload-pages-artifact@v5",
        "actions/deploy-pages@v5",
        "contents: read",
        "pages: write",
        "id-token: write",
        "path: site",
        "python scripts/build_site.py",
        "python scripts/validate_repo.py",
    ]
    for fragment in required_fragments:
        if fragment not in workflow:
            fail(f"workflow missing required fragment: {fragment}")


def validate_cross_fields(data: dict) -> None:
    by_id = {s["id"]: s for s in data["services"]}
    # Explicit guardrails for the facts that previously regressed in the repository.
    expected_policies = {
        "koyeb": "Allowed",
        "upstash-redis": "Allowed",
        "backblaze-b2": "Allowed",
        "github-pages": "Restricted",
        "vercel": "No",
        "netlify": "Allowed",
        "neocities": "Allowed",
        "appwrite": "Allowed",
        "alwaysdata": "No",
        "bubble": "No",
        "read-the-docs": "No",
        "surge": "No",
    }
    expected_free_classes = {"mongodb-atlas": "Free Plan"}
    expected_fragments = {
        "koyeb": "512 MB RAM; 0.1 vCPU; 2 GB SSD",
        "upstash-redis": "500,000 commands/month",
        "backblaze-b2": "3× average monthly stored data",
        "mongodb-atlas": "0.5 GB storage including indexes",
        "github-pages": "Published site <= 1 GB",
        "vercel": "200 projects",
        "netlify": "300 credits/month",
        "deno-deploy": "1M requests/month",
        "firebase-hosting": "10 GB/month CDN data transfer",
        "cloudflare-d1": "5M rows read/day",
        "google-compute-engine": "1 non-preemptible e2-micro VM/month",
        "gitlab-pages": "400 compute minutes/month",
        "byet-host": "5 GB NVMe storage",
        "heliohost": "5 domains",
        "alwaysdata": "256 MB RAM",
        "surge": "Free publishing",
        "neocities": "1 GB storage",
        "appwrite": "750K function executions/month",
        "kaggle-notebooks": "free GPU access",
        "bubble": "50K workload units/month",
        "read-the-docs": "Community tier is for open-source documentation",
    }
    for sid, policy in expected_policies.items():
        if sid not in by_id:
            fail(f"required service missing: {sid}")
        if by_id[sid]["commercial_policy"] != policy:
            fail(f"{sid} commercial_policy regressed: {by_id[sid]['commercial_policy']}")
    for sid, free_class in expected_free_classes.items():
        if sid not in by_id:
            fail(f"required service missing: {sid}")
        if by_id[sid]["free_class"] != free_class:
            fail(f"{sid} free_class regressed: {by_id[sid]['free_class']}")
    for sid, fragment in expected_fragments.items():
        if sid not in by_id:
            fail(f"required service missing: {sid}")
        if fragment.lower() not in by_id[sid]["hard_limit"].lower():
            fail(f"{sid} hard_limit missing required current metric: {fragment}")


def main() -> None:
    data = yaml.safe_load(read_text(DATA_FILE))
    service_ids = validate_schema(data)
    validate_generated_json(data)
    validate_site_files()
    validate_relative_links()
    validate_sitemap()
    validate_stale_strings()
    validate_workflow()
    validate_cross_fields(data)
    print(f"Validation passed: {len(service_ids)} services, schema v{data['metadata']['schema_version']}")


if __name__ == "__main__":
    main()
