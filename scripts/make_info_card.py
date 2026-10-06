"""Generate the neofetch-style profile information card."""

import os
from pathlib import Path

ROOT = Path(__file__).parents[1]
LINES = [
    ("Now", "Building useful things"),
    ("Prev", "Always learning"),
    ("Stack", "Python · TypeScript · Cloud"),
    ("Focus", "Clean systems and good UX"),
]


def main() -> None:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 490 270" role="img">',
        "<style>.bg{fill:#0d1117}.title{fill:#f0f6fc;font:bold 18px monospace}.key{fill:#69f0a0;font:bold 14px monospace}.value{fill:#c9d1d9;font:14px monospace}.line{animation:show .5s ease-out both}@keyframes show{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}</style>",
        '<rect class="bg" width="490" height="270" rx="10"/>',
        '<text class="title" x="28" y="42">bellilihamza@github</text>',
        '<path stroke="#30363d" d="M28 58h434"/>',
    ]
    for index, (key, value) in enumerate(LINES):
        y = 94 + index * 34
        animation = "" if os.getenv("STATIC") else f' style="animation-delay:{index * 0.12:.2f}s"'
        parts.append(
            f'<g class="line"{animation}><text class="key" x="28" y="{y}">{key:10}</text>'
            f'<text class="value" x="145" y="{y}">{value}</text></g>'
        )
    parts.append("</svg>")
    (ROOT / "info-card.svg").write_text("\n".join(parts), encoding="utf-8")


if __name__ == "__main__":
    main()
