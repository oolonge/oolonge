#!/usr/bin/env python3
"""Render section labels as SVG so their size is not tied to heading levels."""

LABELS = {"stack": "Stack", "socials": "Socials"}
SIZE = 18
THEMES = {"light": "#1F2328", "dark": "#E6EDF3"}
FONT = '-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif'


def render(text, color):
    width = int(len(text) * SIZE * 0.62) + 4
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="24" '
        f'viewBox="0 0 {width} 24" role="img" aria-label="{text}">'
        f'<text x="0" y="17" font-family=\'{FONT}\' font-size="{SIZE}" '
        f'font-weight="600" fill="{color}">{text}</text></svg>'
    )


for slug, text in LABELS.items():
    for theme, color in THEMES.items():
        path = f"assets/label-{slug}-{theme}.svg"
        with open(path, "w") as f:
            f.write(render(text, color))
        print(f"wrote {path}")
