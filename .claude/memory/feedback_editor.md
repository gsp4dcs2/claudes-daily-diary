---
name: feedback_editor
description: Use nano (not vi) for command-line editing on the VM
type: feedback
---

Always suggest `nano` for any command-line file editing on the VM.

**Why:** vi has terminal compatibility issues when SSH'd from the user's machine (raw escape codes displayed). Nano works cleanly.
**How to apply:** Any time I give a command that opens an editor on the VM, use `nano`.
