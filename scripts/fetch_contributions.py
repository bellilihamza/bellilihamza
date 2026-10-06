"""Fetch a user's public GitHub contribution calendar without an API token."""

import json
import re
from datetime import date, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "bellilihamza"
OUTPUT = Path(__file__).parents[1] / "data" / "contributions.json"


def parse_date(value: str) -> date:
    return date.fromisoformat(value)


def main() -> None:
    url = f"https://github.com/users/{USERNAME}/contributions"
    response = requests.get(url, timeout=30, headers={"User-Agent": "profile-art-refresh"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    days = []
    for cell in soup.select("td.ContributionCalendar-day[data-date]"):
        raw_count = cell.get("data-count", "0")
        match = re.search(r"\d+", raw_count)
        count = int(match.group()) if match else 0
        days.append(
            {
                "date": cell["data-date"],
                "count": count,
                "level": int(cell.get("data-level", "0")),
            }
        )

    if not days:
        raise RuntimeError("GitHub returned no contribution cells; the page format may have changed.")

    days.sort(key=lambda item: item["date"])
    counts = [item["count"] for item in days]
    current_streak = 0
    cursor = date.today()
    by_date = {parse_date(item["date"]): item["count"] for item in days}
    while by_date.get(cursor, 0) > 0:
        current_streak += 1
        cursor -= timedelta(days=1)

    longest_streak = best_streak = 0
    for item in days:
        if item["count"] > 0:
            best_streak += 1
            longest_streak = max(longest_streak, best_streak)
        else:
            best_streak = 0

    payload = {
        "username": USERNAME,
        "generated_at": date.today().isoformat(),
        "days": days,
        "total": sum(counts),
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": max(counts),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
