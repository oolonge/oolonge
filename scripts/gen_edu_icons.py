#!/usr/bin/env python3
"""Wrap the university logos in SVG with a transparent bottom pad.

With align="middle" a browser puts the image centre 4.15px above the baseline,
while the optical centre of a 16px line sits ~5.8px above it. Padding the bottom
of the icon by twice that difference (~20.6% of its height) lifts the artwork by
exactly the missing amount, so the logo lines up with the text.
"""

import base64
import re

PAD = 0.206  # share of the artwork height added below it


def wrap(body, view, colour_note=""):
    height = round(view * (1 + PAD), 2)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {view} {height}" width="{view}" height="{height}">{colour_note}{body}</svg>')


png = base64.b64encode(open("assets/bmstu-iu7.png", "rb").read()).decode()
open("assets/bmstu-iu7-pad.svg", "w").write(
    wrap(f'<image x="0" y="0" width="192" height="192" xlink:href="data:image/png;base64,{png}"/>', 192))
print("wrote assets/bmstu-iu7-pad.svg")

cu = open("assets/cu.svg").read()
inner = re.sub(r"\s+", " ", cu[cu.index("<g "):cu.rindex("</g>") + 4])
for theme, colour in (("light", "#4C566A"), ("dark", "#D8DEE9")):
    path = f"assets/cu-pad-{theme}.svg"
    open(path, "w").write(wrap(inner.replace('fill="#000000"', f'fill="{colour}"'), 700))
    print(f"wrote {path}")
