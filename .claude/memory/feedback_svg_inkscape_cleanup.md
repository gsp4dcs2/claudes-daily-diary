---
name: Strip Inkscape bloat from SVG files
description: When the user sends SVG files exported from Inkscape, always strip metadata bloat before using them
type: feedback
---

Always strip Inkscape metadata from any SVG the user provides before committing or using it in the project.

**Why:** Inkscape exports include large amounts of non-visual bloat — `sodipodi:namedview`, `inkscape:*` attributes, `xmlns:inkscape`, `xmlns:sodipodi` namespaces, editor window state, zoom/pan position, etc. This inflates file size significantly (e.g. 130 lines → 13 lines) with zero visual benefit.

**How to apply:** When an SVG arrives from the user, clean it down to the essential visual elements only:
- Remove `sodipodi:*` and `inkscape:*` elements and attributes
- Remove unused namespace declarations (`xmlns:inkscape`, `xmlns:sodipodi`, `xmlns:svg`)
- Remove `<?xml ...?>` processing instruction (optional for inline/img use)
- Keep only `viewBox`, `fill`, `xmlns`, and visual elements
- Do this before writing to disk, committing, or bulk-replacing into HTML files
