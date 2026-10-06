"""Convert source-prepped.png into a monochrome self-typing SVG portrait."""

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).parents[1]
RAMP = " .`:-=+*cs#%@"


def main() -> None:
    source = ROOT / "source-prepped.png"
    if not source.exists():
        raise SystemExit("Add source-photo.jpg and run prep_photo.py first.")
    image = Image.open(source).convert("L")
    width = 100
    height = max(1, round(width * image.height / image.width * 0.48))
    image = image.resize((width, height))
    pixels = np.asarray(image)
    rows = []
    for row_index, row in enumerate(pixels):
        text = "".join(RAMP[min(len(RAMP) - 1, int(value) * len(RAMP) // 256)] for value in row)
        y = 24 + row_index * 11
        rows.append(
            f'<text x="8" y="{y}" class="row" style="animation-delay:{row_index * .035:.3f}s">'
            f"{text}</text>"
        )
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 {height * 11 + 32}" role="img">',
        '<style>svg{background:#0d1117}.row{fill:#c9d1d9;font:10px monospace;white-space:pre;animation:type .7s ease-out both}@keyframes type{from{opacity:0;transform:translateX(-12px)}to{opacity:1;transform:none}}</style>',
        *rows,
        "</svg>",
    ]
    (ROOT / "avi-ascii.svg").write_text("\n".join(svg), encoding="utf-8")


if __name__ == "__main__":
    main()
