---
name: feedback_nav_behaviour
description: Rules governing nav-bar state management — the golden rule, search persistence, month label, and acceptable UX trade-offs
type: feedback
---

The golden rule: **only the user changes anything on the nav-bar.** Never auto-update nav state as a side-effect of page load or internal rendering.

**Why:** Earlier bugs caused the month label to jump to an article's own month and search mode to auto-activate from stale sessionStorage. Both were caused by code writing nav state as a side-effect.

**How to apply:**
- `last_browse_month` is written ONLY in `goMonth()`, `btnMonthLabel` click, and `btnHome` click — never in `renderMonth()`
- Search mode on init triggers ONLY from `?search=1` or `?sq=` URL params — never from `sessionStorage.search_query` alone
- Article pages read `?from_month=` URL param as primary source for `ctxYM`, falling back to sessionStorage then `artYM`
- Search result links in `runSearch()` must pass `&from_month=${currentMonth}` so article pages know the browsed month

**Acceptable UX trade-off confirmed by user (2026-03-27):**
Navigating months from an article page (via `[<]` or `[>]`) clears the search text on arrival at the month view. This is intentional — the user made a deliberate navigation choice and arriving in clean browse mode is correct.
