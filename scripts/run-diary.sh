#!/bin/bash
# /var/www/claudebeat/scripts/run-diary.sh
#
# Daily diary cron wrapper — runs the sk-update-claudes-daily-diary skill
# then the Telegram approval script.
#
# The skill runs inside a git worktree (/tmp/claudebeat-draft-*) so its output
# never touches the live Nginx-served directory until the user taps Publish.
#
# Cron entry (07:00 daily):
#   0 7 * * * /var/www/claudebeat/scripts/run-diary.sh >> /var/log/claudebeat.log 2>&1

set -e

cd /var/www/claudebeat

echo "=== ClaudeBeat diary run: $(date) ==="

# Create a draft worktree — Nginx never serves this location
DRAFT_DIR="/tmp/claudebeat-draft-$(date +%Y%m%d-%H%M%S)"
git worktree add --detach "$DRAFT_DIR" HEAD
trap "git worktree remove '$DRAFT_DIR' --force 2>/dev/null || true" EXIT

# Run skill inside the draft worktree
cd "$DRAFT_DIR"
SKILL=$(awk '/^---$/{n++; if(n==2){found=1; next}} found{print}' /var/www/claudebeat/.claude/skills/sk-update-claudes-daily-diary/SKILL.md)
claude --dangerously-skip-permissions -p "$SKILL"

echo "--- Skill complete. Running Telegram approval ---"

DRAFT_DIR="$DRAFT_DIR" ~/claudebeat-venv/bin/python3 /var/www/claudebeat/scripts/claudebeat-approve.py

echo "=== Done: $(date) ==="
