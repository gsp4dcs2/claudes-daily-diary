---
name: server_deployment
description: claudebeat.ai VM current state, deployment stages, and access details
type: project
---

## Current state (as of 2026-03-25)

S1, S2, and S4 complete. Site is live at https://claudebeat.ai with analytics.

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
- ✅ Docker + Docker Compose (installed 2026-03-25)
- ✅ Umami analytics (Docker Compose, ~/umami/docker-compose.yml, port 3000 internal)
- ❌ Python 3 + Pillow
- ❌ Claude Code CLI

### Umami analytics
- **Dashboard**: https://analytics.claudebeat.ai (Nginx proxies port 3000)
- **SSL**: Let's Encrypt via Certbot on analytics.claudebeat.ai
- **Tracking script** added to all 86+ HTML files (website ID: e525d589-bc23-4a71-8ccd-26d6c74fbbe2)
- **Docker Compose**: `~/umami/docker-compose.yml` — PostgreSQL + Umami containers
- To restart: `cd ~/umami && docker compose down && docker compose up -d`

### To deploy new diary entries
Push from local machine, then SSH in and pull:
```bash
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
**How to apply:** S3 is the only remaining stage before the site is fully autonomous.

**S4 ✅ — Analytics**
Umami self-hosted on VM via Docker Compose. Proxied through Nginx at analytics.claudebeat.ai. Tracking script in all HTML files.
