#!/usr/bin/env python3
"""
Backfill source trust badges into all diary articles from 2025-12 through 2026-03.

For each <article class="entry"> that lacks a .source-line div:
  1. Extract the Source: URL from the HTML comment above the article block
  2. Map the domain to a star tier (⭐⭐⭐ / ⭐⭐ / ⭐)
  3. Insert <div class="source-line"> before <div class="tag-list">
Then insert <div class="trust-legend"> once per page, just before </main>.

Files that already contain 'trust-legend' are skipped.
"""

import re
import sys
from pathlib import Path

# ── Domain tiers ──────────────────────────────────────────────────────────────

TIER1 = {'anthropic.com', 'support.claude.com', 'red.anthropic.com'}
TIER2 = {
    'techcrunch.com', 'engadget.com', 'techradar.com', 'theverge.com',
    'wired.com', 'arstechnica.com', 'macrumors.com', 'appleinsider.com',
    '9to5mac.com', 'cnbc.com', 'fortune.com', 'bloomberg.com',
    'reuters.com', 'scientificamerican.com', 'techtimes.com',
}


def stars_for_url(url: str) -> tuple[str, str, str]:
    """Return (stars, tooltip, display_domain) for a source URL."""
    if not url or re.match(r'inspired|based on', url, re.IGNORECASE):
        return '⭐⭐⭐', 'Official Anthropic source', 'anthropic.com'
    try:
        domain = url.split('/')[2].lstrip('www.')
    except IndexError:
        return '⭐', 'Community / research — cross-checked', url[:40]
    if domain in TIER1:
        return '⭐⭐⭐', 'Official Anthropic source', domain
    # github.com/anthropics counts as official
    if domain == 'github.com' and '/anthropics/' in url:
        return '⭐⭐⭐', 'Official Anthropic source', domain
    if domain in TIER2:
        return '⭐⭐', 'Established press — verified journalism', domain
    return '⭐', 'Community / research — cross-checked', domain


TRUST_LEGEND = '''\
  <div class="trust-legend">
    <strong>Source trust ratings</strong>
    <span title="Official Anthropic source — anthropic.com, support.claude.com, official GitHub">⭐⭐⭐</span> Official Anthropic &nbsp;&middot;&nbsp;
    <span title="Established press — TechCrunch, Bloomberg, Ars Technica, Reuters, Wired etc.">⭐⭐</span> Established press &nbsp;&middot;&nbsp;
    <span title="Community content or research analytics — independently cross-checked before publication">⭐</span> Community / research
  </div>'''


def make_source_line(stars: str, tooltip: str, domain: str, url: str) -> str:
    if url.startswith('http'):
        inner = f'<a href="{url}" class="source-link" target="_blank" rel="noopener">{domain}</a>'
    else:
        inner = f'<span class="source-link">{domain}</span>'
    return (
        f'  <div class="source-line">\n'
        f'    <span class="trust-badge" title="{tooltip}">{stars}</span>\n'
        f'    {inner}\n'
        f'  </div>'
    )


def process_file(path: Path) -> tuple[bool, int]:
    """
    Returns (was_written, num_badges_inserted).
    was_written=False means the file was skipped (already has trust-legend).
    """
    content = path.read_text(encoding='utf-8')

    if 'trust-legend' in content:
        return False, 0

    article_re = re.compile(r'<article class="entry">(.*?)</article>', re.DOTALL)
    matches = list(article_re.finditer(content))

    if not matches:
        return False, 0

    insertions = 0

    # Process in reverse order so earlier offsets stay valid
    for m in reversed(matches):
        body = m.group(1)
        if 'source-line' in body:
            continue  # already has a badge (shouldn't happen, but be safe)

        # Look back up to 900 chars for the nearest Source: comment
        window = content[max(0, m.start() - 900): m.start()]
        src_m = re.search(
            r'Source:\s*(https?://\S+|Inspired[^\n\r]*|Based[^\n\r]*)',
            window, re.IGNORECASE
        )
        raw_url = src_m.group(1).rstrip(' *=\r\n') if src_m else ''

        stars, tooltip, domain = stars_for_url(raw_url)
        link_url = raw_url if raw_url.startswith('http') else ''

        badge_html = make_source_line(stars, tooltip, domain, link_url)

        # Find <div class="tag-list"> inside this article
        tag_pos = content.find('<div class="tag-list">', m.start(), m.end())
        insert_at = tag_pos if tag_pos != -1 else (m.end() - len('</article>'))

        content = content[:insert_at] + '\n' + badge_html + '\n\n' + content[insert_at:]
        insertions += 1

    if insertions == 0:
        return False, 0

    # Insert trust-legend just before the last </main>
    main_pos = content.rfind('</main>')
    if main_pos != -1:
        content = content[:main_pos] + TRUST_LEGEND + '\n\n  ' + content[main_pos:]

    path.write_text(content, encoding='utf-8')
    return True, insertions


def main():
    root = Path(__file__).resolve().parent.parent

    targets = [
        root / 'articles' / '2025' / '12',
        root / 'articles' / '2026' / '01',
        root / 'articles' / '2026' / '02',
        root / 'articles' / '2026' / '03',
    ]

    dry_run = '--dry-run' in sys.argv

    total_files = 0
    total_badges = 0
    skipped = 0

    for month_dir in targets:
        if not month_dir.exists():
            print(f'  (skipping missing dir: {month_dir})')
            continue
        print(f'\n{month_dir.relative_to(root)}')
        for html_file in sorted(month_dir.glob('*.html')):
            if dry_run:
                content = html_file.read_text(encoding='utf-8')
                if 'trust-legend' in content:
                    print(f'  — {html_file.name}: already done')
                    skipped += 1
                else:
                    count = len(re.findall(r'<article class="entry">', content))
                    print(f'  ~ {html_file.name}: would add ~{count} badge(s)')
                continue

            written, count = process_file(html_file)
            if not written:
                print(f'  — {html_file.name}: already done, skipped')
                skipped += 1
            else:
                print(f'  + {html_file.name}: {count} badge(s) inserted')
                total_files += 1
                total_badges += count

    if dry_run:
        print(f'\nDry run complete. Pass no args to apply changes.')
    else:
        print(f'\nDone. {total_files} files modified, {total_badges} badges inserted, {skipped} already done.')


if __name__ == '__main__':
    main()
