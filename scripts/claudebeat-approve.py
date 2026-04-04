# $ ~/claudebeat-venv/bin/python3 ./scripts/claudebeat-approve.py
#
# Telegram editorial approval for the ClaudeBeat daily diary cron job.
#
# Workflow:
#   1. Find new/untracked article HTML files (git status)
#   2. Extract each entry: headline, source badge, body snippet
#   3. Send one Telegram message per entry with [✅ Include] [❌ Skip] buttons
#   4. After all entries reviewed, send a summary with [📤 Publish N] [🗑 Discard all]
#   5. Publish  -> strip skipped entries from HTML, git add -A, commit, push
#   6. Discard  -> git restore + clean, notify user
#   7. Timeout (8 hrs) -> auto-publish all entries

import asyncio
import os
import re
import shutil
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

TOKEN    = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID  = int(os.environ['TELEGRAM_CHAT_ID'])
LIVE     = Path('/var/www/claudebeat')
REPO     = Path(os.environ.get('DRAFT_DIR', str(LIVE)))  # draft worktree, or live if standalone
IS_DRAFT = REPO != LIVE
TIMEOUT  = 8 * 3600  # seconds


# ── Source tier → stars ───────────────────────────────────────────────────────

TIER1_DOMAINS = {'anthropic.com', 'support.claude.com', 'red.anthropic.com'}
TIER2_DOMAINS = {
    'techcrunch.com', 'engadget.com', 'techradar.com', 'theverge.com',
    'wired.com', 'arstechnica.com', 'macrumors.com', 'appleinsider.com',
    '9to5mac.com', 'cnbc.com', 'fortune.com', 'bloomberg.com',
    'reuters.com', 'scientificamerican.com', 'techtimes.com',
}

def stars_for_url(url):
    if not url or url.lower().startswith('inspired'):
        return '⭐⭐⭐', 'Official Anthropic source'
    try:
        domain = url.split('/')[2].lstrip('www.')
    except IndexError:
        return '⭐', 'Community / research'
    if domain in TIER1_DOMAINS:
        return '⭐⭐⭐', 'Official Anthropic source'
    if domain in TIER2_DOMAINS:
        return '⭐⭐', 'Established press — verified journalism'
    return '⭐', 'Community / research — cross-checked'


# ── Git helpers ───────────────────────────────────────────────────────────────

def get_new_html_files():
    result = subprocess.run(
        ['git', 'status', '--porcelain'],
        cwd=REPO, capture_output=True, text=True, check=True
    )
    files = []
    for line in result.stdout.splitlines():
        path = line[3:].strip()
        if 'articles/' in path and path.endswith('.html'):
            files.append(REPO / path)
    return sorted(files)


def git_publish(today):
    if IS_DRAFT:
        # Copy only changed files from draft worktree to live dir, track them
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=REPO, capture_output=True, text=True, check=True
        )
        copied = []
        for line in result.stdout.splitlines():
            rel = line[3:].strip().strip('"')
            src = REPO / rel
            dst = LIVE / rel
            if src.is_file():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                copied.append(rel)
        # Add only the files we copied — never git add -A on the live dir
        if copied:
            subprocess.run(['git', 'add', '--'] + copied, cwd=LIVE, check=True)
    else:
        subprocess.run(['git', 'add', '-A'], cwd=LIVE, check=True)
    subprocess.run(
        ['git', 'commit', '-m',
         f'Add {today} diary entry [approved via Telegram]'],
        cwd=LIVE, check=True
    )
    subprocess.run(['git', 'push'], cwd=LIVE, check=True)


def git_discard():
    if not IS_DRAFT:
        # Standalone mode: clean up the live dir directly
        subprocess.run(['git', 'restore', '--staged', '.'], cwd=LIVE)
        subprocess.run(['git', 'restore', '.'], cwd=LIVE)
        subprocess.run(['git', 'clean', '-fd', 'articles/'], cwd=LIVE)
    # Draft mode: run-diary.sh's trap removes the worktree automatically


# ── HTML helpers ──────────────────────────────────────────────────────────────

def escape_html(text):
    """Escape HTML special characters for Telegram HTML parse mode."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def clean(html):
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&[a-z]+;', '', text)
    text = re.sub(r'&#\d+;', '', text)
    return re.sub(r'\s+', ' ', text).strip()


def extract_entries(html_path):
    """Return list of dicts: {headline, source_url, snippet, raw}"""
    content = html_path.read_text(encoding='utf-8')

    # Find ALL article blocks (re.finditer, not re.search)
    entries = []
    for match in re.finditer(
        r'<article class="entry">(.*?)</article>', content, re.DOTALL
    ):
        raw  = match.group(0)
        pos  = match.start()

        # Look back up to 600 chars for the nearest Source: URL
        preceding = content[max(0, pos - 600):pos]
        src = re.search(r'Source:\s*(https?://\S+)', preceding)
        source_url = src.group(1) if src else ''

        # Headline from h2 (strip icon span + entities)
        h2 = re.search(r'<h2[^>]*>(.*?)</h2>', raw, re.DOTALL)
        headline = re.sub(r'^[^\w(]+', '', clean(h2.group(1))) if h2 else '(no title)'

        # First <p> as snippet, up to 180 chars
        p = re.search(r'<p>(.*?)</p>', raw, re.DOTALL)
        snippet = clean(p.group(1))[:180].rsplit(' ', 1)[0] + '…' if p else ''

        entries.append({
            'headline':   headline,
            'source_url': source_url,
            'snippet':    snippet,
            'raw':        raw,
        })

    return entries


def remove_skipped_entries(html_path, skipped_raws):
    """Rewrite the HTML file with skipped article blocks removed."""
    content = html_path.read_text(encoding='utf-8')
    for raw in skipped_raws:
        content = content.replace(raw, '')
    html_path.write_text(content, encoding='utf-8')


# ── Telegram polling helper ───────────────────────────────────────────────────

async def wait_for_callback(bot, target_msg_id, offset_ref, deadline):
    """Poll until a callback for target_msg_id arrives or deadline passes."""
    while asyncio.get_event_loop().time() < deadline:
        try:
            updates = await bot.get_updates(
                offset=offset_ref[0], timeout=30,
                allowed_updates=['callback_query']
            )
        except Exception as e:
            print(f'Poll error: {e}')
            await asyncio.sleep(10)
            continue

        for upd in updates:
            offset_ref[0] = upd.update_id + 1
            cq = upd.callback_query
            if cq and cq.message.message_id == target_msg_id:
                await cq.answer()
                return cq.data

    return None  # timed out


# ── Main ──────────────────────────────────────────────────────────────────────

async def run():
    today     = datetime.now().strftime('%Y-%m-%d')
    new_files = get_new_html_files()

    if not new_files:
        print('No new article files found — nothing to approve.')
        return

    # Collect all entries across all new files
    all_entries = []
    for f in new_files:
        for entry in extract_entries(f):
            entry['file'] = f
            all_entries.append(entry)

    if not all_entries:
        print('New HTML files found but no <article> entries parsed.')
        return

    print(f'Found {len(all_entries)} entries across {len(new_files)} file(s).')

    decisions   = {}   # index -> 'include' | 'skip'
    offset_ref  = [None]
    deadline    = asyncio.get_event_loop().time() + TIMEOUT

    async with Bot(TOKEN) as bot:

        # ── Step 1: send one message per entry ───────────────────────────────
        msg_to_idx = {}

        for i, entry in enumerate(all_entries):
            stars, tip = stars_for_url(entry['source_url'])
            try:
                domain = entry['source_url'].split('/')[2].lstrip('www.')
            except IndexError:
                domain = 'anthropic.com'

            n_of_n = f'Entry {i+1} of {len(all_entries)}'
            text = (
                f'<b>{n_of_n}</b> — {stars} {escape_html(domain)}\n'
                f'<b>{escape_html(entry["headline"])}</b>\n\n'
                f'<i>{escape_html(entry["snippet"])}</i>'
            )
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton('✅ Include', callback_data=f'include_{i}'),
                InlineKeyboardButton('❌ Skip',    callback_data=f'skip_{i}'),
            ]])
            msg = await bot.send_message(
                chat_id=CHAT_ID, text=text,
                parse_mode='HTML', reply_markup=keyboard
            )
            msg_to_idx[msg.message_id] = i
            print(f'  Sent entry {i+1}: {entry["headline"][:60]}')

        # ── Step 2: collect decisions for each entry ──────────────────────────
        while len(decisions) < len(all_entries):
            if asyncio.get_event_loop().time() >= deadline:
                # Auto-include anything not yet decided
                for i in range(len(all_entries)):
                    decisions.setdefault(i, 'include')
                print('Timeout — auto-including all undecided entries.')
                break

            try:
                updates = await bot.get_updates(
                    offset=offset_ref[0], timeout=30,
                    allowed_updates=['callback_query']
                )
            except Exception as e:
                print(f'Poll error: {e}')
                await asyncio.sleep(10)
                continue

            for upd in updates:
                offset_ref[0] = upd.update_id + 1
                cq = upd.callback_query
                if not cq:
                    continue

                data = cq.data  # e.g. 'include_2' or 'skip_0'
                if not data:
                    continue

                parts = data.rsplit('_', 1)
                if len(parts) == 2 and parts[1].isdigit():
                    action, idx = parts[0], int(parts[1])
                    if idx not in decisions:
                        decisions[idx] = action
                        # Remove buttons from that message
                        try:
                            await bot.edit_message_reply_markup(
                                chat_id=CHAT_ID,
                                message_id=cq.message.message_id,
                                reply_markup=None
                            )
                        except Exception:
                            pass
                        label = '✅ Included' if action == 'include' else '❌ Skipped'
                        await bot.edit_message_text(
                            chat_id=CHAT_ID,
                            message_id=cq.message.message_id,
                            text=cq.message.text + f'\n\n{label}',
                            parse_mode=None
                        )
                        await cq.answer()
                        print(f'  Entry {idx+1}: {action}')

        # ── Step 3: summary + final publish/discard button ────────────────────
        included = [i for i, d in decisions.items() if d == 'include']
        skipped  = [i for i, d in decisions.items() if d == 'skip']

        summary_lines = [f'📋 <b>Review complete — {today}</b>\n']
        for i, entry in enumerate(all_entries):
            mark = '✅' if decisions.get(i) == 'include' else '❌'
            summary_lines.append(f'{mark} {escape_html(entry["headline"][:60])}')

        if included:
            summary_lines.append(f'\n{len(included)} entr{"y" if len(included)==1 else "ies"} selected for publication.')
            pub_label = f'📤 Publish {len(included)} selected'
        else:
            summary_lines.append('\nNo entries selected — nothing will be published.')
            pub_label = '📤 Publish (nothing selected)'

        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(pub_label,      callback_data='final_publish'),
            InlineKeyboardButton('🗑 Discard all', callback_data='final_discard'),
        ]])

        summary_msg = await bot.send_message(
            chat_id=CHAT_ID,
            text='\n'.join(summary_lines),
            parse_mode='HTML',
            reply_markup=keyboard
        )

        # ── Step 4: wait for final decision ───────────────────────────────────
        final = await wait_for_callback(
            bot, summary_msg.message_id, offset_ref, deadline
        )
        if final is None:
            final = 'final_publish'
            print('Timeout on final step — auto-publishing.')

        try:
            await bot.edit_message_reply_markup(
                chat_id=CHAT_ID,
                message_id=summary_msg.message_id,
                reply_markup=None
            )
        except Exception:
            pass

        # ── Step 5: act on final decision ─────────────────────────────────────
        if final == 'final_publish' and included:
            # Remove skipped entries from HTML files before committing
            skipped_by_file = {}
            for i in skipped:
                f = all_entries[i]['file']
                skipped_by_file.setdefault(f, []).append(all_entries[i]['raw'])
            for f, raws in skipped_by_file.items():
                remove_skipped_entries(f, raws)

            git_publish(today)
            await bot.send_message(
                chat_id=CHAT_ID,
                text=f'✅ <b>{today}</b> — {len(included)} entr{"y" if len(included)==1 else "ies"} committed and pushed live.',
                parse_mode='HTML'
            )
            print(f'Published {len(included)} entries.')

        else:
            git_discard()
            await bot.send_message(
                chat_id=CHAT_ID,
                text=f'🗑 <b>{today}</b> draft discarded. No changes committed.',
                parse_mode='HTML'
            )
            print('Discarded — no changes committed.')


asyncio.run(run())
