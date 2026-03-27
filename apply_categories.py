#!/usr/bin/env python3
"""
apply_categories.py
Adds a three-category system (Daily News / Best Practices / Tips'n'Tricks)
to Claude's Daily Diary.

Changes made:
  1. index.html  — strapline, cat-icon in list items, cat field in SEARCH_INDEX
  2. articles/**/*.html  — cat-badge near date-badge + strapline
"""

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

# ── Category assignments ───────────────────────────────────────────────────
# Default is "news". Overrides below for Best Practices and Tips 'n' Tricks.

TIPS = {
    "2026-01-02",   # SDK v0.45/v0.35 Structured Output Helpers & Batch API
    "2026-01-15",   # 200K Context Faithfulness & Long-Document Processing Guide
    "2026-01-17",   # Structured Outputs Beta & System Prompt Templates Library
    "2026-03-14",   # Context, Caching & Plan Mode — Three Big Upgrades
    "2026-03-15",   # Fast Mode, Compaction API & Claude Code Updates
    "2026-03-19",   # /loop Command, Claude Marketplace, Market Share & AI SRE
}

PRACTICE = {
    "2026-01-06",   # Responsible Use Guide Refreshed & Prompt Injection Defence Brief
    "2026-01-10",   # Model Welfare Commitments & Feature Circuit Interpretability
    "2026-01-20",   # Prompt Injection Resistance Framework & Refusal Calibration
    "2026-01-22",   # Claude's New Constitution Published
    "2026-01-23",   # Agent Teams Pre-GA Architecture & Multi-Agent Best Practices Guide
    "2026-01-25",   # Trust Center & Operator Trust Levels Guide
    "2026-02-06",   # Agent Teams Ship & Multi-Agent Architecture Deep Dive
    "2026-02-16",   # Economic Primitives for AI & API Streaming Improvements
    "2026-02-21",   # Responsible Disclosure, Agent Self-Preservation Limits
    "2026-02-24",   # RSP v3.0 Published in Full & Enterprise Agents Briefing
    "2026-02-26",   # Dario Amodei's Open Letter on AI Responsibility
    "2026-03-03",   # Who Decides How Frontier AI Is Used? The Governance Question
    "2026-03-07",   # The "Whoa Moment" & Multi-Agent Architecture Patterns
    "2026-03-13",   # Getting Started — Claude Best Practices & Core Principles
}

CAT_META = {
    "news":     ("🧭", "Daily News",     "cat-news"),
    "tips":     ("💡", "Tips 'n' Tricks", "cat-tips"),
    "practice": ("✅", "Best Practices",  "cat-practice"),
}

OLD_STRAPLINE = "Best practices, tips &amp; new features — updated daily"
NEW_STRAPLINE = "Best Practices &middot; Tips &#39;n&#39; Tricks &middot; Daily News"


def cat_for(date: str) -> str:
    if date in TIPS:
        return "tips"
    if date in PRACTICE:
        return "practice"
    return "news"


# ── 1. Update all article HTML files ──────────────────────────────────────

articles_dir = os.path.join(ROOT, "articles")
article_files = []
for dirpath, _, filenames in os.walk(articles_dir):
    for fn in filenames:
        if re.match(r"\d{4}-\d{2}-\d{2}\.html$", fn):
            article_files.append(os.path.join(dirpath, fn))

print(f"Found {len(article_files)} article files.")

updated_articles = 0
for filepath in sorted(article_files):
    filename = os.path.basename(filepath)
    date = filename.replace(".html", "")
    cat = cat_for(date)
    icon, label, css_class = CAT_META[cat]

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    changed = False

    # 1a. Update strapline
    if OLD_STRAPLINE in html:
        html = html.replace(OLD_STRAPLINE, NEW_STRAPLINE)
        changed = True

    # 1b. Add cat-badge after date-badge (skip if already present)
    badge_html = f'<span class="cat-badge {css_class}">{icon} {label}</span>'
    date_badge_pattern = f'<span class="date-badge">{date}</span>'
    if date_badge_pattern in html and 'class="cat-badge' not in html:
        html = html.replace(
            date_badge_pattern,
            f'{date_badge_pattern}\n      {badge_html}'
        )
        changed = True

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        updated_articles += 1

print(f"Updated {updated_articles} article files.")


# ── 2. Update index.html ───────────────────────────────────────────────────

index_path = os.path.join(ROOT, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index_html = f.read()

# 2a. Strapline
if OLD_STRAPLINE in index_html:
    index_html = index_html.replace(OLD_STRAPLINE, NEW_STRAPLINE)
    print("Updated strapline in index.html")

# 2b. Add cat-icon to each list item (after article-date span, before article-title span)
# Pattern: <span class="article-date">YYYY-MM-DD</span>
# We insert: <span class="cat-icon" title="LABEL">ICON</span>
# Only if not already present (check for cat-icon class)

def add_cat_icon(match):
    date = match.group(1)
    cat = cat_for(date)
    icon, label, _ = CAT_META[cat]
    return (
        f'<span class="article-date">{date}</span>\n'
        f'          <span class="cat-icon" title="{label}">{icon}</span>'
    )

if 'class="cat-icon"' not in index_html:
    index_html = re.sub(
        r'<span class="article-date">(\d{4}-\d{2}-\d{2})</span>',
        add_cat_icon,
        index_html
    )
    print("Added cat-icon spans to list items in index.html")

# 2c. Add cat field to each SEARCH_INDEX entry
# Find: date: "YYYY-MM-DD",
# Add:  cat: "news",   (or tips/practice)
# Only if cat field not already present

def add_cat_field(match):
    date = match.group(1)
    cat = cat_for(date)
    return f'date: "{date}", cat: "{cat}",'

if 'cat: "' not in index_html:
    index_html = re.sub(
        r'date: "(\d{4}-\d{2}-\d{2})",',
        add_cat_field,
        index_html
    )
    print("Added cat field to SEARCH_INDEX entries in index.html")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(index_html)

print("Done. index.html updated.")
print("\nSummary:")
print(f"  {len(TIPS)} Tips 'n' Tricks days")
print(f"  {len(PRACTICE)} Best Practices days")
print(f"  {len(article_files) - len(TIPS) - len(PRACTICE)} Daily News days")
