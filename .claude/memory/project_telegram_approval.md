---
name: project_telegram_approval
description: Plan to implement Telegram bot editorial approval workflow for autonomous daily diary updates
type: project
---

The user has chosen Option C — Telegram bot — as the editorial approval mechanism for the fully autonomous diary cron job.

**Why:** When the cron job runs at 07:00 daily, Claude writes the day's content and sends a summary to a private Telegram bot. The user taps Approve or Reject from their phone. On Approve, the content is committed and pulled live on the VM. On Reject, the draft is discarded and flagged for manual review.

**How to apply:** When the user is ready, implement this end-to-end in a single session. Full plan below.

---

## What needs to be built

### 1. Create a Telegram bot (user does this — 2 minutes)
- Open Telegram, search for **@BotFather**
- Send `/newbot`, follow prompts, choose a name (e.g. "ClaudeBeat Editor")
- BotFather returns a **bot token** (looks like `123456789:ABCdef...`) — save it
- Start a chat with the new bot (so it can message you)
- Get your **chat ID**: message `@userinfobot` in Telegram — it returns your numeric chat ID

### 2. Install python-telegram-bot on the VM
```bash
pip install python-telegram-bot
```

### 3. Approval workflow logic (to add to cron/skill runner)

The daily cron script should:
1. Run the diary skill (research + write HTML)
2. `git diff --stat` to confirm new files
3. Send a Telegram message to the user's chat ID with:
   - Date
   - Article title + category
   - Entry headlines (bullet list)
   - Sources used
   - Two inline keyboard buttons: ✅ Approve / ❌ Reject
4. Wait for a button press (polling or webhook)
5. On **Approve**: `git commit`, `git push`, `cd /var/www/claudebeat && git pull`
6. On **Reject**: `git checkout -- .` (discard), send confirmation message

### 4. Sending a message with approve/reject buttons (Python sketch)
```python
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler

TOKEN   = "YOUR_BOT_TOKEN"
CHAT_ID = YOUR_CHAT_ID   # integer

async def send_approval_request(summary: str, date: str):
    bot = Bot(token=TOKEN)
    keyboard = [[
        InlineKeyboardButton("✅ Approve", callback_data=f"approve:{date}"),
        InlineKeyboardButton("❌ Reject",  callback_data=f"reject:{date}"),
    ]]
    await bot.send_message(
        chat_id=CHAT_ID,
        text=summary,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
```

### 5. Timeout / fallback
If no response within 4 hours, send a reminder. If no response within 8 hours, auto-approve (so the diary doesn't fall silent on days the user is unavailable). This threshold is configurable.

---

## What the user needs to have ready for the session
- Telegram installed on phone
- 5 minutes to create the bot via @BotFather and get the token + chat ID
- SSH access to the VM

## Notes
- Bot token and chat ID should be stored in a `.env` file on the VM (not in git)
- The `.env` file should be added to `.gitignore`
- This replaces the manual `/sk-update-claudes-daily-diary` invocation entirely
