#!/usr/bin/env python3
"""
fetch_contributions.py — scrape the public contribution calendar HTML
fragment GitHub serves at /users/<username>/contributions (no API token
needed) and write data/contributions.json with raw days + derived stats.
"""
import json
import re
import sys
import os
import datetime
import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_USERNAME", "AbhiiishekPandey")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")


def fetch(username: str) -> dict:
    headers = {"User-Agent": "Mozilla/5.0 (profile-readme-bot)"}
    resp = requests.get(f"https://github.com/users/{username}/contributions", headers=headers, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # GitHub's current markup: each day is a <td class="ContributionCalendar-day"
    # data-date="YYYY-MM-DD" data-level="0-4" id="...">, with the actual
    # contribution count only available in a sibling <tool-tip for="<id>">
    # whose text reads "3 contributions on April 14th." or
    # "No contributions on August 10th." — no data-count attribute anymore.
    cells = soup.select("td.ContributionCalendar-day[data-date]")
    if not cells:
        cells = soup.select("[data-date]")

    tooltip_by_id = {}
    for tip in soup.select("tool-tip[for]"):
        tooltip_by_id[tip.get("for")] = tip.get_text(strip=True)

    count_re = re.compile(r"^(No|\d+)\s+contributions?\s+on", re.IGNORECASE)

    days = []
    for cell in cells:
        date_str = cell.get("data-date")
        if date_str is None:
            continue
        level = cell.get("data-level")
        level_i = int(level) if level not in (None, "") else None

        count_i = None
        cell_id = cell.get("id")
        tip_text = tooltip_by_id.get(cell_id) if cell_id else None
        if tip_text:
            m = count_re.match(tip_text)
            if m:
                token = m.group(1)
                count_i = 0 if token.lower() == "no" else int(token)
        if count_i is None:
            # fall back to data-count if some future markup restores it,
            # else approximate from level (0 = none, 1-4 = increasing)
            count_attr = cell.get("data-count")
            count_i = int(count_attr) if count_attr not in (None, "") else (level_i or 0)

        days.append({"date": date_str, "count": count_i, "level": level_i})

    if not days:
        raise RuntimeError(
            "No contribution cells found — GitHub may have changed its markup, "
            "or the profile has no public contribution graph."
        )

    days.sort(key=lambda d: d["date"])

    # derive stats
    total = sum(d["count"] for d in days if d["count"] is not None)

    current_streak = 0
    longest_streak = 0
    running = 0
    today = datetime.date.today().isoformat()
    for d in days:
        c = d["count"] or 0
        if c > 0:
            running += 1
            longest_streak = max(longest_streak, running)
        else:
            running = 0
    # current streak = trailing run ending today/most-recent day with count>0
    for d in reversed(days):
        c = d["count"] or 0
        if c > 0:
            current_streak += 1
        else:
            break

    best_day = max(days, key=lambda d: d["count"] or 0)

    monthly = {}
    for d in days:
        month_key = d["date"][:7]
        monthly[month_key] = monthly.get(month_key, 0) + (d["count"] or 0)

    payload = {
        "username": username,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_contributions": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "monthly_totals": monthly,
        "days": days,
    }
    return payload


if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else USERNAME
    data = fetch(username)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"wrote {OUT_PATH}  ({len(data['days'])} days, {data['total_contributions']} total)")
