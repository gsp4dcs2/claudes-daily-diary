---
name: project_telegram_approval
description: Telegram bot editorial approval workflow — current build state, credentials, and exact next step
type: project
---

The user has chosen Option C — Telegram bot — as the editorial approval mechanism for the fully autonomous diary cron job.

**Why:** When the cron job runs at 07:00 daily, Claude writes the day's content and sends a summary to a private Telegram bot. The user taps Approve or Reject from their phone. On Approve, the content is committed and pushed live on the VM. On Reject, the draft is discarded.

---

## Current state (end of session 2026-04-02)

### ✅ Done
- Telegram installed on phone, account created as "TeleClaude"
- Bot created via @BotFather: **claudebeat_editor_bot**
- Bot token: `8633455378:AAENHCKKt4nT9z8K6L9tKOyf5iY3s6a8Ups`
- Chat ID: `8613239362`
- python-telegram-bot v22.7 installed at `~/claudebeat-venv/`
- Credentials file created at `~/claudebeat-approve.env` (chmod 600)

### ❌ Stuck at
A simple "hello world" Telegram message test failed — no message arrived on phone and no error was shown. Root cause unknown — most likely one of:
1. The bot hasn't been properly started by the user (need to open `t.me/claudebeat_editor_bot` and tap Start)
2. A network/firewall issue on the VM blocking outbound HTTPS to Telegram's API
3. The test script silently failed

### 🔜 Next session — start here
Run this diagnostic to get a clear error message:
```bash
~/claudebeat-venv/bin/python3 -c "
import asyncio
from telegram import Bot

async def test():
    async with Bot('8633455378:AAENHCKKt4nT9z8K6L9tKOyf5iY3s6a8Ups') as bot:
        info = await bot.get_me()
        print('Bot name:', info.first_name)
        await bot.send_message(chat_id=8613239362, text='ClaudeBeat bot alive!')
        print('Message sent!')

asyncio.run(test())
"
```

If `get_me()` fails → token or network issue.
If `get_me()` succeeds but send fails → chat_id issue (user hasn't started the bot).

Also verify the user has opened `t.me/claudebeat_editor_bot` on their phone and tapped **Start**.

---

## What still needs to be built (next session onwards)

### 1. Credentials file (already done)
`~/claudebeat-approve.env` contains TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.

### 2. Approval script to write: `~/claudebeat-approve.py`
Logic:
1. Read today's new article from `/var/www/claudebeat/articles/yyyy/mm/yyyy-mm-dd.html`
2. Extract title + entry headlines
3. Send Telegram message with ✅ Approve / ❌ Reject inline buttons
4. Poll for response (timeout 8 hours → auto-approve)
5. On approve: `cd /var/www/claudebeat && git add -A && git commit && git push && git pull`
6. On reject: discard changes, notify user

### 3. Cron job
Use the wrapper script (avoids quoting issues, logs output):
```
0 7 * * * /var/www/claudebeat/scripts/run-diary.sh >> /var/log/claudebeat.log 2>&1
```

`scripts/run-diary.sh` (committed to repo) does:
```bash
cd /var/www/claudebeat
SKILL=$(cat .claude/skills/sk-update-claudes-daily-diary/SKILL.md)
claude --dangerously-skip-permissions -p "$SKILL"
~/claudebeat-venv/bin/python3 ~/claudebeat-approve.py
```

Note: `--dangerously-skip-permissions` is required (not `--non-interactive`) —
the latter does NOT skip permission prompts and the cron would silently stall.

### 4. .gitignore
Ensure `.env` and `claudebeat-approve.env` are in `.gitignore`.

---

## VM environment
- OS: Ubuntu 24.04 LTS
- Repo: `/var/www/claudebeat`
- Python venv: `~/claudebeat-venv/`
- python-telegram-bot: v22.7
- Credentials: `~/claudebeat-approve.env`
