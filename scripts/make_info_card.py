#!/usr/bin/env python3
"""
Generate an animated neofetch-style terminal info card SVG (840 x 880)
that displays system and profile information with staggered line animations.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")

W, H = 840, 880
PAD = 24
TITLEBAR_H = 34
LINE_H = 34
START_Y = TITLEBAR_H + 38

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
TEXT = "#e6edf3"
CYAN = "#38bdf8"
GREEN = "#39d353"
GOLD = "#facc15"
PURPLE = "#c084fc"
RED = "#f87171"

lines = [
    ("header", "ben-coderr@macbook-pro", CYAN, 22, True),
    ("divider", "---------------------------------------------------", MUTED, 16, False),
    ("kv", "OS", "macOS Sonoma / Arch Linux", CYAN),
    ("kv", "Host", "MacBook Pro (Apple Silicon)", CYAN),
    ("kv", "Role", "Fullstack Engineer & Mobile Architect", CYAN),
    ("kv", "Education", "Data Science & AI (Univ Mostaganem)", CYAN),
    ("kv", "Startup", "Founder & Builder (0 -> 1 Products)", GOLD),
    ("kv", "Frontend", "React, Next.js, Vue, Tailwind, TypeScript", GREEN),
    ("kv", "Mobile", "React Native, Expo, Flutter, Kotlin, Swift", GREEN),
    ("kv", "Backend", "Node.js, NestJS, FastAPI, Python, Express", CYAN),
    ("kv", "Data/AI", "PyTorch, TensorFlow, Scikit-learn, OpenCV", PURPLE),
    ("kv", "Databases", "PostgreSQL, Redis, MongoDB, Supabase", PURPLE),
    ("kv", "DevOps", "Docker, Git, Linux, CI/CD, Vite", GOLD),
    ("kv", "Hardware", "ESP32, STM32, Arduino, Raspberry Pi, ROS", RED),
    ("kv", "Location", "Mostaganem, Algeria 🇩🇿", MUTED),
    ("kv", "Portfolio", "https://bencoder.netlify.app", CYAN),
]

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<style>',
    '.line { opacity: 0; animation: typeLine 0.4s cubic-bezier(0.16, 1, 0.3, 1) both; }',
    '@keyframes typeLine { 0% { opacity: 0; transform: translateX(-10px); } 100% { opacity: 1; transform: translateX(0); } }',
    '@media (prefers-reduced-motion: reduce) { .line { opacity: 1 !important; transform: none !important; animation: none !important; } }',
    '</style>',
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">benkorich@github: ~$ neofetch</text>')

cur_y = START_Y
for idx, item in enumerate(lines):
    delay = 0.12 * idx
    kind = item[0]
    if kind == "header":
        parts.append(f'<g class="line" style="animation-delay:{delay:.2f}s">'
                     f'<text x="{PAD+8}" y="{cur_y}" fill="{item[2]}" font-size="{item[3]}" font-weight="bold">{item[1]}</text></g>')
        cur_y += 24
    elif kind == "divider":
        parts.append(f'<g class="line" style="animation-delay:{delay:.2f}s">'
                     f'<text x="{PAD+8}" y="{cur_y}" fill="{item[2]}" font-size="{item[3]}">{item[1]}</text></g>')
        cur_y += 32
    elif kind == "kv":
        key, val, col = item[1], item[2], item[3]
        parts.append(f'<g class="line" style="animation-delay:{delay:.2f}s">'
                     f'<text x="{PAD+8}" y="{cur_y}" font-size="16" fill="{col}" font-weight="600">{key:<11} : '
                     f'<tspan fill="{TEXT}" font-weight="normal">{val}</tspan></text></g>')
        cur_y += LINE_H

# Palette blocks at bottom
cur_y += 18
blocks_normal = ["#1f242c", "#f87171", "#34d399", "#fbbf24", "#60a5fa", "#c084fc", "#38bdf8", "#f3f4f6"]
blocks_bright = ["#374151", "#fca5a5", "#6ee7b7", "#fde68a", "#93c5fd", "#e9d5ff", "#7dd3fc", "#ffffff"]

delay = len(lines) * 0.12 + 0.1
parts.append(f'<g class="line" style="animation-delay:{delay:.2f}s">')
bx = PAD + 8
for c in blocks_normal:
    parts.append(f'<rect x="{bx}" y="{cur_y}" width="34" height="18" rx="3" fill="{c}"/>')
    bx += 42
parts.append('</g>')

cur_y += 24
delay += 0.1
parts.append(f'<g class="line" style="animation-delay:{delay:.2f}s">')
bx = PAD + 8
for c in blocks_bright:
    parts.append(f'<rect x="{bx}" y="{cur_y}" width="34" height="18" rx="3" fill="{c}"/>')
    bx += 42
parts.append('</g>')

parts.append('</svg>')
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT}: {W} x {H}, {len(svg)} bytes")
