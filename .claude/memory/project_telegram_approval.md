---
name: project_telegram_approval
description: Telegram bot editorial approval workflow — current build state, credentials, and exact next step
type: project
---

The user has chosen Option C — Telegram bot — as the editorial approval mechanism for the fully autonomous diary cron job.

**Why:** When the cron job runs at 07:00 daily, Claude writes the day's content and sends a Telegram message per entry with [✅ Include] [❌ Skip] buttons. The user taps from their phone. On final Publish, content is committed and pushed live. On Discard, draft is discarded.

---

## Current state (end of session 2026-04-03)

### ✅ Done
- Telegram installed on phone, account created as "TeleClaude"
- Bot created via @BotFather: **claudebeat_editor_bot**
- Bot token: `8633455378:AAENHCKKt4nT9z8K6L9tKOyf5iY3s6a8Ups`
- Chat ID: `8613239362`
- python-telegram-bot v22.7 installed at `~/claudebeat-venv/`
- Credentials file at `~/claudebeat-approve.env` (chmod 600)
- `scripts/claudebeat-approve.py` — per-entry approval script (in repo)
- `scripts/run-diary.sh` — cron wrapper (in repo), working correctly
- Claude Code CLI v2.1.91 installed and authenticated on VM
- Full end-to-end test run completed successfully (2026-04-03 diary written and published)
- SKILL.md updated with CRITICAL block: **never run git add/commit/push** — approval script handles all git ops
- Telegram per-entry buttons confirmed working (screenshot received in previous session)

### ❌ Still to do
1. **Cron job** — not yet set up on VM. Command to add:
   ```
   crontab -e
   ```
   Add line:
   ```
   0 7 * * * /var/www/claudebeat/scripts/run-diary.sh >> /var/log/claudebeat.log 2>&1
   ```
2. **Telegram approval test** — not completed this session. Planned test:
   append a dummy entry to today's article, run `~/claudebeat-venv/bin/python3 scripts/claudebeat-approve.py` directly, verify Telegram buttons appear and Include/Skip/Publish flow works end-to-end, then `git restore` to clean up.

### 🔜 Next session — start here
1. Run the Telegram approval test (see above)
2. Set up the cron job
3. Watch 07:00 UTC run the following morning

---

## Key fixes made this session

- `run-diary.sh` SKILL variable: changed `cat` to `awk` to strip YAML frontmatter before passing to `claude -p`
- `run-diary.sh` approve script path: changed `~/claudebeat-approve.py` → `scripts/claudebeat-approve.py`
- SKILL.md: added CRITICAL block forbidding git commit/push during skill execution

## Known git sync issue (Windows ↔ VM)

The VM commits when it runs the skill. Windows then can't push without pulling first.
Standard workflow when push is rejected on Windows:
```
git stash
git pull --rebase
git stash pop
git push
```

---

## VM environment
- OS: Ubuntu 24.04 LTS
- Repo: `/var/www/claudebeat`
- Python venv: `~/claudebeat-venv/`
- python-telegram-bot: v22.7
- Credentials: `~/claudebeat-approve.env`
- Claude Code CLI: v2.1.91, authenticated
- Git author: configured (`git config --global user.email/user.name`)
- Git safe directory: configured (`git config --global --add safe.directory /var/www/claudebeat`)
- Repo ownership: `claude:claude` on `/var/www/claudebeat`

## Cron wrapper: scripts/run-diary.sh
```bash
#!/bin/bash
set -e
cd /var/www/claudebeat
echo "=== ClaudeBeat diary run: $(date) ==="
SKILL=$(awk '/^---$/{n++; if(n==2){found=1; next}} found{print}' .claude/skills/sk-update-claudes-daily-diary/SKILL.md)
claude --dangerously-skip-permissions -p "$SKILL"
echo "--- Skill complete. Running Telegram approval ---"
~/claudebeat-venv/bin/python3 scripts/claudebeat-approve.py
echo "=== Done: $(date) ==="
```
