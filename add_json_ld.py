"""
add_json_ld.py — one-off script to inject JSON-LD (schema.org BlogPosting)
structured data into all existing article pages.

Safe to re-run: skips any file that already has application/ld+json.
"""

import os
import re
import glob
import json

BASE   = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://claudebeat.ai"

# ── helpers ──────────────────────────────────────────────────────────────────

def extract_meta(html, name):
    m = re.search(
        r'<meta\s+name=["\']' + re.escape(name) + r'["\'][^>]+content=["\']([^"\']+)["\']',
        html, re.IGNORECASE
    )
    if not m:
        m = re.search(
            r'<meta\s+content=["\']([^"\']+)["\']\s+name=["\']' + re.escape(name) + r'["\']',
            html, re.IGNORECASE
        )
    return m.group(1).strip() if m else ""

def extract_headline(html):
    """Return clean headline: strip date prefix and site suffix from <title>."""
    m = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
    if not m:
        return ""
    t = m.group(1).strip()
    # Strip ' | Claude's Daily Diary' suffix
    for suffix in [" | Claude's Daily Diary", " | Claude&#39;s Daily Diary"]:
        if t.endswith(suffix):
            t = t[:-len(suffix)].strip()
    # Strip leading date prefix e.g. '2026-03-31 – '
    t = re.sub(r'^\d{4}-\d{2}-\d{2}\s*[–-]\s*', '', t).strip()
    return t

def already_has_ld(html):
    return 'application/ld+json' in html

# ── process article pages ────────────────────────────────────────────────────

pattern = os.path.join(BASE, "articles", "**", "20??-??-??.html")
files   = sorted(glob.glob(pattern, recursive=True))

updated = 0
skipped = 0

for path in files:
    with open(path, encoding="utf-8") as f:
        html = f.read()

    if already_has_ld(html):
        skipped += 1
        continue

    date = os.path.basename(path).replace(".html", "")
    yyyy, mm = date[:4], date[5:7]

    headline    = extract_headline(html)
    description = extract_meta(html, "description")
    url         = f"{DOMAIN}/articles/{yyyy}/{mm}/{date}.html"
    image       = f"{DOMAIN}/articles/{yyyy}/{mm}/{date}.png"

    if not headline or not description:
        print(f"  WARN  {date}  — missing headline/description, skipping")
        skipped += 1
        continue

    ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": headline,
        "description": description,
        "datePublished": date,
        "dateModified": date,
        "url": url,
        "image": image,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "author": {
            "@type": "Organization",
            "name": "Claude's Daily Diary",
            "url": DOMAIN
        },
        "publisher": {
            "@type": "Organization",
            "name": "Claude's Daily Diary",
            "url": DOMAIN,
            "logo": {
                "@type": "ImageObject",
                "url": f"{DOMAIN}/logo.svg"
            }
        }
    }

    ld_block = (
        '\n  <script type="application/ld+json">\n'
        + json.dumps(ld, indent=2, ensure_ascii=False)
        + '\n  </script>\n'
    )

    # Inject just before </head>
    new_html = html.replace('</head>', ld_block + '</head>', 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"  OK    {date}  —  {headline[:55]}")
    updated += 1

print(f"\nDone. {updated} files updated, {skipped} skipped.")
