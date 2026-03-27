---
name: sk-backfill-claudebeat
description: Retrospectively backfill ClaudeBeat diary articles from a given start date up to (but not including) the earliest existing article. All entries are tagged 'retrospective' and contain no knowledge of events after their entry date.
---

You are executing the **sk-backfill-claudebeat** skill.

Invocation format: `/sk-backfill-claudebeat {yyyy-mm-dd}`

The argument `{yyyy-mm-dd}` is the **earliest date to backfill to** — the oldest article
that will be created. All dates from this date up to (but not including) the earliest
existing article will be filled in.

---

## Goal

1. Identify the earliest existing article date — that is where backfilling stops.
2. Build a list of every calendar date from `{from-date}` up to the day before the
   earliest existing article.
3. For each date in that range (oldest first), research, write, and publish one
   retrospective diary article.
4. Update `index.html` (article list + SEARCH_INDEX) after each day is written.

---

## Step 1 — Determine the date range

Glob all `articles/**/20??-??-??.html` files and sort them ascending.
The **first** (oldest) file tells you the stop-before date.

Example: if the oldest file is `articles/2026/03/2026-03-10.html` and the argument
is `2026-03-07`, the dates to fill are `2026-03-07`, `2026-03-08`, `2026-03-09`.

Path derivation: from `2026-03-07`:
- `{yyyy}` = `2026`
- `{mm}` = `03`
- File path = `articles/2026/03/2026-03-07.html`

**If there are no dates in the range** (e.g. the argument equals the earliest existing
date), stop immediately and inform the user: no dates to backfill.

---

## Step 2 — Scan all existing entries (de-duplication list)

Read the `<h2>` titles from **all** existing `articles/**/20??-??-??.html` files.
Keep a running de-duplication list — every new entry must avoid repeating any topic
already on this list. Update the list after writing each day.

---

## Step 2b — Source whitelist

Read `notes/sources.md`. Abide by it strictly:

- **✅ Approved** — use freely; still cross-check significant claims against at least
  one other approved source before publishing
- **🔍 Provisional** — may use if content is solid; flag in commit message
- **❌ Excluded** — never use

**Content guardrails (always apply):**
1. No political commentary — report what happened *to* or *from* Anthropic; never
   editorially on political figures or governments
2. No speculation presented as fact — estimates, valuations, timelines must be
   attributed and labelled as estimates
3. No culture-war adjacency — present multiple perspectives on ethics debates; never
   take a side
4. Anthropic-relevance test — every entry must be directly about Claude, Anthropic,
   or AI development best practices

If a story is uncertain or borderline, cross-check it. If still uncertain, skip it
and flag it in the final summary for the editor's review.

---

## Step 3 — The no-future-knowledge rule (CRITICAL)

Every retrospective article must be written **as if on that date** — with no knowledge
of anything that happened after it.

Specifically:
- **Do not reference future events.** If covering 2026-02-15, do not mention anything
  announced after 2026-02-15.
- **Use present tense for that date.** Write "Anthropic *has* announced…", not
  "Anthropic *had* announced…"
- **Do not hint at outcomes.** If a lawsuit was filed on the entry date, do not say
  "which would later be resolved by…"
- **Research accordingly.** When searching for news, use date-bounded queries and
  discard any sources that post-date the entry.

---

## Step 4 — For each date in the range (oldest first)

### 4a — Research

Search for Claude/Anthropic news published **on or around that specific date**.
Use targeted queries such as:

- `anthropic claude news {yyyy-mm-dd}`
- `anthropic claude {month} {year}`
- `site:anthropic.com {year}`
- `claude code {month} {year} release`

Collect **2–4 distinct topics** not already on the de-duplication list.
Only use ✅ Approved or 🔍 Provisional sources from `notes/sources.md`.
Discard any source or claim that post-dates the entry date.

### 4b — Create the article file

Create `articles/{yyyy}/{mm}/{yyyy-mm-dd}.html`. Copy the structure of the nearest
existing article, updating:
- `<title>` → `{yyyy-mm-dd} – {Title} | Claude's Daily Diary`
- `<meta name="description">` accordingly
- `<span class="date-badge">` → the entry date
- category badge immediately after the date-badge (see category table in CLAUDE.md)
  e.g. `<span class="cat-badge cat-news">🧭 Daily News</span>` — most retrospective days are `news`
- `<h1>` in `.article-header` → a title summarising the day's topics

All root-relative links must use `../../../`:
`href="../../../favicon.svg"`, `href="../../../styles.css"`, `href="../../../index.html"`

Insert the teaser image reference **just before the first `<article class="entry">`**:

```html
    <figure class="entry-teaser">
      <img src="{yyyy-mm-dd}.png" alt="{page title} — visual for {yyyy-mm-dd}">
    </figure>
```

Append `<article class="entry">` blocks **before `</main>`** using the entry template
in Step 7 below. Every entry **must** include `<span class="tag">retrospective</span>`
in its tag list.

### 4c — Choose an artist and generate the teaser image

Check `generate_images.py`'s `DAYS` list to see which artists have already been used
and in what order. No artist may be reused unless at least 8 other artists have
appeared since their last use.

Pick one artist from the palette below whose visual language best echoes the day's themes:

| Artist | Style cues | Best-fit diary topics |
|--------|-----------|----------------------|
| **Wassily Kandinsky** | Bold primaries, diagonal grid, circles + triangles + arcs, prussian-blue bg | Prompting, composition, reasoning |
| **Piet Mondrian** | Off-white bg, yellow grid bands, red/blue rectangles, black lines | Context windows, grids, structured data |
| **Giacomo Balla** (Futurism) | Near-black bg, radiating coloured planes from VP, motion lines | Fast Mode, speed, latency, throughput |
| **Gustav Klimt** | Very dark bg, dense gold spirals + mosaic fragments, teal/rust accents | Models, craftsmanship, constitution, ethics |
| **Paul Klee** | Warm→cool colour grid cells, dark grid lines, white node circles | Agent networks, cells, multi-agent coordination |
| **Robert Delaunay** | Dark bg, large overlapping spectral-ring discs, full rainbow | Dispatch, signals, radio, cross-device, voice |
| **Joan Miró** | Deep-indigo bg, bold biomorphic blobs in primaries, black outlines, stars | /loop, cycles, playful automation, marketplace |
| **Kazimir Malevich** | Cream bg, bold tilted geometric shapes (black, red, navy, yellow) | Security, safety, absolutes, pure structure |
| **Georges Seurat** (Pointillism) | Dark/mid bg, thousands of tiny coloured dots building forms | Token counts, data density, embeddings, analytics |
| **Fernand Léger** | Dark bg, bold mechanical outlines, flat primaries, industrial shapes | APIs, infrastructure, computer use, hardware |
| **El Lissitzky** (Constructivism) | White/cream bg, bold red + black geometric bars at angles, sans-serif | Developer platform, tooling, CLI, structured outputs |
| **László Moholy-Nagy** (Bauhaus) | Transparent overlapping circles + rectangles, primary colours on white | Transparency, trust, memory, open-source |
| **Franz Marc** | Rich jewel-toned bg (cobalt, emerald), stylised animal/nature shapes | AI wellbeing, safety, consciousness, alignment |
| **Alexander Calder** | White bg, primary-coloured flat shapes on thin black lines | Adaptive thinking, flexible agents, balance |
| **Mark Rothko** (Colour Field) | Two or three hazy soft-edged colour bands, luminous edges | Long-running agents, context depth, compaction |

Write a new motif function `img_{slug}_{date}()` in `generate_images.py` following the
existing patterns (use `layer()` + `comp()` for RGBA compositing, `rng = Random(42)`
for determinism, at least 4 distinct visual elements).

Insert the new entry into the `DAYS` list **in chronological order** (backfill entries
go before the existing ones):

```python
DAYS = [
    ("{yyyy-mm-dd}", img_fn, "{1-3 word keyword}", "{Artist Name}"),
    ...existing entries...,
]
```

Then run:
```
python generate_images.py
```

New files produced:
- `articles/{yyyy}/{mm}/{yyyy-mm-dd}.png`
- `articles/{yyyy}/{mm}/{yyyy-mm-dd}-thumb.png`

### 4d — Append to the article list in index.html

Retrospective entries go at the **bottom** of `<ul class="article-list">` — below all
existing entries, maintaining oldest-last order. Insert above the
`<!-- Future entries will be prepended above this comment -->` marker but below any
`<!-- Retrospective entries below -->` comment (add that comment if it doesn't exist).

```html
<li>
  <a href="articles/{yyyy}/{mm}/{yyyy-mm-dd}.html">
    <img class="entry-thumb" src="articles/{yyyy}/{mm}/{yyyy-mm-dd}-thumb.png" alt="{yyyy-mm-dd} thumbnail">
    <span class="article-date">{yyyy-mm-dd}</span>
    <span class="cat-icon" title="{Label}">{icon}</span>
    <span class="article-title">{Short title}</span>
    <span class="article-arrow" aria-hidden="true">→</span>
  </a>
</li>
```

When writing multiple retrospective dates in one run, insert them in **newest-first
order** within the retrospective block (so 03-09 appears above 03-08 above 03-07).

### 4e — Append to SEARCH_INDEX in index.html

Retrospective entries go at the **end** of the `const SEARCH_INDEX = [...]` array —
after all existing entries. Strip HTML tags from the entry bodies for the `text` field.

```js
    {
      date: "{yyyy-mm-dd}", cat: "{key}",
      title: "{page h1 title}",
      url: "articles/{yyyy}/{mm}/{yyyy-mm-dd}.html",
      text: "{stripped plain text of all entry bodies, space-separated}"
    },
```
Where `{key}` is `"news"`, `"practice"`, or `"tips"` (matches the category badge).

When writing multiple dates in one run, insert them in **newest-first order** at the
end of the array (so 03-09 appears before 03-08 before 03-07 at the tail).

### 4f — Update the de-duplication list

Add the newly written topics before moving to the next date.

---

## Step 5 — Commit after all dates are written

Stage and commit all new/modified files:
- `articles/{yyyy}/{mm}/{yyyy-mm-dd}.html` (one per new date)
- `articles/{yyyy}/{mm}/{yyyy-mm-dd}.png` (one per new date)
- `articles/{yyyy}/{mm}/{yyyy-mm-dd}-thumb.png` (one per new date)
- `generate_images.py`
- `index.html`

Commit message format:
```
Add retrospective diary entries for {date-range}

{Brief summary of dates and topics covered}

Provisional sources used (if any): {list}

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

Then push to GitHub. The editor will pull on the VM once reviewed.

---

## Step 6 — Entry template

```html
<!-- ═══════════════════════════════════════════════════════
     ENTRY N — {Topic Title}
     Source: {URL used}
     ═══════════════════════════════════════════════════════ -->
<article class="entry">
  <h2><span class="entry-icon">✦</span> {Topic Title}</h2>

  <p>{One-paragraph summary, written as if on the entry date — no future knowledge.}</p>

  <h3>{Sub-heading if needed}</h3>
  <ul>
    <li>{Key point 1}</li>
    <li>{Key point 2}</li>
  </ul>

  <!-- Optional: .callout, .callout.tip, .callout.warning, pre>code -->

  <div class="tag-list">
    <span class="tag">{tag1}</span>
    <span class="tag">{tag2}</span>
    <span class="tag">retrospective</span>
  </div>
</article>
```

Rules:
- Every entry **must** carry `<span class="tag">retrospective</span>`
- 200–400 words of readable prose + lists per entry
- Source URL in HTML comment above `<article>`
- No future knowledge — write as if on the entry date
- Do not overwrite existing content

---

## Done

Summarise what was written:
- Date range covered
- Topics per day
- Artists used
- Any provisional sources flagged for editor review
- Any stories skipped due to uncertainty (flag for editor)
