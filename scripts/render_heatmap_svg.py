#!/usr/bin/env python3
"""
render_heatmap_svg.py — draw data/contributions.json as the classic
53-week x 7-day calendar of rounded boxes, with a diagonal line-after-line
slide-down reveal (CSS keyframes, plays once on load, then freezes).
"""
import json
import os
import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "contrib-heatmap.svg")

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
# index 0 = no contributions ... index 4 = GitHub's top tier, 5 = neon accent
# reserved for the single best day of the year

CELL = 11
GAP = 3
CELL_STEP = CELL + GAP
LEFT_PAD = 30      # room for day-of-week labels
TOP_PAD = 22       # room for month labels
RIGHT_PAD = 12
BOTTOM_PAD = 56    # room for legend + stats footer

BG = "transparent"
TEXT_COLOR = "#8b949e"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
WEEKDAY_LABELS = {1: "Mon", 3: "Wed", 5: "Fri"}  # Mon=0 offset shown sparsely


def load_data():
    with open(DATA_PATH) as f:
        return json.load(f)


def build_weeks(days):
    """Bucket days into GitHub-style Sunday-first weeks (columns)."""
    by_date = {d["date"]: d for d in days}
    dates = sorted(by_date.keys())
    first = datetime.date.fromisoformat(dates[0])
    last = datetime.date.fromisoformat(dates[-1])

    # walk back first date to the preceding Sunday so week columns align
    start = first - datetime.timedelta(days=(first.weekday() + 1) % 7)

    weeks = []
    cur = start
    week = []
    while cur <= last:
        key = cur.isoformat()
        entry = by_date.get(key, {"date": key, "count": 0, "level": 0})
        week.append(entry)
        if len(week) == 7:
            weeks.append(week)
            week = []
        cur += datetime.timedelta(days=1)
    if week:
        while len(week) < 7:
            week.append(None)
        weeks.append(week)
    return weeks


def level_color(entry, best_date):
    if entry is None or not entry.get("count"):
        return PALETTE[0]
    if entry["date"] == best_date:
        return PALETTE[5]
    level = entry.get("level")
    if level is None:
        level = 1
    level = max(1, min(4, level))
    return PALETTE[level]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(data):
    days = data["days"]
    weeks = build_weeks(days)
    n_weeks = len(weeks)
    best_date = data["best_day"]["date"]

    width = LEFT_PAD + n_weeks * CELL_STEP + RIGHT_PAD
    height = TOP_PAD + 7 * CELL_STEP + BOTTOM_PAD

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" font-family="Consolas, \'Courier New\', monospace">'
    )
    parts.append(f'<rect width="100%" height="100%" fill="{BG}"/>')
    parts.append("<style>")
    parts.append("""
      .cell { animation: reveal 0.5s cubic-bezier(.25,.1,.25,1) both; }
      @keyframes reveal {
        0%   { opacity: 0; transform: translate(-6px, -6px); }
        100% { opacity: 1; transform: translate(0, 0); }
      }
    """)
    parts.append("</style>")

    # month labels: place a label above the first week-column that starts a new month
    last_month = None
    for wi, week in enumerate(weeks):
        first_valid = next((d for d in week if d is not None), None)
        if first_valid is None:
            continue
        dt = datetime.date.fromisoformat(first_valid["date"])
        if dt.day <= 7 and dt.month != last_month:
            x = LEFT_PAD + wi * CELL_STEP
            parts.append(
                f'<text x="{x}" y="{TOP_PAD - 8}" font-size="10" fill="{TEXT_COLOR}">{MONTHS[dt.month-1]}</text>'
            )
            last_month = dt.month

    # weekday labels (Mon/Wed/Fri) — row index 1,3,5 (Sunday-first grid)
    for row, label in WEEKDAY_LABELS.items():
        y = TOP_PAD + row * CELL_STEP + CELL * 0.8
        parts.append(f'<text x="0" y="{y:.1f}" font-size="9" fill="{TEXT_COLOR}">{label}</text>')

    # cells, diagonal stagger: delay increases with (week + row)
    stagger = 0.012
    for wi, week in enumerate(weeks):
        for ri, entry in enumerate(week):
            if entry is None:
                continue
            x = LEFT_PAD + wi * CELL_STEP
            y = TOP_PAD + ri * CELL_STEP
            color = level_color(entry, best_date)
            delay = (wi + ri) * stagger
            count = entry.get("count") or 0
            date_label = entry["date"]
            title = f'{count} contribution{"s" if count != 1 else ""} on {date_label}'
            parts.append(
                f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                f'rx="2.5" fill="{color}" style="animation-delay:{delay:.3f}s">'
                f'<title>{esc(title)}</title></rect>'
            )

    # legend: Less [boxes] More
    legend_y = TOP_PAD + 7 * CELL_STEP + 20
    legend_x = LEFT_PAD
    parts.append(f'<text x="{legend_x}" y="{legend_y+8:.0f}" font-size="10" fill="{TEXT_COLOR}">Less</text>')
    lx = legend_x + 32
    for i in range(5):
        parts.append(
            f'<rect x="{lx}" y="{legend_y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{PALETTE[i]}"/>'
        )
        lx += CELL_STEP
    parts.append(f'<text x="{lx+4}" y="{legend_y+8:.0f}" font-size="10" fill="{TEXT_COLOR}">More</text>')

    # stats footer
    stats_y = legend_y + 24
    total = data["total_contributions"]
    longest = data["longest_streak"]
    stats_text = f"{total} contributions in the last year  \u00b7  longest streak {longest} days"
    parts.append(
        f'<text x="{LEFT_PAD}" y="{stats_y:.0f}" font-size="11" fill="{TEXT_COLOR}">{esc(stats_text)}</text>'
    )

    parts.append("</svg>")

    with open(OUT_PATH, "w") as f:
        f.write("\n".join(parts))
    print(f"wrote {OUT_PATH}  ({n_weeks} weeks x 7 days, {total} contributions)")


if __name__ == "__main__":
    data = load_data()
    build_svg(data)
