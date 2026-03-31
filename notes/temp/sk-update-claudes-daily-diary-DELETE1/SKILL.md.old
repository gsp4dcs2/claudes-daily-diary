---
name: sk-update-claudes-daily-diary
description: Research latest Claude/Anthropic features and best practices, then append new entries to today's Claude Daily Diary HTML file and update index.html
---

You are executing the **sk-update-claudes-daily-diary** skill.

## Goal

Research the latest Claude / Anthropic best practices and new features, then
append a new `<article class="entry">` block to today's daily diary page.

---

## Step 1 — Determine today's file

Today's date is available in `CLAUDE.md` as `currentDate`. The target file is:

```
./{yyyy-mm-dd}.html
```

in the workspace root (the directory where this project's `CLAUDE.md` lives).

---

## Step 2 — Research (web search)

Search the internet for **recent** Claude / Anthropic news and best practices.
Use queries such as:

- `site:anthropic.com claude new features 2025 2026`
- `claude.ai best practices prompting latest`
- `anthropic claude API updates`
- `claude code tips tricks`

Trusted sources to prefer (in order):
1. `docs.anthropic.com`
2. `anthropic.com/news`
3. `claude.ai` release notes / changelog
4. Well-regarded tech publications (e.g. Simon Willison's blog, Hacker News top threads about Claude)

Collect **2–4 distinct topics** that are new or meaningfully updated since the
last diary entry. Avoid duplicating topics already covered in existing
`{yyyy-mm-dd}.html` files in the workspace.

---

## Step 3 — Check existing entries

Read today's `./{yyyy-mm-dd}.html` file (if it exists).
Scan the `<article class="entry">` blocks for already-covered topics.
Only write entries for topics **not yet documented**.

---

## Step 4 — Append new entries

For each new topic, append an `<article class="entry">` block **before the
closing `</main>` tag** in today's HTML file.

### Entry template

```html
<!-- ═══════════════════════════════════════════════════════
     ENTRY N — {Topic Title}
     Source: {URL used}
     ═══════════════════════════════════════════════════════ -->
<article class="entry">
  <h2><span class="entry-icon">✦</span> {Topic Title}</h2>

  <p>{One-paragraph summary of the new feature or best practice.}</p>

  <h3>{Sub-heading if needed}</h3>
  <ul>
    <li>{Key point 1}</li>
    <li>{Key point 2}</li>
  </ul>

  <!-- Optional: callout, code block, etc. using existing CSS classes -->

  <div class="tag-list">
    <span class="tag">{tag1}</span>
    <span class="tag">{tag2}</span>
  </div>
</article>
```

Rules:
- Keep each entry focused (200–400 words of readable prose + lists).
- Link to the source in an HTML comment above the `<article>` tag.
- Use existing CSS classes: `.callout`, `.callout.tip`, `.callout.warning`,
  `<pre><code>`, `.tag-list`, `.tag`.
- Do **not** overwrite existing content — only append.

---

## Step 5 — Update index.html (if today's entry is new)

If today's date is **not yet listed** in `index.html`, prepend a new `<li>`
**at the very top of** the `<ul class="article-list">` list:

```html
<li>
  <a href="{yyyy-mm-dd}.html">
    <span class="article-date">{yyyy-mm-dd}</span>
    <span class="article-title">{Short title summarising today's updates}</span>
    <span class="article-arrow" aria-hidden="true">→</span>
  </a>
</li>
```

---

## Step 6 — Create today's file if it does not exist

If `./{yyyy-mm-dd}.html` does not yet exist, create it by copying the structure
of the most recent existing `{yyyy-mm-dd}.html` file, updating:
- `<title>` to `{yyyy-mm-dd} – {Title} | Claude's Daily Diary`
- `<meta name="description">` accordingly
- `<span class="date-badge">` to today's date
- `<h1>` in `.article-header` to the new day's title

Then append entries as per Step 4.

---

## Done

Summarise what was added (topics + sources) in a short plain-text response
to the user.
