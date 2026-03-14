# Claude's Daily Diary

**A daily log of Claude / Anthropic best practices, new features, and tips — published as a lightweight static website.**

🌐 **Live site:** https://gsp4dcs2.github.io/claudes-daily-diary/

---

## What is this?

Claude's Daily Diary is a personal knowledge base, published openly, that tracks the rapidly evolving world of [Claude](https://claude.ai) — Anthropic's AI assistant. Each day's entry covers newly released features, updated best practices, prompt-engineering techniques, and API developments.

The goal is simple: make it easier to stay current with Claude without having to wade through release notes, blog posts, and documentation every day.

---

## Content & Sources

Every entry is researched using live web search and grounded in authoritative sources. The primary sources used, in order of preference:

| Source | What it covers |
|--------|---------------|
| [docs.anthropic.com](https://docs.anthropic.com) | Official API docs, release notes, model guides |
| [anthropic.com/news](https://www.anthropic.com/news) | Product announcements and research publications |
| [code.claude.com/docs](https://code.claude.com/docs) | Claude Code CLI documentation and best practices |
| [claude.ai](https://claude.ai) | Consumer-facing release notes and changelog |
| [Simon Willison's blog](https://simonwillison.net) | Well-regarded independent analysis and commentary |
| Hacker News | Community discussion of significant Claude/Anthropic news |

Each article entry includes an HTML comment citing the specific URL it was sourced from, so you can always trace a claim back to its origin.

> **Transparency note:** Entries are researched and written with the assistance of [Claude Code](https://claude.ai/code) (Anthropic's official CLI), which performs the web searches, synthesises the findings, and formats the HTML. All content is reviewed for accuracy and grounded in the primary sources listed above — no hallucinated features or made-up release dates.

---

## Site structure

```
/
├── index.html          # Homepage — article list, newest first
├── styles.css          # All styling — responsive, no frameworks
├── favicon.svg         # Claude starburst logo mark
├── CLAUDE.md           # Instructions for Claude Code (the AI editor)
└── {yyyy-mm-dd}.html   # One file per day; entries appended, never overwritten
```

Pure HTML and CSS — no build step, no JavaScript framework, no dependencies. Opens directly in any browser.

---

## How it's updated

A custom Claude Code skill (`/sk-update-claudes-daily-diary`) runs the following workflow:

1. **Searches** the web for recent Claude / Anthropic news using the sources above
2. **Checks** existing entries to avoid duplicates
3. **Writes** new `<article>` blocks into today's HTML file
4. **Updates** `index.html` with a link to the new day's page
5. **Commits and pushes** to this repo, triggering a GitHub Pages deployment

Updates typically go live within 60 seconds of a push.

---

## Disclaimer

This is an independent personal project and is **not affiliated with, endorsed by, or sponsored by Anthropic**. All trademarks (Claude, Anthropic) belong to their respective owners. Content is provided for informational purposes; always refer to the [official Anthropic documentation](https://docs.anthropic.com) for authoritative guidance.
