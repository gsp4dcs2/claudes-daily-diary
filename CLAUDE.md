# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Claude's Daily Diary** — a static local HTML website documenting Claude/Anthropic best practices,
tips, and new features. Updated daily.

## Architecture

```
ws02/
├── index.html          # Homepage — sorted article list (newest first)
├── styles.css          # All CSS — responsive, CSS custom properties
├── favicon.svg         # SVG favicon — coral starburst on dark brown (#2D1B0E)
├── {yyyy-mm-dd}.html   # One file per day; entries appended, never overwritten
└── CLAUDE.md           # This file
```

No build step, no dependencies — pure HTML/CSS, open directly in a browser.

## Conventions

### Adding a new day's entries
1. Create `./{yyyy-mm-dd}.html` (copy structure from the most recent day file — it already includes the favicon link).
2. Prepend a new `<li>` at the **top** of `<ul class="article-list">` in `index.html`.
3. Append `<article class="entry">` blocks **before `</main>`** — never overwrite existing entries.

### Entry structure
```html
<article class="entry">
  <h2><span class="entry-icon">✦</span> {Title}</h2>
  <p>…</p>
  <div class="tag-list"><span class="tag">{tag}</span></div>
</article>
```

### CSS classes to use
- `.entry` — article card
- `.callout` / `.callout.tip` / `.callout.warning` — highlighted boxes
- `.tag` / `.tag-list` — topic chips
- `pre > code` — code blocks (dark theme)
- `.date-badge` — date pill on article pages
- `.article-date` — date in index list

### Design tokens (defined in `styles.css :root`)
- Primary colour: `#E8734A` (coral)
- Max content width: `860px`
- Font: system stack; mono: SF Mono / Fira Code / Cascadia Code

## Skill

`/sk-update-claudes-daily-diary` — searches the web for new Claude features/best practices and
appends entries to today's HTML file, updating `index.html` as needed.
Skill file: `~/.claude/skills/sk-update-claudes-daily-diary/SKILL.md` (local only — not in repo)

## Scheduling

The skill can be run:
- **Manually** — invoke `/sk-update-claudes-daily-diary` any time.
- **In-session cron** — via Claude Code's `CronCreate` tool (session-only, 3-day max).
- **Persistently** — via Windows Task Scheduler (runs even when Claude is closed).
