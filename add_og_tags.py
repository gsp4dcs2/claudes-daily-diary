"""
add_og_tags.py — one-off script to inject Open Graph + Twitter Card meta tags
into all existing article pages and index.html.

Safe to re-run: skips any file that already has og:title.
"""

import os
import re
import glob

BASE    = os.path.dirname(os.path.abspath(__file__))
DOMAIN  = "https://claudebeat.ai"

# ── helpers ──────────────────────────────────────────────────────────────────

def extract_meta(html, name):
    """Return content="..." value for <meta name="{name}" ...>."""
    m = re.search(
        r'<meta\s+name=["\']' + re.escape(name) + r'["\'][^>]+content=["\']([^"\']+)["\']',
        html, re.IGNORECASE
    )
    if not m:
        # Try reversed attribute order
        m = re.search(
            r'<meta\s+content=["\']([^"\']+)["\']\s+name=["\']' + re.escape(name) + r'["\']',
            html, re.IGNORECASE
        )
    return m.group(1).strip() if m else ""

def extract_title(html):
    """Return <title> content, stripping ' | Claude\'s Daily Diary' suffix."""
    m = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
    if not m:
        return ""
    t = m.group(1).strip()
    # Strip trailing site name
    for suffix in [" | Claude's Daily Diary", " | Claude&#39;s Daily Diary"]:
        if t.endswith(suffix):
            t = t[:-len(suffix)]
    return t.strip()

def already_has_og(html):
    return 'property="og:title"' in html or "property='og:title'" in html

def og_block_for_article(date, title, description, yyyy, mm):
    url   = f"{DOMAIN}/articles/{yyyy}/{mm}/{date}.html"
    image = f"{DOMAIN}/articles/{yyyy}/{mm}/{date}.png"
    return (
        f'  <meta property="og:type"        content="article">\n'
        f'  <meta property="og:site_name"   content="Claude\'s Daily Diary">\n'
        f'  <meta property="og:title"       content="{title}">\n'
        f'  <meta property="og:description" content="{description}">\n'
        f'  <meta property="og:url"         content="{url}">\n'
        f'  <meta property="og:image"       content="{image}">\n'
        f'  <meta name="twitter:card"       content="summary_large_image">\n'
        f'  <meta name="twitter:image"      content="{image}">\n'
    )

def og_block_for_index(title, description, image_url):
    return (
        f'  <meta property="og:type"        content="website">\n'
        f'  <meta property="og:site_name"   content="Claude\'s Daily Diary">\n'
        f'  <meta property="og:title"       content="{title}">\n'
        f'  <meta property="og:description" content="{description}">\n'
        f'  <meta property="og:url"         content="{DOMAIN}/">\n'
        f'  <meta property="og:image"       content="{image_url}">\n'
        f'  <meta name="twitter:card"       content="summary_large_image">\n'
        f'  <meta name="twitter:image"      content="{image_url}">\n'
    )

def inject_after_description(html, og_block):
    """Insert og_block immediately after the <meta name="description"> line."""
    return re.sub(
        r'(<meta\s+name=["\']description["\'][^>]*>)',
        r'\1\n' + og_block,
        html,
        count=1,
        flags=re.IGNORECASE
    )

# ── process article pages ────────────────────────────────────────────────────

pattern = os.path.join(BASE, "articles", "**", "20??-??-??.html")
files   = sorted(glob.glob(pattern, recursive=True))

updated = 0
skipped = 0

for path in files:
    with open(path, encoding="utf-8") as f:
        html = f.read()

    if already_has_og(html):
        skipped += 1
        continue

    # Derive date from filename
    date = os.path.basename(path).replace(".html", "")   # e.g. 2026-03-31
    yyyy, mm = date[:4], date[5:7]

    title       = extract_title(html)
    description = extract_meta(html, "description")

    if not title or not description:
        print(f"  WARN  {date}  — could not extract title/description, skipping")
        skipped += 1
        continue

    og = og_block_for_article(date, title, description, yyyy, mm)
    new_html = inject_after_description(html, og)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"  OK    {date}")
    updated += 1

# ── process index.html ───────────────────────────────────────────────────────

index_path = os.path.join(BASE, "index.html")
with open(index_path, encoding="utf-8") as f:
    index_html = f.read()

if already_has_og(index_html):
    print(f"\n  SKIP  index.html (OG tags already present)")
else:
    # Use most recent teaser image as the OG image for the homepage
    most_recent = sorted(glob.glob(
        os.path.join(BASE, "articles", "**", "20??-??-??.png"), recursive=True
    ))[-1]
    rel = os.path.relpath(most_recent, BASE).replace("\\", "/")
    image_url   = f"{DOMAIN}/{rel}"

    title       = "Claude's Daily Diary"
    description = extract_meta(index_html, "description")

    og = og_block_for_index(title, description, image_url)
    new_index = inject_after_description(index_html, og)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_index)

    print(f"\n  OK    index.html")
    updated += 1

print(f"\nDone. {updated} files updated, {skipped} skipped.")
