#!/bin/bash
# /var/www/claudebeat/scripts/run-diary.sh
#
# Daily diary cron wrapper — runs the sk-update-claudes-daily-diary skill
# then the Telegram approval script.
#
# Cron entry (07:00 daily):
#   0 7 * * * /var/www/claudebeat/scripts/run-diary.sh >> /var/log/claudebeat.log 2>&1

set -e

cd /var/www/claudebeat

echo "=== ClaudeBeat diary run: $(date) ==="

SKILL=$(cat .claude/skills/sk-update-claudes-daily-diary/SKILL.md)
claude --dangerously-skip-permissions -p "$SKILL"

echo "--- Skill complete. Running Telegram approval ---"

~/claudebeat-venv/bin/python3 ~/claudebeat-approve.py

echo "=== Done: $(date) ==="
