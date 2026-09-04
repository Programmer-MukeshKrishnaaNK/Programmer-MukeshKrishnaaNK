#!/usr/bin/env python3
"""
Generate self-hosted SVG assets for the GitHub profile.

The workflow supplies GITHUB_TOKEN automatically.
No third-party stats service is required.
"""

from __future__ import annotations
import datetime as dt
import json
import os
import urllib.request

USERNAME = os.environ.get("GITHUB_USERNAME", "Programmer-MukeshKrishnaaNK")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

def api(path: str):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN','')}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "mukesh-profile-generator",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def main():
    user = api(f"/users/{USERNAME}")
    repos = api(f"/users/{USERNAME}/repos?per_page=100&sort=updated")
    public_repos = user.get("public_repos", 0)
    followers = user.get("followers", 0)
    stars = sum(r.get("stargazers_count", 0) for r in repos)

    # Keep the stats card self-hosted. Values are replaced in the SVG.
    stats_path = os.path.join(ASSETS, "stats.svg")
    with open(stats_path, encoding="utf-8") as f:
        svg = f.read()
    svg = svg.replace('id="repos" x="18" y="67" fill="url(#g)" font-size="32" font-weight="700">--',
                      f'id="repos" x="18" y="67" fill="url(#g)" font-size="32" font-weight="700">{public_repos}')
    svg = svg.replace('id="followers" x="18" y="67" fill="url(#g)" font-size="32" font-weight="700">--',
                      f'id="followers" x="18" y="67" fill="url(#g)" font-size="32" font-weight="700">{followers}')
    svg = svg.replace('id="stars" x="18" y="67" fill="url(#g)" font-size="32" font-weight="700">--',
                      f'id="stars" x="18" y="67" fill="url(#g)" font-size="32" font-weight="700">{stars}')
    svg = svg.replace('id="updated" x="18" y="67" fill="#c8d1da" font-size="20">--',
                      f'id="updated" x="18" y="67" fill="#c8d1da" font-size="20">{dt.datetime.utcnow():%Y-%m-%d}')
    write(stats_path, svg)

    # Lightweight activity strip from the public events endpoint.
    events = api(f"/users/{USERNAME}/events/public?per_page=100")
    counts = {}
    today = dt.date.today()
    for e in events:
        created = e.get("created_at", "")[:10]
        if created:
            try:
                d = dt.date.fromisoformat(created)
                if (today - d).days < 35:
                    counts[created] = counts.get(created, 0) + 1
            except ValueError:
                pass

    x0, y0, size, gap = 35, 48, 11, 3
    cells = []
    for i in range(35):
        d = today - dt.timedelta(days=34-i)
        n = counts.get(d.isoformat(), 0)
        opacity = min(0.15 + n * 0.18, 1)
        x = x0 + i * (size + gap)
        cells.append(f'<rect x="{x}" y="{y0}" width="{size}" height="{size}" rx="2" fill="url(#g)" opacity="{opacity:.2f}"><animate attributeName="opacity" values="0;{opacity:.2f};{opacity:.2f}" dur="0.8s" begin="{i*0.025:.2f}s" fill="freeze"/></rect>')
        cells.append(f'<rect x="{x}" y="{y0+18}" width="{size}" height="{size}" rx="2" fill="url(#g)" opacity="{max(0.12, opacity*.75):.2f}"/>')
        cells.append(f'<rect x="{x}" y="{y0+36}" width="{size}" height="{size}" rx="2" fill="url(#g)" opacity="{max(0.10, opacity*.55):.2f}"/>')
    with open(os.path.join(ASSETS, "contributions.svg"), encoding="utf-8") as f:
        csvg = f.read()
    csvg = csvg.replace('<g id="cells"></g>', '<g id="cells">' + ''.join(cells) + '</g>')
    write(os.path.join(ASSETS, "contributions.svg"), csvg)

if __name__ == "__main__":
    main()
