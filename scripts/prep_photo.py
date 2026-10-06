"""Remove a photo background and improve local contrast for ASCII conversion."""

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def main() -> None:
    if len(sys.argv) not in (2, 3):
        raise SystemExit(
            "Usage: python scripts/prep_photo.py source-photo.jpg [--remove-background]"
        )
    source = Path(sys.argv[1])
    image = Image.open(source).convert("RGB")
    pixels = np.array(image)
    if len(sys.argv) == 3 and sys.argv[2] == "--remove-background":
        from rembg import remove

        foreground = remove(image.convert("RGBA"))
        rgba = np.array(foreground)
        alpha = rgba[:, :, 3:4] / 255.0
        white = np.full(rgba[:, :, :3].shape, 255, dtype=np.uint8)
        pixels = (rgba[:, :, :3] * alpha + white * (1 - alpha)).astype(np.uint8)
    gray = cv2.cvtColor(pixels, cv2.COLOR_RGB2GRAY)
    enhanced = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)
    Image.fromarray(enhanced).save(Path(__file__).parents[1] / "source-prepped.png")


if __name__ == "__main__":
    main()
