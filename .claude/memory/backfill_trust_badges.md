---
name: backfill_trust_badges
description: REMINDER — retrospectively add ⭐⭐⭐/⭐⭐/⭐ trust badges to all existing articles (only 2026-04-01 and 2026-04-02 have them so far)
type: project
---

All articles from 2025-12-11 through 2026-03-31 are missing the source trust badge treatment added on 2026-04-02.

**Why:** The `.source-line` / `.trust-badge` / `.trust-legend` CSS and HTML pattern was introduced on 2026-04-02. Only the two most recent articles (2026-04-01, 2026-04-02) have been manually updated. All earlier articles need the same treatment applied retrospectively.

**How to apply:** For each existing article:
1. Parse the `Source:` URL from the HTML comment above each `<article>` block
2. Map the domain to its tier in `notes/sources.md` → choose ⭐⭐⭐ / ⭐⭐ / ⭐
3. Insert `<div class="source-line">` block before each `<div class="tag-list">`
4. Insert `<div class="trust-legend">` once per page just before `</main>`

**Scale:** ~113 articles × ~3 entries each = ~340 source-line insertions. Needs a scripted approach — write a Python script to do the bulk edit rather than manual edits.

**Status:** NOT DONE — remind the user at the start of every session until completed.
