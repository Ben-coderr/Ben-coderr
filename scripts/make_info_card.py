#!/usr/bin/env python3
"""
Generate an animated Cyberpunk / Neo-Matrix neofetch terminal card SVG (840 x 890)
with interactive skill meters, live system status, and cyberpunk color blocks.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")

W, H = 840, 890
PAD = 24
TITLEBAR_H = 32
START_Y = TITLEBAR_H + 34
LINE_H = 34

BG = "#06090e"
BG2 = "#0d1520"
MUTED = "#64748b"
TEXT = "#e2e8f0"
CYAN = "#00f0ff"
GREEN = "#00ff88"
PURPLE = "#c084fc"
GOLD = "#fbbf24"
BLUE = "#38bdf8"

lines = [
    ("header", "ben-coderr@cyber-deck", CYAN, 22),
    ("divider", "-------------------------------------------------------------", "#1e293b", 16),
    ("status", "STATUS", "ONLINE · 🚀 BUILDING 0 → 1 STARTUP", GREEN),
    ("kv", "OS", "Arch Linux x86_64 / macOS Sonoma", BLUE),
    ("kv", "Host", "MacBook Pro (Apple Silicon M-Series)", BLUE),
    ("kv", "Role", "Fullstack Engineer & Mobile Architect", CYAN),
    ("kv", "Education", "Data Science & Machine Learning (Univ Mostaganem)", PURPLE),
    ("bar", "Frontend", "78%", "Next.js · React · Vue · Tailwind · TS", CYAN, 12, 16),
    ("bar", "Mobile",   "75%", "React Native · Flutter · Kotlin · Swift", GREEN, 12, 16),
    ("bar", "Backend",  "85%", "Node.js · NestJS · FastAPI · Python · Go", BLUE, 14, 16),
    ("bar", "Data/AI",  "76%", "PyTorch · Scikit-learn · OpenCV · Pandas", PURPLE, 12, 16),
    ("bar", "Hardware", "65%", "ESP32 · STM32 · Arduino · Raspberry Pi", GOLD, 10, 16),
    ("kv", "Databases", "PostgreSQL · Redis · MongoDB · Supabase", PURPLE),
    ("kv", "DevOps", "Docker · Linux Kernel · CI/CD · Vite · Git", GOLD),
    ("kv", "Location", "Mostaganem, Algeria 🇩🇿", MUTED),
    ("kv", "Portfolio", "https://bencoder.netlify.app", CYAN),
]

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<style>',
    '.line { opacity: 0; animation: typeLine 0.35s cubic-bezier(0.16, 1, 0.3, 1) both; }',
    '@keyframes typeLine { 0% { opacity: 0; transform: translateX(-10px); } 100% { opacity: 1; transform: translateX(0); } }',
    '@media (prefers-reduced-motion: reduce) { .line { opacity: 1 !important; transform: none !important; animation: none !important; } }',
    '</style>',
    '<defs>',
    f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0%" stop-color="{BG2}"/><stop offset="100%" stop-color="{BG}"/>'
    '</linearGradient>',
    '<linearGradient id="cyberBorder" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0%" stop-color="#00f0ff" stop-opacity="0.7"/>'
    '<stop offset="50%" stop-color="#00ff88" stop-opacity="0.3"/>'
    '<stop offset="100%" stop-color="#38bdf8" stop-opacity="0.6"/>'
    '</linearGradient>',
    '</defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="url(#cyberBorder)" stroke-width="1.5"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="#00f0ff" stroke-opacity="0.25"/>',
]

for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#00ff88"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="#5eead4" font-size="12" font-weight="600" text-anchor="middle">ben-coderr@cyber-deck: ~$ neofetch --matrix</text>')

cur_y = START_Y
for idx, item in enumerate(lines):
    delay = 0.08 * idx
    kind = item[0]
    if kind == "header":
        parts.append(f'<g class="line" style="animation-delay:{delay:.2f}s">'
                     f'<text x="{PAD+8}" y="{cur_y}" fill="{item[2]}" font-size="{item[3]}" font-weight="bold">'
                     f'{item[1]} <tspan fill="{GREEN}" font-size="14">[ACTIVE]</tspan></text></g>')
        cur_y += 20
    elif kind == "divider":
        parts.append(f'<g class="line" style="animation-delay:{delay:.2f}s">'
                     f'<text x="{PAD+8}" y="{cur_y}" fill="{item[2]}" font-size="{item[3]}">{item[1]}</text></g>')
        cur_y += 28
    elif kind == "status":
        parts.append(f'<g class="line" style="animation-delay:{delay:.2f}s">'
                     f'<rect x="{PAD+8}" y="{cur_y-16}" width="{78}" height="20" rx="4" fill="#064e3b" stroke="#00ff88" stroke-width="0.8"/>'
                     f'<text x="{PAD+14}" y="{cur_y-2}" font-size="11" font-weight="bold" fill="#00ff88">{item[1]}</text>'
                     f'<text x="{PAD+96}" y="{cur_y-2}" font-size="13" font-weight="bold" fill="{item[3]}">{item[2]}</text></g>')
        cur_y += 30
    elif kind == "kv":
        key, val, col = item[1], item[2], item[3]
        parts.append(f'<g class="line" style="animation-delay:{delay:.2f}s">'
                     f'<text x="{PAD+8}" y="{cur_y}" font-size="14" fill="{col}" font-weight="600">{key:<9} '
                     f'<tspan fill="#64748b">❯</tspan> <tspan fill="{TEXT}" font-weight="normal">{val}</tspan></text></g>')
        cur_y += LINE_H
    elif kind == "bar":
        key, pct, tags, col, filled, total_ticks = item[1], item[2], item[3], item[4], item[5], item[6]
        bar_str = "█" * filled + "░" * (total_ticks - filled)
        parts.append(f'<g class="line" style="animation-delay:{delay:.2f}s">'
                     f'<text x="{PAD+8}" y="{cur_y}" font-size="13" fill="{col}" font-weight="600">{key:<9} '
                     f'<tspan fill="#64748b">❯</tspan> <tspan fill="{col}" font-family="monospace">[{bar_str}]</tspan> '
                     f'<tspan fill="#ffffff" font-weight="bold">{pct}</tspan> '
                     f'<tspan fill="#94a3b8" font-size="12">{tags}</tspan></text></g>')
        cur_y += LINE_H

# Palette blocks at bottom
cur_y += 10
blocks_normal = ["#1e293b", "#f87171", "#34d399", "#fbbf24", "#60a5fa", "#c084fc", "#00f0ff", "#f3f4f6"]
blocks_bright = ["#334155", "#fca5a5", "#6ee7b7", "#fde68a", "#93c5fd", "#e9d5ff", "#a7f3d0", "#ffffff"]

delay = len(lines) * 0.08 + 0.1
parts.append(f'<g class="line" style="animation-delay:{delay:.2f}s">')
bx = PAD + 8
for c in blocks_normal:
    parts.append(f'<rect x="{bx}" y="{cur_y}" width="34" height="16" rx="3" fill="{c}"/>')
    bx += 42
parts.append('</g>')

cur_y += 22
delay += 0.08
parts.append(f'<g class="line" style="animation-delay:{delay:.2f}s">')
bx = PAD + 8
for c in blocks_bright:
    parts.append(f'<rect x="{bx}" y="{cur_y}" width="34" height="16" rx="3" fill="{c}"/>')
    bx += 42
parts.append('</g>')

parts.append('</svg>')
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT}: {W} x {H}, {len(svg)} bytes")
