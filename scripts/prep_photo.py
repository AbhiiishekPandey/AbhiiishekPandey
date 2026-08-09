#!/usr/bin/env python3
"""
prep_photo.py — turn a normal headshot into a clean, high-contrast
grayscale image that converts nicely to ASCII.

Usage:
    python scripts/prep_photo.py source-photo.png
Output:
    prepped-photo.png  (grayscale, background removed -> white, CLAHE contrast)
"""
import sys
import io
import numpy as np
import cv2
from PIL import Image
from rembg import remove

def prep(src_path: str, out_path: str = "prepped-photo.png"):
    with open(src_path, "rb") as f:
        input_bytes = f.read()

    # 1. Remove background -> RGBA with subject isolated
    result_bytes = remove(input_bytes)
    fg = Image.open(io.BytesIO(result_bytes)).convert("RGBA")

    # 2. Composite onto pure white so background maps to blank ASCII glyph
    white_bg = Image.new("RGBA", fg.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, fg).convert("RGB")

    # 3. Convert to grayscale, boost local contrast with CLAHE
    gray = cv2.cvtColor(np.array(composited), cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    contrasted = clahe.apply(gray)

    # 4. Re-flatten near-white background to pure white (CLAHE can mottle it)
    mask = contrasted > 245
    contrasted[mask] = 255

    Image.fromarray(contrasted).save(out_path)
    print(f"wrote {out_path}  ({contrasted.shape[1]}x{contrasted.shape[0]})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python prep_photo.py <source-photo>")
        sys.exit(1)
    prep(sys.argv[1])
