# $ ~/claudebeat-venv/bin/python3 ./scripts/claudebeat-approve.py
#
# Telegram editorial approval for the ClaudeBeat daily diary cron job.
#
# Workflow:
#   1. Find new/untracked article files (git status)
#   2. Extract title + entry headlines from the HTML
#   3. Send Telegram message with Approve / Reject inline buttons
#   4. Wait up to 8 hours for a button press
#   5. Approve  -> git add -A, commit, push; confirm to user
#   6. Reject   -> discard all uncommitted changes; confirm to user
#   7. Timeout  -> auto-approve (diary never silently stalls)

import asyncio
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup


# ── Credentials ───────────────────────────────────────────────────────────────

def load_env(path):
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())

load_env(Path.home() / 'claudebeat-approve.env')

TOKEN   = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = int(os.environ['TELEGRAM_CHAT_ID'])
REPO    = Path('/var/www/claudebeat')
TIMEOUT = 8 * 3600  # seconds — auto-approve after 8 hours


# ── Git helpers ───────────────────────────────────────────────────────────────

def get_new_html_files():
    result = subprocess.run(
        ['git', 'status', '--porcelain'],
        cwd=REPO, capture_output=True, text=True, check=True
    )
    files = []
    for line in result.stdout.splitlines():
        status = line[:2].strip()
        path   = line[3:].strip()
        if 'articles/' in path and path.endswith('.html'):
            files.append(REPO / path)
    return files


def git_approve(today):
    subprocess.run(['git', 'add', '-A'], cwd=REPO, check=True)
    subprocess.run(
        ['git', 'commit', '-m', f'Add {today} diary entry [approved via Telegram]'],
        cwd=REPO, check=True
    )
    subprocess.run(['git', 'push'], cwd=REPO, check=True)


def git_reject():
    subprocess.run(['git', 'restore', '--staged', '.'], cwd=REPO)
    subprocess.run(['git', 'restore', '.'], cwd=REPO)
    subprocess.run(['git', 'clean', '-fd', 'articles/'], cwd=REPO)


# ── HTML parsing ──────────────────────────────────────────────────────────────

def extract_info(html_path):
    content = html_path.read_text(encoding='utf-8')

    m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    title = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else html_path.stem
    title = re.sub(r'&amp;', '&', title)

    raw_h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL)
    headlines = []
    for h in raw_h2s:
        text = re.sub(r'<[^>]+>', '', h)
        text = re.sub(r'&amp;', '&', text)
        text = re.sub(r'&#\d+;', '', text)
        text = re.sub(r'^[^\w(]+', '', text).strip()
        if text:
            headlines.append(text)

    return title, headlines


# ── Main ──────────────────────────────────────────────────────────────────────

async def run():
    today     = datetime.now().strftime('%Y-%m-%d')
    new_files = get_new_html_files()

    if not new_files:
        print('No new article files found — nothing to approve.')
        return

    lines = [f'\U0001f4f0 *ClaudeBeat \u2014 {today}*\n']
    for f in sorted(new_files):
        title, headlines = extract_info(f)
        lines.append(f'*{title}*')
        for h in headlines:
            lines.append(f'  \u2022 {h}')
    lines.append('\nApprove to commit & push live, or Reject to discard.')
    text = '\n'.join(lines)

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton('\u2705 Approve', callback_data='approve'),
        InlineKeyboardButton('\u274c Reject',  callback_data='reject'),
    ]])

    async with Bot(TOKEN) as bot:
        msg    = await bot.send_message(
            chat_id=CHAT_ID,
            text=text,
            parse_mode='Markdown',
            reply_markup=keyboard,
        )
        msg_id = msg.message_id
        print(f'Approval message sent (id={msg_id}). Waiting up to 8 hours...')

        decision   = None
        offset     = None
        loop_start = asyncio.get_event_loop().time()

        while asyncio.get_event_loop().time() - loop_start < TIMEOUT:
            try:
                updates = await bot.get_updates(
                    offset=offset, timeout=30,
                    allowed_updates=['callback_query']
                )
            except Exception as e:
                print(f'Poll error (will retry): {e}')
                await asyncio.sleep(10)
                continue

            for upd in updates:
                offset = upd.update_id + 1
                cq = upd.callback_query
                if cq and cq.message.message_id == msg_id:
                    decision = cq.data
                    await cq.answer()

            if decision:
                break

        try:
            await bot.edit_message_reply_markup(
                chat_id=CHAT_ID, message_id=msg_id, reply_markup=None
            )
        except Exception:
            pass

        if decision is None:
            decision = 'approve'
            print('Timeout reached — auto-approving.')

        if decision == 'approve':
            git_approve(today)
            await bot.send_message(
                chat_id=CHAT_ID,
                text=f'\u2705 *{today}* committed and pushed live.',
                parse_mode='Markdown',
            )
            print('Approved and pushed.')
        else:
            git_reject()
            await bot.send_message(
                chat_id=CHAT_ID,
                text=f'\u274c *{today}* draft discarded. No changes committed.',
                parse_mode='Markdown',
            )
            print('Rejected — changes discarded.')


asyncio.run(run())
