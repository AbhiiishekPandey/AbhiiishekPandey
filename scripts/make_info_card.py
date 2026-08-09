#!/usr/bin/env python3
"""
make_info_card.py — hand-authored neofetch-style SVG panel.
Lines fade + slide in on a short stagger, then freeze.

Set STATIC=1 to emit a frozen (fully-visible, non-animated) frame,
handy for local Quick Look previews.
"""
import os

WIDTH = 490
HEIGHT = 372
STATIC = os.environ.get("STATIC") == "1"

TITLE = "avi@github"
DIVIDER_LEN = 30

FIELDS = [
    ("Now", "B.Tech Data Science Student"),
    ("Prev", "Web Dev \u00b7 Antigravity (Vite/React/TS)"),
    ("Stack", "Python \u00b7 SQL \u00b7 Excel \u00b7 Power BI"),
    ("Building", "HEALTH. \u2014 health content brand"),
    ("Organizing", "GDG \u00b7 TEDx campus chapters"),
    ("Focus", "Data Analysis \u00b7 Business Analytics"),
]

BG = "#0d1117"
BORDER = "#30363d"
TITLE_COLOR = "#c9d1d9"
LABEL_COLOR = "#39d353"
VALUE_COLOR = "#8b949e"
DIVIDER_COLOR = "#30363d"
PROMPT_COLOR = "#58a6ff"

FONT = "Consolas, 'Courier New', monospace"
LABEL_SIZE = 13.5
LINE_H = 30
PAD_X = 26
TOP_Y = 46


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def anim_attrs(start_t: float, dur: float = 0.45):
    if STATIC:
        return ""
    return (
        f'<animate attributeName="opacity" from="0" to="1" '
        f'begin="{start_t:.2f}s" dur="{dur}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="-14,0" to="0,0" begin="{start_t:.2f}s" dur="{dur}s" '
        f'fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>'
    )


def build_svg(out_path: str):
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'width="{WIDTH}" height="{HEIGHT}" font-family="{FONT}">'
    )

    # panel background + border, rounded
    parts.append(
        f'<rect x="1" y="1" width="{WIDTH-2}" height="{HEIGHT-2}" rx="10" '
        f'fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>'
    )

    # title bar: three "traffic light" dots + title text
    parts.append('<circle cx="24" cy="22" r="6" fill="#ff5f56"/>')
    parts.append('<circle cx="44" cy="22" r="6" fill="#ffbd2e"/>')
    parts.append('<circle cx="64" cy="22" r="6" fill="#27c93f"/>')
    parts.append(
        f'<text x="{WIDTH/2}" y="27" font-size="13" fill="{TITLE_COLOR}" '
        f'text-anchor="middle">{esc(TITLE)}</text>'
    )
    parts.append(f'<line x1="0" y1="40" x2="{WIDTH}" y2="40" stroke="{BORDER}" stroke-width="1"/>')

    # shell prompt line
    y = TOP_Y
    t = 0.0
    parts.append(f'<g opacity="{1 if STATIC else 0}" transform="translate({0 if STATIC else -14},0)">')
    parts.append(
        f'<text x="{PAD_X}" y="{y}" font-size="{LABEL_SIZE}" fill="{PROMPT_COLOR}">'
        f'&gt; whoami --verbose</text>'
    )
    parts.append(anim_attrs(t))
    parts.append("</g>")
    t += 0.12
    y += LINE_H

    # divider
    parts.append(f'<g opacity="{1 if STATIC else 0}" transform="translate({0 if STATIC else -14},0)">')
    parts.append(
        f'<text x="{PAD_X}" y="{y}" font-size="{LABEL_SIZE}" fill="{DIVIDER_COLOR}">'
        f'{"-" * DIVIDER_LEN}</text>'
    )
    parts.append(anim_attrs(t))
    parts.append("</g>")
    t += 0.10
    y += LINE_H

    # key/value rows
    label_col_w = 118
    for label, value in FIELDS:
        parts.append(f'<g opacity="{1 if STATIC else 0}" transform="translate({0 if STATIC else -14},0)">')
        parts.append(
            f'<text x="{PAD_X}" y="{y}" font-size="{LABEL_SIZE}" fill="{LABEL_COLOR}" '
            f'font-weight="bold">{esc(label)}</text>'
        )
        parts.append(
            f'<text x="{PAD_X + label_col_w}" y="{y}" font-size="{LABEL_SIZE}" '
            f'fill="{VALUE_COLOR}">{esc(value)}</text>'
        )
        parts.append(anim_attrs(t))
        parts.append("</g>")
        t += 0.14
        y += LINE_H

    # closing divider + blinking cursor
    parts.append(f'<g opacity="{1 if STATIC else 0}" transform="translate({0 if STATIC else -14},0)">')
    parts.append(
        f'<text x="{PAD_X}" y="{y}" font-size="{LABEL_SIZE}" fill="{DIVIDER_COLOR}">'
        f'{"-" * DIVIDER_LEN}</text>'
    )
    parts.append(anim_attrs(t))
    parts.append("</g>")
    t += 0.12
    y += LINE_H

    parts.append(f'<g opacity="{1 if STATIC else 0}">')
    parts.append(f'<text x="{PAD_X}" y="{y}" font-size="{LABEL_SIZE}" fill="{PROMPT_COLOR}">&gt; _</text>')
    if not STATIC:
        parts.append(f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="0.3s" fill="freeze"/>')
        cursor_start = t + 0.3
        parts.append(
            f'<animate attributeName="opacity" values="1;0;1" keyTimes="0;0.5;1" '
            f'begin="{cursor_start:.2f}s" dur="1s" repeatCount="indefinite"/>'
        )
    parts.append("</g>")

    parts.append("</svg>")

    with open(out_path, "w") as f:
        f.write("\n".join(parts))
    print(f"wrote {out_path} (STATIC={STATIC})")


if __name__ == "__main__":
    build_svg("info-card.svg")
