#!/usr/bin/env python3
"""
make_ascii_svg.py — downsample prepped-photo.png to a character grid and
emit a self-typing, monochrome SVG (avi-ascii.svg).

Each row wipes in left-to-right via an SVG <clipPath> animated with SMIL,
staggered top-to-bottom, then freezes (no looping).
"""
import numpy as np
from PIL import Image

RAMP = " .`:-=+*cs#%@"   # bright (sparse) -> dark (dense); leading space = blank
COLS = 100
ROWS = 53
FONT_SIZE = 8.6
CHAR_W = FONT_SIZE * 0.6      # monospace advance width
LINE_H = FONT_SIZE * 1.0
FILL_COLOR = "#8b949e"        # light gray, GitHub dark-mode friendly
CURSOR_COLOR = "#c9d1d9"

def image_to_ascii_grid(path: str, cols: int, rows: int) -> list[str]:
    img = Image.open(path).convert("L")
    # keep source aspect ratio, but characters are taller than wide,
    # so squash vertical sampling a bit to avoid a stretched portrait
    img = img.resize((cols, rows), Image.LANCZOS)
    arr = np.array(img).astype(np.float32) / 255.0  # 0=black,1=white

    ramp_len = len(RAMP)
    lines = []
    for y in range(rows):
        row_chars = []
        for x in range(cols):
            brightness = arr[y, x]
            idx = int((1.0 - brightness) * (ramp_len - 1) + 0.5)
            idx = max(0, min(ramp_len - 1, idx))
            row_chars.append(RAMP[idx])
        lines.append("".join(row_chars))
    return lines

def escape_xml(s: str) -> str:
    return (s.replace("&", "&amp;")
              .replace("<", "&lt;")
              .replace(">", "&gt;"))

def build_svg(lines: list[str], out_path: str):
    width = COLS * CHAR_W + 20
    height = ROWS * LINE_H + 20

    total_rows = len(lines)
    row_stagger = 0.045          # seconds between each row starting
    row_wipe_dur = 0.5           # seconds for a single row to fully wipe in
    last_start = (total_rows - 1) * row_stagger
    total_dur = last_start + row_wipe_dur

    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" '
        f'width="{width:.0f}" height="{height:.0f}" font-family="Consolas, \'Courier New\', monospace">'
    )
    svg_parts.append('<rect width="100%" height="100%" fill="transparent"/>')
    svg_parts.append("<defs>")

    for i, line in enumerate(lines):
        stripped_len = len(line.rstrip())
        if stripped_len == 0:
            continue
        row_width = stripped_len * CHAR_W
        start_t = i * row_stagger
        clip_id = f"clip{i}"
        svg_parts.append(f'<clipPath id="{clip_id}">')
        svg_parts.append(
            f'<rect x="0" y="0" width="0" height="{LINE_H:.2f}">'
            f'<animate attributeName="width" from="0" to="{row_width:.2f}" '
            f'begin="{start_t:.3f}s" dur="{row_wipe_dur:.2f}s" '
            f'fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>'
            f'</rect>'
        )
        svg_parts.append("</clipPath>")

    svg_parts.append("</defs>")
    svg_parts.append(f'<g transform="translate(10,10)">')

    for i, line in enumerate(lines):
        stripped = line.rstrip()
        if len(stripped) == 0:
            continue
        y = i * LINE_H
        clip_id = f"clip{i}"
        start_t = i * row_stagger
        row_width = len(stripped) * CHAR_W
        text_escaped = escape_xml(stripped)

        svg_parts.append(f'<g clip-path="url(#{clip_id})">')
        svg_parts.append(
            f'<text x="0" y="{y + LINE_H*0.82:.2f}" font-size="{FONT_SIZE}" '
            f'fill="{FILL_COLOR}" xml:space="preserve">{text_escaped}</text>'
        )
        svg_parts.append("</g>")

        # small cursor block riding the wipe edge of each row, then vanishing
        svg_parts.append(
            f'<rect x="0" y="{y + LINE_H*0.12:.2f}" width="{CHAR_W*0.55:.2f}" '
            f'height="{LINE_H*0.8:.2f}" fill="{CURSOR_COLOR}" opacity="0">'
            f'<animate attributeName="x" from="0" to="{row_width:.2f}" '
            f'begin="{start_t:.3f}s" dur="{row_wipe_dur:.2f}s" fill="freeze" '
            f'calcMode="spline" keySplines="0.25 0.1 0.25 1"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" '
            f'keyTimes="0;0.05;0.9;1" begin="{start_t:.3f}s" '
            f'dur="{row_wipe_dur:.2f}s" fill="freeze"/>'
            f'</rect>'
        )

    svg_parts.append("</g>")
    svg_parts.append("</svg>")

    with open(out_path, "w") as f:
        f.write("\n".join(svg_parts))
    print(f"wrote {out_path}  ({total_rows} rows, total anim ~{total_dur:.2f}s)")

if __name__ == "__main__":
    lines = image_to_ascii_grid("prepped-photo.png", COLS, ROWS)
    build_svg(lines, "avi-ascii.svg")
