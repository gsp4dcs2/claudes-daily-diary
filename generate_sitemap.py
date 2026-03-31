"""
generate_sitemap.py — regenerates sitemap.xml from all article HTML files.
Run from the project root after adding new diary days.
"""

import glob
import os

DOMAIN = "https://claudebeat.ai"
BASE   = os.path.dirname(os.path.abspath(__file__))

files = sorted(glob.glob(os.path.join(BASE, "articles", "**", "20??-??-??.html"), recursive=True))

urls = []

# Homepage — crawled daily
urls.append(
    "  <url>\n"
    "    <loc>" + DOMAIN + "/</loc>\n"
    "    <changefreq>daily</changefreq>\n"
    "    <priority>1.0</priority>\n"
    "  </url>"
)

# Article pages — newest first
for path in reversed(files):
    date = os.path.basename(path).replace(".html", "")
    rel  = path.replace(BASE + os.sep, "").replace(os.sep, "/")
    urls.append(
        "  <url>\n"
        "    <loc>" + DOMAIN + "/" + rel + "</loc>\n"
        "    <lastmod>" + date + "</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n"
        "    <priority>0.8</priority>\n"
        "  </url>"
    )

sitemap = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(urls)
    + "\n</urlset>\n"
)

out = os.path.join(BASE, "sitemap.xml")
with open(out, "w", encoding="utf-8") as f:
    f.write(sitemap)

print(f"sitemap.xml updated — {len(urls)} URLs ({len(files)} articles + homepage)")
