# Questions Index

Format: `Qyymmdd{G|C}q` — yy=year, mm=month, dd=day, G=George / C=Claude, q=question ref (a–z)

| ID        | Date       | Raised by | Question                                                              | Status   | Notes |
|-----------|------------|-----------|-----------------------------------------------------------------------|----------|-------|
| Q260324Ga | 2026-03-24 | George    | Should we index questions with Qyymmdd-q IDs?                        | Resolved | Adopted — this file |
| Q260324Gb | 2026-03-24 | George    | Should Claude maintain questions.md, and use G/C prefix to tag owner? | Resolved | Adopted — Claude maintains file; G=George, C=Claude |
| Q260324Gc | 2026-03-24 | George    | Once on the VM, can GitHub be removed as a third-party dependency?    | Resolved | Yes — VM becomes primary; GitHub kept as passive offsite mirror, pushed to automatically by cron |
| Q260324Gd | 2026-03-24 | George    | Can the diary skill be moved into the project dir instead of ~/.claude/skills? | Resolved | Done — moved to .claude/skills/ in repo; travels with git clone to any machine incl. VM |
| Q260324Ge | 2026-03-24 | George    | Should ClaudeBeat use a source whitelist, and should full autonomy (S3) wait until the editorial relationship is established? | Resolved | Whitelist created in notes/sources.md; SKILL.md updated to enforce it. Manual editorial workflow kept for now — S3 autonomy deferred until trust and content patterns are well established |
| Q260324Gf | 2026-03-24 | George    | When was Claude Code made public? | Open | Best recollection: research preview Feb 2025, GA May 2025 — needs verification against anthropic.com/news before treating as settled |
| Q260402Ga | 2026-04-02 | George    | Entry icons (✦) appearing instead of category icons (🧭/✅/💡) in some backfilled articles — why does this keep happening? | Open | Spotted in 2026-03-29; root cause: SKILL.md step 5 template uses ✦ but h2 icon should be category emoji; needs SKILL.md fix + audit of affected articles |
| Q260402Gb | 2026-04-02 | George    | Is using inshorts.com acceptable as a source? It aggregates from primary sources (e.g. newsbytesapp.com) making ClaudeBeat content third-hand. | Open | Agreed: inshorts.com must be excluded; sources.md to be updated; all future research must trace to Tier 1–2 primary sources only |
| Q260402Gc | 2026-04-02 | George    | VentureBeat covers nearly identical territory to ClaudeBeat — how do we differentiate and ensure we are not simply replicating their content? | Open | ClaudeBeat must go deeper, be more opinionated/practical, and not rely on VentureBeat as a source; editorial strategy response in PDF |
