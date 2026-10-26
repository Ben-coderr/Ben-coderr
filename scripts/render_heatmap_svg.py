#!/usr/bin/env python3
"""
Render data/contributions.json as an Executive GitHub-native contribution heatmap SVG:
- Luxury GitHub dark mode (#0d1117 / #161b22 / #30363d)
- Native GitHub contribution greens (#161b22, #0e4429, #006d32, #26a641, #39d353)
- Smooth staggered reveal animation
- Live streak and activity summary footer
"""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IN_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "contrib-heatmap.svg")

# GitHub Dark Theme Palette
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

CELL = 12
GAP = 3
STEP = CELL + GAP
PAD = 24
LEFT_LABEL_W = 30
TOP_LABEL_H = 22
TITLEBAR_H = 34

BG = "#0d1117"
BG2 = "#161b22"
FRAME = "#30363d"
MUTED = "#7d8590"
TEXT = "#e6edf3"
BLUE = "#58a6ff"
GREEN = "#39d353"
GOLD = "#d29922"

# Stagger timing (seconds)
COL_T = 0.014
ROW_T = 0.035
CELL_DUR = 0.35


def level_for(count):
    if count == 0:
        return 0
    if count <= 4:
        return 1
    if count <= 12:
        return 2
    if count <= 25:
        return 3
    return 4


def build_grid(days):
    first = datetime.date.fromisoformat(days[0]["date"])
    lead_pad = (first.weekday() + 1) % 7
    grid = []
    col = [None] * lead_pad
    for d in days:
        date = datetime.date.fromisoformat(d["date"])
        weekday = (date.weekday() + 1) % 7
        while len(col) < weekday:
            col.append(None)
        col.append((d["date"], d["count"], level_for(d["count"])))
        if len(col) == 7:
            grid.append(col)
            col = []
    if col:
        while len(col) < 7:
            col.append(None)
        grid.append(col)
    return grid


def render(data):
    days = data["days"]
    grid = build_grid(days)
    n_cols = len(grid)
    art_w = n_cols * STEP
    art_h = 7 * STEP

    month_labels = []
    seen_months = set()
    for ci, column in enumerate(grid):
        for cell in column:
            if cell is None:
                continue
            date = datetime.date.fromisoformat(cell[0])
            key = (date.year, date.month)
            if key not in seen_months and date.day <= 7:
                seen_months.add(key)
                month_labels.append((ci, date.strftime("%b")))
            break

    canvas_w = PAD + LEFT_LABEL_W + art_w + PAD
    stats_h = 80
    canvas_h = TITLEBAR_H + TOP_LABEL_H + art_h + stats_h + PAD

    css = f"""
@keyframes cellIn {{
  0%   {{ opacity: 0; transform: translateY(-4px) scale(0.7); }}
  100% {{ opacity: 1; transform: translateY(0) scale(1); }}
}}
.c {{ opacity: 0; animation: cellIn {CELL_DUR:.2f}s cubic-bezier(0.16, 1, 0.3, 1) both; }}
@media (prefers-reduced-motion: reduce) {{ .c {{ opacity: 1 !important; transform: none !important; animation: none !important; }} }}
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" '
        f'viewBox="0 0 {canvas_w} {canvas_h}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="hbg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{BG2}"/><stop offset="100%" stop-color="{BG}"/></linearGradient>',
        '</defs>',
        f'<rect width="{canvas_w}" height="{canvas_h}" rx="12" fill="url(#hbg)"/>',
        f'<rect x="0.5" y="0.5" width="{canvas_w-1}" height="{canvas_h-1}" rx="12" '
        f'fill="none" stroke="{FRAME}" stroke-width="1"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{canvas_w}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-width="1"/>',
    ]
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
    parts.append(f'<text x="{canvas_w/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" font-family="monospace" '
                 f'text-anchor="middle">abdenour@macbook ~ % ./contributions.sh</text>')

    grid_top = TITLEBAR_H + TOP_LABEL_H
    grid_left = PAD + LEFT_LABEL_W

    for ci, label in month_labels:
        x = grid_left + ci * STEP
        parts.append(f'<text x="{x}" y="{TITLEBAR_H + 16}" fill="{MUTED}" font-size="11">{label}</text>')

    for wi, wname in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = grid_top + wi * STEP + CELL * 0.78
        parts.append(f'<text x="{PAD}" y="{y:.1f}" fill="{MUTED}" font-size="10">{wname}</text>')

    for ci, column in enumerate(grid):
        gx = grid_left + ci * STEP
        for ri, cell in enumerate(column):
            if cell is None:
                continue
            date_s, count, lvl = cell
            gy = grid_top + ri * STEP
            delay = ci * COL_T + ri * ROW_T
            plural = "s" if count != 1 else ""
            stroke_attr = ' stroke="#30363d" stroke-width="0.5"' if lvl == 0 else ''
            parts.append(
                f'<rect class="c" x="{gx}" y="{gy}" width="{CELL}" height="{CELL}" rx="2.5" '
                f'fill="{PALETTE[lvl]}"{stroke_attr} style="animation-delay:{delay:.3f}s">'
                f'<title>{date_s}: {count} contribution{plural}</title></rect>'
            )

    # Legend
    leg_y = grid_top + art_h + 8
    leg_x = canvas_w - PAD - (len(PALETTE) * (CELL + 2) + 65)
    parts.append(f'<text x="{leg_x}" y="{leg_y + CELL*0.8:.1f}" fill="{MUTED}" font-size="11" text-anchor="end">Less</text>')
    lx = leg_x + 8
    for lvl, color in enumerate(PALETTE):
        s_attr = ' stroke="#30363d" stroke-width="0.5"' if lvl == 0 else ''
        parts.append(f'<rect x="{lx}" y="{leg_y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{color}"{s_attr}/>')
        lx += CELL + 3
    parts.append(f'<text x="{lx + 4}" y="{leg_y + CELL*0.8:.1f}" fill="{MUTED}" font-size="11">More</text>')

    sep_y = leg_y + CELL + 12
    parts.append(f'<line x1="{PAD}" y1="{sep_y}" x2="{canvas_w-PAD}" y2="{sep_y}" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.6"/>')

    cs = data["current_streak"]["length"]
    ls = data["longest_streak"]["length"]
    total = data["total_contributions"]
    best = data["best_day"]
    rng = data["range"]

    ly = sep_y + 22
    parts.append(f'<text x="{PAD}" y="{ly}" font-size="13.5" fill="{TEXT}">'
                 f'<tspan font-weight="700" fill="{GREEN}">{total:,}</tspan>'
                 f'<tspan fill="{MUTED}"> contributions in the last year</tspan></text>')
    parts.append(f'<text x="{canvas_w - PAD}" y="{ly}" font-size="12" font-family="monospace" fill="{MUTED}" text-anchor="end">'
                 f'{rng["start"]} &#8594; {rng["end"]}</text>')
    ly += 22
    parts.append(f'<text x="{PAD}" y="{ly}" font-size="13" fill="{MUTED}">current streak '
                 f'<tspan fill="{BLUE}" font-weight="700">{cs} days</tspan>'
                 f'<tspan fill="{MUTED}">   &#183;   longest </tspan>'
                 f'<tspan fill="{BLUE}" font-weight="700">{ls} days</tspan></text>')
    parts.append(f'<text x="{canvas_w - PAD}" y="{ly}" font-size="12" font-family="monospace" fill="{MUTED}" text-anchor="end">'
                 f'best day <tspan fill="{GOLD}" font-weight="700">{best["count"]}</tspan> commits on {best["date"]}</text>')

    parts.append("</svg>")
    return "".join(parts)


if __name__ == "__main__":
    if not os.path.exists(IN_PATH):
        print(f"Error: {IN_PATH} not found.", file=sys.stderr)
        sys.exit(1)
    data = json.load(open(IN_PATH))
    svg = render(data)
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH} ({len(svg)} bytes)")
