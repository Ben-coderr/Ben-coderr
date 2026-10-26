#!/usr/bin/env python3
"""
Convert an avatar / portrait into a clean Cyberpunk / Neo-Matrix ASCII-art SVG
with a terminal window frame, typing animation row-by-row, and a blinking cursor.

Usage: python scripts/make_ascii_svg.py [source-photo.png] [output.svg]
"""
import html
import os
import sys
from PIL import Image, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "ben-ascii.svg")

COLS = int(os.environ.get("COLS", 140))
ART_W_TARGET = 800
CELL_W = ART_W_TARGET / COLS
CELL_H = CELL_W * 15 / 8
ROWS = round(COLS * 8 / 15)

PAD = 20
TITLEBAR_H = 32
STATUS_H = 34
ART_W = COLS * CELL_W
ART_H = ROWS * CELL_H
CANVAS_W = ART_W + PAD * 2
CANVAS_H = TITLEBAR_H + ART_H + STATUS_H + PAD

BG = "#06090e"
BG2 = "#0d1520"
TITLE_TEXT = "#5eead4"
CURSOR = "#00f0ff"

ROW_DUR = 5.2 / ROWS
STAGGER = ROW_DUR

if not os.path.exists(SRC):
    alt = os.path.join(HERE, "..", "source-prepped.png")
    if os.path.exists(alt):
        SRC = alt
    else:
        print(f"Error: {SRC} not found.", file=sys.stderr)
        sys.exit(1)

im = Image.open(SRC).convert("L")
im = ImageEnhance.Contrast(im).enhance(1.25)
im = ImageEnhance.Brightness(im).enhance(1.05)
im = im.resize((COLS, ROWS), Image.LANCZOS)
px = im.load()

STATIC = bool(os.environ.get("STATIC"))
RAMP = " .`:-=+*#%@"

rows_txt = []
for y in range(ROWS):
    chars = []
    for x in range(COLS):
        lum = px[x, y] / 255.0
        if lum < 0.08:
            chars.append(" ")
        else:
            idx = int(lum * (len(RAMP) - 1) + 0.5)
            idx = max(0, min(len(RAMP) - 1, idx))
            chars.append(RAMP[idx])
    rows_txt.append("".join(chars))

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>',
    f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0%" stop-color="{BG2}"/><stop offset="100%" stop-color="{BG}"/>'
    '</linearGradient>',
    '<linearGradient id="cyberBorder" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0%" stop-color="#00f0ff" stop-opacity="0.7"/>'
    '<stop offset="50%" stop-color="#00ff88" stop-opacity="0.3"/>'
    '<stop offset="100%" stop-color="#38bdf8" stop-opacity="0.6"/>'
    '</linearGradient>',
    '<linearGradient id="textGrad" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0%" stop-color="#38bdf8"/><stop offset="100%" stop-color="#a7f3d0"/>'
    '</linearGradient>',
    '</defs>',
    f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="url(#cyberBorder)" stroke-width="1.5"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="#00f0ff" stroke-opacity="0.25"/>',
]

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#00ff88"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" font-weight="600" text-anchor="middle">ben-coderr@cyber-deck: ~$ ./neural_avatar.sh</text>')

art_top = TITLEBAR_H + PAD * 0.35
font_size = CELL_H * 0.88
for ry, line in enumerate(rows_txt):
    y = art_top + ry * CELL_H + CELL_H * 0.74
    row_y = art_top + ry * CELL_H
    delay = ry * STAGGER
    safe = html.escape(line)
    text = (f'<text xml:space="preserve" x="{PAD}" y="{y:.1f}" fill="url(#textGrad)" '
            f'font-size="{font_size:.1f}" textLength="{ART_W}" lengthAdjust="spacing">{safe}</text>')

    if STATIC:
        parts.append(text)
        continue

    parts.append(
        f'<clipPath id="r{ry}"><rect x="{PAD}" y="{row_y:.1f}" height="{CELL_H}" width="0">'
        f'<animate attributeName="width" from="0" to="{ART_W}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
    )
    parts.append(f'<g clip-path="url(#r{ry})">{text}</g>')
    parts.append(
        f'<rect y="{row_y+1:.1f}" width="{CELL_W*1.5}" height="{CELL_H-2}" fill="{CURSOR}" opacity="0">'
        f'<animate attributeName="x" from="{PAD}" to="{PAD+ART_W}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0.9" begin="{delay:.3f}s"/>'
        f'<set attributeName="opacity" to="0" begin="{delay+ROW_DUR:.3f}s"/></rect>'
    )

status_line_y = TITLEBAR_H + ART_H + PAD * 0.35
status_y = status_line_y + 22
parts.append(f'<line x1="0" y1="{status_line_y:.1f}" x2="{CANVAS_W}" y2="{status_line_y:.1f}" stroke="#00f0ff" stroke-opacity="0.2"/>')
parts.append(f'<text x="{PAD}" y="{status_y:.1f}" fill="{TITLE_TEXT}" font-size="13">'
             f'ben@matrix:~$ whoami <tspan fill="#00ff88" font-weight="bold">Abdenour Benkorich</tspan> '
             f'<tspan fill="#38bdf8">[CYBER/ARCHITECT]</tspan></text>')
status_chars = len("ben@matrix:~$ whoami Abdenour Benkorich [CYBER/ARCHITECT] ")
parts.append(f'<rect x="{PAD + status_chars * 13 * 0.58:.1f}" y="{status_y-12:.1f}" width="8" height="14" fill="#00f0ff">'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="0.8s" repeatCount="indefinite"/></rect>')

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT}: {CANVAS_W} x {CANVAS_H}, {len(svg)} bytes")
