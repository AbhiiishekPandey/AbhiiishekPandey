#!/usr/bin/env python3
"""
make_ascii_svg.py — downsample prepped-photo.png to a character grid and
emit a self-typing, monochrome SVG (avi-ascii.svg).

v2: rows reveal via opacity + slide (animate/animateTransform directly on
each row's <text>), the same pattern used successfully in info-card.svg.
An earlier clip-path "wipe" version rendered blank when embedded via <img>
on GitHub, so this drops clip-path entirely in favor of the proven pattern.
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

def image_to_ascii_grid(path: str, cols: int, rows: int) -> list[str]:
    img = Image.open(path).convert("L")
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
    row_stagger = 0.035
    row_fade_dur = 0.4

    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" '
        f'width="{width:.0f}" height="{height:.0f}" font-family="Consolas, \'Courier New\', monospace">'
    )
    svg_parts.append('<rect width="100%" height="100%" fill="transparent"/>')
    svg_parts.append('<g transform="translate(10,10)">')

    for i, line in enumerate(lines):
        stripped = line.rstrip()
        if len(stripped) == 0:
            continue
        y = i * LINE_H
        start_t = i * row_stagger
        text_escaped = escape_xml(stripped)

        svg_parts.append('<g opacity="0" transform="translate(-14,0)">')
        svg_parts.append(
            f'<text x="0" y="{y + LINE_H*0.82:.2f}" font-size="{FONT_SIZE}" '
            f'fill="{FILL_COLOR}" xml:space="preserve">{text_escaped}</text>'
        )
        svg_parts.append(
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{start_t:.3f}s" dur="{row_fade_dur}s" fill="freeze"/>'
        )
        svg_parts.append(
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="-14,0" to="0,0" begin="{start_t:.3f}s" dur="{row_fade_dur}s" '
            f'fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>'
        )
        svg_parts.append('</g>')

    svg_parts.append('</g>')
    svg_parts.append('</svg>')

    with open(out_path, "w") as f:
        f.write("\n".join(svg_parts))
    total_dur = (total_rows - 1) * row_stagger + row_fade_dur
    print(f"wrote {out_path}  ({total_rows} rows, total anim ~{total_dur:.2f}s)")

if __name__ == "__main__":
    lines = image_to_ascii_grid("prepped-photo.png", COLS, ROWS)
    build_svg(lines, "avi-ascii.svg")
