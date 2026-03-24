---
name: server_deployment
description: claudebeat.ai VM current state, deployment stages, and access details
type: project
---

## Current state (as of 2026-03-22)

S1 and S2 complete. Site is live at https://claudebeat.ai serving the diary directly from GitHub clone.

### VM details
- **Public IP**: 77.68.36.146
- **SSH**: `ssh claude@77.68.36.146 -p 64572`
- **Domain**: `claudebeat.ai` — registered Namecheap, $179.96/2yr (~2027 expiry), LIVE with HTTPS
- **SSL cert**: Let's Encrypt via Certbot, expires 2026-06-20, auto-renewing
- **Web root**: `/var/www/claudebeat` — git clone of https://github.com/gsp4dcs2/claudes-daily-diary

### What's installed
- ✅ Nginx (config at `/etc/nginx/sites-available/claudebeat`, serving claudebeat.ai)
- ✅ Git
- ✅ Certbot / SSL (HTTPS on 443, HTTP→HTTPS redirect)
- ❌ Python 3 + Pillow
- ❌ Claude Code CLI

### To deploy new diary entries
SSH in and pull:
```bash
ssh claude@77.68.36.146 -p 64572
cd /var/www/claudebeat && sudo git pull
```
Entries are live immediately after pull.

---

## Deployment stages

**S1 ✅ — Content deployment pipeline**
VM clones from GitHub. Local skill runs → commits → pushes to GitHub → manual `git pull` on VM deploys.

**S2 ✅ — Domain + HTTPS**
DNS A records set in Namecheap. Certbot installed and configured. HTTPS live.

**S3 — Autonomous daily update (PENDING)**
Install Claude Code CLI on VM with Anthropic API key.
Skill file is in the repo at `.claude/skills/sk-update-claudes-daily-diary/SKILL.md` — arrives with `git clone`/`git pull`.
Cron: `0 7 * * * cd /var/www/claudebeat && claude -p "/sk-update-claudes-daily-diary"`
This runs fully autonomously, no local machine required.
GitHub will remain as a passive offsite mirror — cron job should `git add`, `git commit`, `git push` after each update.

Steps for S3:
1. Install Node.js + Claude Code CLI on VM
2. Set Anthropic API key on VM
3. Set up cron job (skill already in repo)

**Why:** Daily diary must update without user intervention. VM-side Claude Code is the cleanest path.
**How to apply:** S3 is the only remaining stage.
