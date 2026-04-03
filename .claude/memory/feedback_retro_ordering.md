---
name: feedback_retro_ordering
description: Retrospective entries in index.html must be in strict continuous newest-first order within the retro block — never insert older entries above newer ones
type: feedback
---

The retrospective `<ul>` block in `index.html` (below `<!-- Retrospective entries below -->`) must maintain **strict newest-first order across the entire block**. When adding older backfill entries, insert them BELOW any existing retro entries that are newer — never above them.

**Why:** The JS month filter reads `<li>` items in DOM order. If Dec 01–03 are above Dec 04–10, the browser shows them between Dec 10 and Dec 11, breaking the month view. Discovered 2026-04-03 when Dec 01–03 appeared between Dec 10 and Dec 11 in the Dec 2025 month view.

**How to apply:**
- Before inserting retro entries, identify where in the retro block the new dates belong chronologically.
- Entries newer than existing retro items → insert above them (closer to the `<!-- Future entries -->` marker).
- Entries older than existing retro items → insert below them (closer to the closing `</ul>`).
- After any retro insertion, verify the full retro block reads newest → oldest top to bottom.
- The rule is: the entire retro block must be one contiguous newest-first sequence, not two separate sub-sequences.
