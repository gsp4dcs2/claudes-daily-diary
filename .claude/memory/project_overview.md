---
name: project_overview
description: Full current state of the Claude's Daily Diary / claudebeat.ai project — architecture, features, files, conventions, and deployment plan
type: project
---

## What this project is

**Claude's Daily Diary** (publishing as **claudebeat.ai**) — a static HTML website covering
Claude/Anthropic news, best practices, tips, and new features. Updated daily via an automated
skill. Goal: the go-to independent developer publication for Claude news, funded by SEO + ads.

**Why:** User registered claudebeat.ai ($179.96 / 2 years via Namecheap, ~2027 expiry) to turn
this into a real public publication that covers its own costs through display advertising.

---

## Repository

`D:\Tresorit\z_Keepass\GSP\AI\Claude\ws02_Claudes_Daily_Diary`

---

## Key files

| File | Purpose |
|------|---------|
| `index.html` | Homepage — article list (newest-first) + live search + `SEARCH_INDEX` script block |
| `styles.css` | All CSS including search, teaser image, and thumbnail rules |
| `generate_images.py` | Python + Pillow — generates artist-style 1200×630 teasers + 96×96 thumbs |
| `favicon.svg` | Coral starburst SVG favicon |
| `articles/2026/03/{date}.html` | Daily diary pages |
| `articles/2026/03/{date}.png` | 1200×630 artist-style teaser per day |
| `articles/2026/03/{date}-thumb.png` | 96×96 index thumbnail per day |
| `CLAUDE.md` | Full project conventions, architecture, deployment notes |
| `.claude/skills/sk-update-claudes-daily-diary/SKILL.md` | Skill file — project-level, travels with the repo |
| `.claude/memory/` | Project-local memories — synced via Tresorit across all machines |

---

## Features built

1. **Live full-text search** — inline `SEARCH_INDEX` JS in index.html, filters as you type, shows body-text snippets
2. **Artist-style teaser images** — each day has a unique 1200×630 image inspired by a historic artist
3. **Index thumbnails** — 96×96 center-crop shown left of every list item in index.html
4. **Automated skill** `/sk-update-claudes-daily-diary` — researches news, writes HTML, generates artist image, updates index + SEARCH_INDEX
5. **Artist palette** — 15 artists documented in SKILL.md Step 3c with topic-matching guidance

---

## Design tokens

- Primary: `#E8734A` (coral) · Background: `#F7F6F3` · Surface: `#FFFFFF`
- Max width: `860px` · Font: system stack · Mono: SF Mono / Fira Code

---

## Deployment — IN PROGRESS

- **S1 ✅** VM clones from GitHub. Local skill runs → commits → pushes to GitHub → manual `git pull` on VM deploys.
- **S2 ✅** DNS A records set. Certbot installed. HTTPS live at claudebeat.ai.
- **S3 ❌ PENDING** Install Claude Code CLI on VM, set Anthropic API key, set up cron job.

**How to apply:** When picking up S3, install Node.js + Claude Code CLI on VM, set API key, add cron:
`0 7 * * * cd /var/www/claudebeat && claude -p "/sk-update-claudes-daily-diary"`
