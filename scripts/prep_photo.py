#!/usr/bin/env python3
"""
Prepares an input image (photo or logo) for ASCII conversion:
- Resizes and crops to square if needed
- Handles alpha transparency
- Auto-detects dark-background logos to ensure proper ASCII density mapping
- Applies contrast stretching and tone mapping

Usage: python scripts/prep_photo.py [source-photo.png] [source-prepped.png]
"""
import os
import sys
import numpy as np
from PIL import Image, ImageOps, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

if not os.path.exists(INP):
    print(f"Error: {INP} not found.", file=sys.stderr)
    sys.exit(1)

img = Image.open(INP)

# Handle transparency if present: composite over black or white
if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
    alpha = img.convert("RGBA").split()[-1]
    bg = Image.new("RGBA", img.size, (0, 0, 0, 255))
    bg.paste(img, mask=alpha)
    img = bg.convert("RGB")
else:
    img = img.convert("RGB")

gray = ImageOps.grayscale(img)
arr = np.array(gray)

# Check average luminance: if image is mostly dark (like dark background logo), invert it
# so the logo prints as ASCII characters and background remains whitespace.
mean_lum = np.mean(arr)
if mean_lum < 110:
    gray = ImageOps.invert(gray)

# Enhance contrast
enhancer = ImageEnhance.Contrast(gray)
enhanced = enhancer.enhance(1.4)

# Square crop
w, h = enhanced.size
side = min(w, h)
left = (w - side) // 2
top = (h - side) // 2
cropped = enhanced.crop((left, top, left + side, top + side))

cropped.save(OUT)
print(f"wrote {OUT}: size {cropped.size}, ready for make_ascii_svg.py")
