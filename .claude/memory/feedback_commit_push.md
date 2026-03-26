---
name: feedback_commit_push
description: Always push to remote immediately after committing — do not wait for the user to ask
type: feedback
---

Always `git push` as part of the commit flow — never stop at `git commit` alone.

**Why:** The server deploys via `git pull` from the remote. If the commit isn't pushed, the server stays on the old version and the user has to notice and ask for the push separately.
**How to apply:** Whenever the user asks to "commit", treat it as commit + push in a single step. Use `git commit ... && git push` chained together.
