# Month Navigator — Design Questions

Raised during brainstorm on 2026-03-27. Answer each before implementing.

---

## Q1 — Search interaction  ✅ ANSWERED
**Question:** When the user types in the search box, should it search across all months
(overriding the month filter), or only within the currently displayed month?

**Answer:** Search should be a separate **[Search] tab** in the nav, independent of the
month navigator. The nav would read: `[Home]  [<] March '26 [>]  [Search]`

- Home tab: month-filtered article list, controlled by `[<]` / `[>]`
- Search tab: full-text search across all articles, results listed in place
- The two modes are completely independent — no shared state needed

**Persistence note:** In-memory JS state is sufficient for the session. If we want the
selected month to survive a page refresh, one line of `sessionStorage` handles it
(nice-to-have, not required for v1).

---

## Q2 — Oldest month boundary  ✅ ANSWERED
**Question:** Should the `[<]` button go grey/inoperative when on the oldest available
month (currently January '26), mirroring the `[>]` behaviour on the current month?

**Answer:** Yes — both ends clamp. `[<]` disabled on oldest month, `[>]` disabled on current month.

---

## Q3 — Empty months  ✅ ANSWERED
**Question:** If a future gap month has no articles, should the navigator skip over it
silently, or land on it and show "No entries this month"?

**Answer:** Land on it and show: "No entries this month for now — please come back soon :)"
(Acknowledged this should never happen in practice given daily updates + backfill policy.)

---

## Q4 — Shareable URLs  ✅ ANSWERED
**Question:** Should navigating to Feb '26 update the URL (e.g. `?month=2026-02`) so
a specific month can be shared or bookmarked?

**Answer:** Yes — update the URL with `?month=2026-02` on every navigation. On page load,
read the param and open that month directly (e.g. for newsletter links dropping readers
into a specific month). Also handles the sessionStorage persistence from Q1 naturally.

---

## Q5 — Page scroll on navigation  ✅ ANSWERED
**Question:** When clicking `[<]` or `[>]`, should the page scroll back to the top of
the article list automatically?

**Answer:** Yes — scroll to top on month change. Additionally, remember each month's
scroll position so returning to a previously visited month restores where the user left off.

**Storage:** sessionStorage keyed by month (`scroll_2026-03 = 1840`) — persists within
the tab session but resets on fresh visit. Avoids stale-position issues from new articles
being added. (localStorage considered but rejected — too persistent, risks confusion.)

**Flow:**
1. User scrolls down in March '26
2. Clicks [<] to go to Feb '26 — saves March scroll pos, scrolls Feb to top (or saved pos if visited before)
3. Clicks [>] back to March '26 — restores saved scroll position

---

## TODO — Revisit before v2
- **sessionStorage vs localStorage for scroll position**: currently using sessionStorage
  (resets on fresh tab). If the user prefers scroll memory to survive across separate
  visits/days, switch to localStorage — but risk of stale position if new articles are
  added above where they last were. Confirm preference before changing.

---

## Implementation notes (accumulating)

- Nav layout: `[Home]  [<] March '26 [>]  [Search]`
- Month filter: pure JS, reads `.article-date` spans from existing DOM
- No server-side changes needed
- Search tab replaces current inline search box on homepage
