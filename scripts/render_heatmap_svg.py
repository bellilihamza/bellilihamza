"""Render contribution JSON as an animated, self-contained SVG."""

import json
from pathlib import Path

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
ROOT = Path(__file__).parents[1]


def main() -> None:
    data = json.loads((ROOT / "data" / "contributions.json").read_text(encoding="utf-8"))
    days = data["days"][-371:]
    width, height = 860, 150
    cell, gap = 12, 3
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">',
        "<style>@keyframes reveal{from{opacity:0;transform:translate(-5px,-5px)}to{opacity:1;transform:none}}"
        ".day{animation:reveal .35s ease-out both}.label{fill:#8b949e;font:11px monospace}</style>",
        '<rect width="100%" height="100%" rx="10" fill="#0d1117"/>',
    ]
    for index, item in enumerate(days):
        x = 22 + (index // 7) * (cell + gap)
        y = 22 + (index % 7) * (cell + gap)
        delay = (index % 53) * 0.018
        color = PALETTE[min(max(int(item["level"]), 0), len(PALETTE) - 1)]
        parts.append(
            f'<rect class="day" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" '
            f'fill="{color}" style="animation-delay:{delay:.3f}s"><title>{item["date"]}: '
            f'{item["count"]} contributions</title></rect>'
        )
    total = f'{data["total"]:,}'
    parts.extend(
        [
            '<text class="label" x="22" y="132">Less</text>',
            '<text class="label" x="782" y="132">More</text>',
            f'<text class="label" x="22" y="147">{total} contributions in the last year · '
            f'{data["current_streak"]} day current streak</text>',
        ]
    )
    parts.append("</svg>")
    (ROOT / "contrib-heatmap.svg").write_text("\n".join(parts), encoding="utf-8")


if __name__ == "__main__":
    main()
