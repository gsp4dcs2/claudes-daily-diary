---
name: feedback_confirm_before_starting
description: Always confirm with the user before starting a task — don't interpret a short reply as an instruction to proceed
type: feedback
---

Don't interpret a short reply (like a number, "yes", "ok") as an instruction to immediately start work unless the context makes it unambiguous. When the user presents a list of options or tasks, confirm which one they want actioned before cracking on.

**Why:** User said "3" meaning they were giving feedback on item 3 of a conversation, not asking me to start task #3. I proceeded without checking and did a large batch operation the user hadn't explicitly requested.

**How to apply:** After presenting a task list or set of options, wait for a clear instruction like "do it", "go ahead", or "start on #1" before beginning work. A bare number or short acknowledgement is not sufficient authorisation.
