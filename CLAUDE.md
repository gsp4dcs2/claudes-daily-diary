# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Claude's Daily Diary** — a static local HTML website documenting Claude/Anthropic best practices,
tips, and new features. Updated daily.

## Architecture

```
ws02_Claudes_Daily_Diary/
├── index.html          # Homepage — sorted article list (newest first)
├── styles.css          # All CSS — responsive, CSS custom properties
├── favicon.svg         # SVG favicon — coral starburst on dark brown (#2D1B0E)
├── CLAUDE.md           # This file
└── archives/
    └── {yyyy}/
        └── {mm}/
            └── {yyyy-mm-dd}.html  # One file per day; entries appended, never overwritten
```

No build step, no dependencies — pure HTML/CSS, open directly in a browser.

## Conventions

### Adding a new day's entries
1. Create `./archives/{yyyy}/{mm}/{yyyy-mm-dd}.html` (copy structure from the most recent day file). Use `../../../` for all root-relative links (`favicon.svg`, `styles.css`, `index.html`).
2. Prepend a new `<li>` with `href="archives/{yyyy}/{mm}/{yyyy-mm-dd}.html"` at the **top** of `<ul class="article-list">` in `index.html`.
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

`/sk-update-claudes-daily-diary` — detects any missing days since the last diary entry, backfills
them in chronological order, then appends entries for today. Updates `index.html` throughout.
Skill file: `~/.claude/skills/sk-update-claudes-daily-diary/SKILL.md` (local only — not in repo)

## Scheduling

The skill can be run:
- **Manually** — invoke `/sk-update-claudes-daily-diary` any time.
- **In-session cron** — via Claude Code's `CronCreate` tool (session-only, 3-day max).
- **Persistently** — via Windows Task Scheduler (runs even when Claude is closed).
