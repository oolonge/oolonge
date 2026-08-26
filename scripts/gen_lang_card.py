#!/usr/bin/env python3
"""Render a "Most Used Languages" card as SVG from the GitHub API."""

import json
import os
import urllib.request

USER = "oolonge"
TOP_N = 6
WIDTH = 340
OUT = {
    "assets/top-langs-light.svg": {"title": "#4C566A", "text": "#4C566A", "track": "#E5E9F0"},
    "assets/top-langs-dark.svg": {"title": "#81A1C1", "text": "#D8DEE9", "track": "#2E3440"},
}

COLORS = {
    "C++": "#f34b7d", "C": "#555555", "Python": "#3572A5", "R": "#198CE7",
    "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "HTML": "#e34c26", "CSS": "#663399",
    "PHP": "#4F5D95", "Shell": "#89e051", "Makefile": "#427819", "CMake": "#DA3434",
    "QMake": "#427819", "TeX": "#3D6117", "MATLAB": "#e16737", "Assembly": "#6E4C13",
    "Dockerfile": "#384d54", "Mako": "#7e858d", "PLpgSQL": "#336790", "RPC": "#34495e",
    "Jupyter Notebook": "#DA5B0B", "Batchfile": "#C1F12E", "Go": "#00ADD8", "Rust": "#dea584",
}
FALLBACK = "#8c9bab"


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}",
                                 headers={"Accept": "application/vnd.github+json",
                                          "User-Agent": "lang-card"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect():
    totals = {}
    page = 1
    while True:
        repos = api(f"/users/{USER}/repos?per_page=100&page={page}")
        if not repos:
            break
        for repo in repos:
            if repo["fork"]:
                continue
            for lang, size in api(f"/repos/{USER}/{repo['name']}/languages").items():
                totals[lang] = totals.get(lang, 0) + size
        page += 1
    return totals


def render(langs, theme):
    total = sum(size for _, size in langs)
    rows = (len(langs) + 1) // 2
    height = 74 + rows * 24
    bar_w = WIDTH - 32

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" aria-label="Most used languages">',
        '<style>'
        '.t{font:600 16px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;fill:'
        + theme["title"] + '}'
        '.l{font:400 12px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;fill:'
        + theme["text"] + '}'
        '</style>',
        '<text x="16" y="26" class="t">Most Used Languages</text>',
        f'<rect x="16" y="40" width="{bar_w}" height="8" rx="4" fill="{theme["track"]}"/>',
        f'<clipPath id="bar"><rect x="16" y="40" width="{bar_w}" height="8" rx="4"/></clipPath>',
        '<g clip-path="url(#bar)">',
    ]

    offset = 16.0
    for name, size in langs:
        seg = bar_w * size / total
        parts.append(f'<rect x="{offset:.2f}" y="40" width="{seg:.2f}" height="8" '
                     f'fill="{COLORS.get(name, FALLBACK)}"/>')
        offset += seg
    parts.append('</g>')

    for i, (name, size) in enumerate(langs):
        col, row = i % 2, i // 2
        x = 16 + col * (bar_w / 2 + 8)
        y = 74 + row * 24
        pct = 100.0 * size / total
        parts.append(f'<circle cx="{x + 5:.1f}" cy="{y - 4:.1f}" r="5" '
                     f'fill="{COLORS.get(name, FALLBACK)}"/>')
        parts.append(f'<text x="{x + 17:.1f}" y="{y:.1f}" class="l">{name} {pct:.1f}%</text>')

    parts.append('</svg>')
    return "\n".join(parts)


def main():
    totals = collect()
    langs = sorted(totals.items(), key=lambda kv: -kv[1])[:TOP_N]
    for path, theme in OUT.items():
        with open(path, "w") as f:
            f.write(render(langs, theme))
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
