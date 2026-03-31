---
name: sk-update-claudes-daily-diary
description: Check for missing diary days and backfill them, then append new entries to today's Claude Daily Diary HTML file and update index.html
---

You are executing the **sk-update-claudes-daily-diary** skill.

## Goal

1. Detect any days between the most recent diary entry and today that have no HTML file.
2. Backfill each missing day in chronological order (oldest first).
3. Add today's entry.

---

## Step 1 — Determine dates

Today's date is available in `CLAUDE.md` as `currentDate`.

Glob all `articles/**/20??-??-??.html` files and sort them.
The **most recent** existing file tells you the last covered date.

Path derivation: from a date string like `2026-03-21`, derive:
- `{yyyy}` = characters 1–4 → `2026`
- `{mm}` = characters 6–7 → `03`
- Archive path = `articles/{yyyy}/{mm}/{yyyy-mm-dd}.html`

Build a list of every calendar date from the day **after** the last covered date
up to and including today. Any date in that range without a corresponding
`.html` file is a **missing day** that needs backfilling.

Example: if the last file is `articles/2026/03/2026-03-17.html` and today is `2026-03-20`,
the missing days are `2026-03-18` and `2026-03-19`, and today is `2026-03-20`.

---

## Step 2 — Scan all existing entries (de-duplication list)

Before any research, read the `<h2>` titles from **all** existing
`articles/**/20??-??-??.html` files. Keep a running list of covered topics — every new
day's entries (backfill and today) must avoid repeating anything on this list.
Update the list after writing each day so the next day doesn't duplicate it.

---

## Step 2b — Source whitelist

Before researching, read `notes/sources.md` in the project root. This is the editorial
source whitelist. Abide by it strictly:

- **✅ Approved** — may be used freely; still cross-check significant claims against
  at least one other approved source before including
- **🔍 Provisional** — may be used if the content is solid; flag the source in the
  commit message for editorial review
- **❌ Excluded** — never use, regardless of how strong the story looks

**Content guardrails (always apply):**
1. No political commentary — report what happened *to* or *from* Anthropic; never editorially on political figures or governments
2. No speculation presented as fact — revenue estimates, valuations, IPO timelines must be clearly attributed and labelled as estimates
3. No culture-war adjacency — on ethics debates, present multiple perspectives; never take a side
4. Anthropic-relevance test — every entry must be directly about Claude, Anthropic, or AI development best practices

If a story feels uncertain or borderline, cross-check it across multiple approved sources.
If still uncertain, do not publish it — flag it in the summary for the editor's review.

---

## Step 3 — Backfill missing days (repeat for each missing date)

For each missing date, in chronological order (oldest first):

### 3a — Research for that specific date

Search the web for Claude/Anthropic news published **around that date**.
Use targeted queries such as:

- `anthropic claude news {yyyy-mm-dd}`
- `anthropic claude {month} {year} new features`
- `site:anthropic.com news {year}`
- `claude code updates {month} {year}`

Collect **2–4 distinct topics** not already on the covered-topics list.
Only use sources that are ✅ Approved or 🔍 Provisional in `notes/sources.md`.

### 3b — Create the missing day's file

Create `articles/{yyyy}/{mm}/{yyyy-mm-dd}.html` (the Write tool creates the directory
automatically). Copy the structure of the most recent existing file, updating:
- `<title>` to `{yyyy-mm-dd} – {Title} | Claude's Daily Diary`
- `<meta name="description">` accordingly
- Open Graph + Twitter Card tags (see block below) — update all URLs and image paths
- `<span class="date-badge">` to the missing date
- category badge (see below) immediately after the date-badge
- `<h1>` in `.article-header` to a title summarising the day's topics

**Open Graph / Twitter Card block** — insert immediately after `<meta name="description">`:

```html
  <meta property="og:type"        content="article">
  <meta property="og:site_name"   content="Claude's Daily Diary">
  <meta property="og:title"       content="{yyyy-mm-dd} – {Title}">
  <meta property="og:description" content="{same as meta description}">
  <meta property="og:url"         content="https://claudebeat.ai/articles/{yyyy}/{mm}/{yyyy-mm-dd}.html">
  <meta property="og:image"       content="https://claudebeat.ai/articles/{yyyy}/{mm}/{yyyy-mm-dd}.png">
  <meta name="twitter:card"       content="summary_large_image">
  <meta name="twitter:image"      content="https://claudebeat.ai/articles/{yyyy}/{mm}/{yyyy-mm-dd}.png">
```

**Category badge** — choose the one that best fits the day's primary content:

| Category | Key | Icon | Use when… |
|----------|-----|------|-----------|
| Daily News | `news` | 🧭 | Launches, partnerships, funding, platform announcements |
| Best Practices | `practice` | ✅ | Guides, architecture, governance, responsible-use frameworks |
| Tips 'n' Tricks | `tips` | 💡 | Specific techniques, shortcuts, developer productivity |

```html
<span class="cat-badge cat-{key}">{icon} {Label}</span>
```
e.g. `<span class="cat-badge cat-news">🧭 Daily News</span>`

All root-relative links inside the new file must use `../../../`:
- `href="../../../favicon.svg"`, `href="../../../styles.css"`, `href="../../../index.html"`

Also insert the teaser image reference **just before the first `<article class="entry">`** block:

```html
    <figure class="entry-teaser">
      <img src="{yyyy-mm-dd}.png" alt="{page title} — visual for {yyyy-mm-dd}">
    </figure>
```

(The image is in the same directory as the HTML, so no path prefix is needed.)

Append `<article class="entry">` blocks **before `</main>`** using the
entry template (see Step 5 below).

### 3c — Generate artist-style teaser image + thumbnail

Every new diary day gets a unique 1200×630 teaser image and a 96×96 thumbnail, each
**inspired by a specific historic artist** chosen to match the day's topics. The images
are generated in Python + Pillow and saved alongside the HTML.

#### Step 3c-i — Choose an artist

Pick one artist from the palette below whose visual language best echoes the day's themes.
No artist may be reused unless at least 8 other artists have appeared since their last use.

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

#### Step 3c-ii — Write the motif function

Open `generate_images.py` at the project root. Add a new function `img_{slug}_{date}()`
(e.g. `img_seurat_20260321()`) using Python + Pillow. Follow the patterns already in
the file:

```python
def img_seurat_20260321():
    """Georges Seurat pointillist style — data embeddings theme."""
    img = Image.new("RGB", (W, H), (12, 18, 45))   # deep navy bg

    # ... draw with ImageDraw, use layer()/comp() for alpha blending ...
    # Scatter thousands of tiny ellipses (r=3-7) in spectral colours
    # Build up forms (concentric density gradients, bright centre)

    return img
```

Key rules for every motif:
- Use **RGBA layers** (`layer()` + `comp()`) for any semi-transparent element
- Aim for **at least 4 distinct visual elements** (bg texture, large shape, medium details, scatter)
- Use the **full colour spectrum** — do not restrict yourself to the site's coral palette
- All randomness must use the module-level `rng = Random(42)` so images are deterministic

Then append the new entry to the `DAYS` list:

```python
DAYS = [
    ...existing entries...,
    ("{yyyy-mm-dd}", img_seurat_20260321, "{1-3 word keyword}", "Georges Seurat"),
]
```

#### Step 3c-iii — Run the generator

From the project root:

```
python generate_images.py
```

The script regenerates **all** entries in `DAYS`, so existing images are refreshed too
(they are deterministic, so they will be byte-identical). New files produced:
- `articles/{yyyy}/{mm}/{yyyy-mm-dd}.png` — 1200×630 teaser with artist badge overlay
- `articles/{yyyy}/{mm}/{yyyy-mm-dd}-thumb.png` — 96×96 center-crop thumbnail

The badge overlay (already handled by `add_badge()` in the script) places:
- Coral date pill (bottom-left)
- White bold 1-3 word keyword headline
- Cream small text: `"in the style of {Artist Name}"`

### 3e — Append to SEARCH_INDEX in index.html

After writing the new day's file, strip HTML tags from every `<article class="entry">` block you
just wrote (replace `<[^>]+>` with a space, collapse multiple spaces, trim). Then **prepend** a new
object to the `const SEARCH_INDEX = [...]` array in the `<script>` block near the bottom of
`index.html`, just before the first existing `{` (keeping newest-first order). Use this format:

```js
    {
      date: "{yyyy-mm-dd}", cat: "{key}",
      title: "{page h1 title}",
      url: "articles/{yyyy}/{mm}/{yyyy-mm-dd}.html",
      text: "{stripped plain text of all entry bodies, space-separated}"
    },
```
Where `{key}` is `"news"`, `"practice"`, or `"tips"` (matches the category badge chosen in Step 3b).

### 3f — Add to index.html article list

Prepend a `<li>` for the missing date **at the very top** of
`<ul class="article-list">` in `index.html` — but below any dates that are
more recent (i.e. maintain newest-first order):

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

### 3g — Update the covered-topics list

Add the newly written topics to the running de-duplication list before
moving on to the next missing date.

---

## Step 4 — Today's entry

After all backfill days are done, handle today (`currentDate`).

### 4a — Check if today is already published

Open `articles/{yyyy}/{mm}/{today}.html` (if it exists) and count the `<article class="entry">`
blocks already present.

- **If one or more entries exist:** today's diary is already published.
  Inform the user with a short message, e.g.:

  > Today's entry (`{yyyy-mm-dd}`) is already published with N entries
  > covering: {comma-separated topic titles}.
  > Any late-breaking news will be picked up in tomorrow's run. Nothing
  > further to do today.

  Then **stop** — do not research or append anything further.

- **If the file is missing or empty:** proceed to Step 4b.

### 4b — Research and write today's entry

1. **Research** — search for the latest Claude/Anthropic news not already
   on the covered-topics list. Collect 2–4 distinct topics.
2. **Create or open** `articles/{yyyy}/{mm}/{today}.html` — create it (copying
   the most recent file's structure) if it doesn't exist yet.
   All root-relative links must use `../../../` (favicon, styles, index).
3. **Insert teaser image reference** just before the first `<article class="entry">`:
   ```html
   <figure class="entry-teaser">
     <img src="{today}.png" alt="{page title} — visual for {today}">
   </figure>
   ```
4. **Append entries** before `</main>`.
5. **Generate artist-style image** — follow Step 3c exactly (choose artist, write motif
   function, add to `DAYS` list in `generate_images.py`, run `python generate_images.py`).
6. **Update SEARCH_INDEX** — strip HTML from the new entries and prepend a new object to
   the `SEARCH_INDEX` array in `index.html` (same format as Step 3e).
7. **Update index.html article list** — prepend a `<li>` at the top if today is not yet
   listed, including the `<img class="entry-thumb">` element (same format as Step 3f).

---

## Step 5 — Entry template

Use this structure for every entry (backfill and today):

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

## Done

Summarise what was added in a short plain-text response:
- List any backfilled days with their topics
- List today's new topics
- Note sources used
