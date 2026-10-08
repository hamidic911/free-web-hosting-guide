# Contributing

Thank you for contributing to **Awesome Free Web Hosting & Cloud 2026**.

## Rules

1. Use the provider's official pricing, limits, Terms, documentation, or official product announcements as the primary source.
2. Update `services.yml` first. Do not hand-edit generated JSON/site files when the data comes from the catalog.
3. Use `commercial_policy: Allowed | Restricted | No` rather than a boolean.
4. Use `card_requirement: Required | Conditional | Not required`.
5. State the hard limit and the consequence of inactivity or quota exhaustion when applicable.
6. Do not add star ratings, S/A/B tiers, affiliate links, or unsupported “best” claims.
7. Update `last_verified` whenever a factual field changes.

## Local validation

```bash
python -m pip install -r requirements.txt
python scripts/validate_repo.py
```

The validator rebuilds the site data and checks the canonical schema, generated JSON, internal links, sitemap entries, and stale terminology.
