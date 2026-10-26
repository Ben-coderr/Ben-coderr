#!/usr/bin/env python3
"""
Generate profile-card.svg:
Executive developer identity card matching stats.svg in dimensions (840x880),
color system (#0d1117 / #161b22 / #30363d), and typography.
Features the authentic AB monogram logo, structured spec cards, and engineering specs.
"""
import base64
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.join(HERE, "..")
PHOTO_PATH = os.path.join(REPO_ROOT, "source-photo.png")
OUT_PATH = os.path.join(REPO_ROOT, "profile-card.svg")

W, H = 840, 880
PAD = 24
FRAME = "#30363d"
BG = "#0d1117"
BG2 = "#161b22"
CARD_BG = "#161b22"
MUTED = "#7d8590"
TEXT = "#e6edf3"
BLUE = "#58a6ff"
GREEN = "#39d353"
PURPLE = "#bc8cff"
GOLD = "#d29922"

def get_photo_b64():
    if os.path.exists(PHOTO_PATH):
        with open(PHOTO_PATH, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
            return f"data:image/png;base64,{data}"
    return ""

def render():
    photo_b64 = get_photo_b64()

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
               f'font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif">')
    
    # CSS animations
    svg.append('''<style>
.f { opacity: 0; animation: fadeIn 0.45s ease-out both; }
@keyframes fadeIn { 0% { opacity: 0; transform: translateY(10px); } 100% { opacity: 1; transform: translateY(0); } }
@media (prefers-reduced-motion: reduce) { .f { opacity: 1 !important; transform: none !important; animation: none !important; } }
</style>''')

    # Defs
    svg.append('<defs>')
    svg.append(f'<linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">'
               f'<stop offset="0%" stop-color="{BG2}"/><stop offset="100%" stop-color="{BG}"/></linearGradient>')
    svg.append('<clipPath id="avatarClip"><rect x="28" y="56" width="100" height="100" rx="20"/></clipPath>')
    svg.append('</defs>')

    # Window Container
    svg.append(f'<rect width="{W}" height="{H}" rx="12" fill="url(#bgGrad)"/>')
    svg.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>')

    # Title bar (matching stats.svg exactly)
    TITLEBAR_H = 34
    svg.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-width="1"/>')
    for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        svg.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')
    svg.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" font-family="monospace" '
               f'text-anchor="middle">abdenour@macbook ~ % whoami</text>')

    # Header / Hero Section (y=56 to y=180)
    svg.append('<g class="f" style="animation-delay:0.05s">')
    svg.append(f'<rect x="26" y="54" width="104" height="104" rx="22" fill="none" stroke="{BLUE}" stroke-width="1.5" stroke-opacity="0.8"/>')
    if photo_b64:
        svg.append(f'<image href="{photo_b64}" x="28" y="56" width="100" height="100" clip-path="url(#avatarClip)"/>')
    else:
        svg.append(f'<rect x="28" y="56" width="100" height="100" rx="20" fill="#21262d"/>')
        svg.append(f'<text x="78" y="115" fill="{BLUE}" font-size="32" font-weight="700" text-anchor="middle">AB</text>')

    # Identity details
    svg.append(f'<text x="150" y="86" fill="{TEXT}" font-size="25" font-weight="700">Abdenour Benkorich</text>')
    svg.append(f'<text x="150" y="112" fill="{BLUE}" font-size="15" font-weight="600">Fullstack Engineer &amp; Mobile Architect</text>')
    svg.append(f'<text x="150" y="132" fill="{MUTED}" font-size="13">@Ben-coderr · Mostaganem, Algeria 🇩🇿 (UTC+1)</text>')

    # Availability pill
    svg.append(f'<rect x="150" y="142" width="295" height="24" rx="12" fill="#1c2128" stroke="{FRAME}" stroke-width="1"/>')
    svg.append(f'<circle cx="164" cy="154" r="4.5" fill="{GREEN}"/>')
    svg.append(f'<text x="176" y="158" fill="{TEXT}" font-size="11.5" font-weight="500">Available for High-Impact Roles &amp; Ventures</text>')
    svg.append('</g>')

    # Section Divider
    svg.append(f'<line x1="{PAD}" y1="184" x2="{W-PAD}" y2="184" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.6"/>')

    # Grid of 4 modular cards (Row 1 & Row 2)
    GRID_Y = 200
    CARD_W = 388
    CARD_H1 = 160
    GAP_X = 16
    GAP_Y = 16
    COL1_X = PAD
    COL2_X = PAD + CARD_W + GAP_X

    # Card 1: Specializations (Row 1, Col 1)
    svg.append(f'<g class="f" style="animation-delay:0.15s">')
    svg.append(f'<rect x="{COL1_X}" y="{GRID_Y}" width="{CARD_W}" height="{CARD_H1}" rx="10" fill="{CARD_BG}" stroke="{FRAME}" stroke-width="1"/>')
    svg.append(f'<text x="{COL1_X+20}" y="{GRID_Y+30}" fill="{BLUE}" font-family="monospace" font-size="13" font-weight="700">// CORE SPECIALIZATIONS</text>')
    specs1 = [
        ("Fullstack Web", "React · Next.js · TypeScript · Tailwind"),
        ("Mobile Systems", "React Native · Flutter · Native APIs"),
        ("Backend &amp; APIs", "FastAPI · NestJS · Node.js · Express"),
    ]
    for idx, (label, val) in enumerate(specs1):
        cy = GRID_Y + 62 + idx * 32
        svg.append(f'<text x="{COL1_X+20}" y="{cy}" fill="{MUTED}" font-size="12" font-family="monospace">{label}:</text>')
        svg.append(f'<text x="{COL1_X+124}" y="{cy}" fill="{TEXT}" font-size="12.5" font-weight="500">{val}</text>')
    svg.append('</g>')

    # Card 2: AI & Embedded (Row 1, Col 2)
    svg.append(f'<g class="f" style="animation-delay:0.25s">')
    svg.append(f'<rect x="{COL2_X}" y="{GRID_Y}" width="{CARD_W}" height="{CARD_H1}" rx="10" fill="{CARD_BG}" stroke="{FRAME}" stroke-width="1"/>')
    svg.append(f'<text x="{COL2_X+20}" y="{GRID_Y+30}" fill="{PURPLE}" font-family="monospace" font-size="13" font-weight="700">// INTELLIGENCE &amp; ROBOTICS</text>')
    specs2 = [
        ("Deep Learning", "PyTorch · TensorFlow · OpenCV · Vision"),
        ("Data Science", "Scikit-Learn · Pandas · NumPy · EDA"),
        ("Embedded IoT", "ESP32 · STM32 · Arduino · ROS · Sensors"),
    ]
    for idx, (label, val) in enumerate(specs2):
        cy = GRID_Y + 62 + idx * 32
        svg.append(f'<text x="{COL2_X+20}" y="{cy}" fill="{MUTED}" font-size="12" font-family="monospace">{label}:</text>')
        svg.append(f'<text x="{COL2_X+124}" y="{cy}" fill="{TEXT}" font-size="12.5" font-weight="500">{val}</text>')
    svg.append('</g>')

    # Row 2
    GRID_Y2 = GRID_Y + CARD_H1 + GAP_Y
    CARD_H2 = 160

    # Card 3: Academics & Ventures (Row 2, Col 1)
    svg.append(f'<g class="f" style="animation-delay:0.35s">')
    svg.append(f'<rect x="{COL1_X}" y="{GRID_Y2}" width="{CARD_W}" height="{CARD_H2}" rx="10" fill="{CARD_BG}" stroke="{FRAME}" stroke-width="1"/>')
    svg.append(f'<text x="{COL1_X+20}" y="{GRID_Y2+30}" fill="{GREEN}" font-family="monospace" font-size="13" font-weight="700">// ACADEMICS &amp; VENTURES</text>')
    specs3 = [
        ("Education", "Data Science &amp; AI @ Univ Mostaganem"),
        ("Ventures", "Founder · 0 → 1 Product Stealth Startup"),
        ("Methodology", "Rapid Prototyping · Clean Architecture"),
    ]
    for idx, (label, val) in enumerate(specs3):
        cy = GRID_Y2 + 62 + idx * 32
        svg.append(f'<text x="{COL1_X+20}" y="{cy}" fill="{MUTED}" font-size="12" font-family="monospace">{label}:</text>')
        svg.append(f'<text x="{COL1_X+124}" y="{cy}" fill="{TEXT}" font-size="12.5" font-weight="500">{val}</text>')
    svg.append('</g>')

    # Card 4: Tooling & Infra (Row 2, Col 2)
    svg.append(f'<g class="f" style="animation-delay:0.45s">')
    svg.append(f'<rect x="{COL2_X}" y="{GRID_Y2}" width="{CARD_W}" height="{CARD_H2}" rx="10" fill="{CARD_BG}" stroke="{FRAME}" stroke-width="1"/>')
    svg.append(f'<text x="{COL2_X+20}" y="{GRID_Y2+30}" fill="{GOLD}" font-family="monospace" font-size="13" font-weight="700">// TOOLING &amp; ENVIRONMENT</text>')
    specs4 = [
        ("OS / Kernel", "macOS (Apple Silicon) · Linux / POSIX"),
        ("Workstation", "Ghostty · zsh · Neovim · VS Code"),
        ("Database/CI", "PostgreSQL · Redis · Docker · GitHub Actions"),
    ]
    for idx, (label, val) in enumerate(specs4):
        cy = GRID_Y2 + 62 + idx * 32
        svg.append(f'<text x="{COL2_X+20}" y="{cy}" fill="{MUTED}" font-size="12" font-family="monospace">{label}:</text>')
        svg.append(f'<text x="{COL2_X+124}" y="{cy}" fill="{TEXT}" font-size="12.5" font-weight="500">{val}</text>')
    svg.append('</g>')

    # Row 3: Wide Engineering Card (Row 3, Full Width)
    CARD_W_WIDE = W - PAD * 2
    GRID_Y3 = GRID_Y2 + CARD_H2 + GAP_Y
    CARD_H3 = 240

    svg.append(f'<g class="f" style="animation-delay:0.55s">')
    svg.append(f'<rect x="{PAD}" y="{GRID_Y3}" width="{CARD_W_WIDE}" height="{CARD_H3}" rx="10" fill="{CARD_BG}" stroke="{FRAME}" stroke-width="1"/>')
    svg.append(f'<text x="{PAD+20}" y="{GRID_Y3+32}" fill="{MUTED}" font-family="monospace" font-size="13" font-weight="700">$ cat ~/.engineering_principles</text>')

    quote_lines = [
        "\"Architecting resilient, production-grade applications from first principles.",
        " Bridging artificial intelligence research with scalable, high-velocity UX.\""
    ]
    for q_idx, q_line in enumerate(quote_lines):
        svg.append(f'<text x="{PAD+20}" y="{GRID_Y3+66 + q_idx*24}" fill="{TEXT}" font-size="14" font-style="italic">{q_line}</text>')

    # Tech stack pill badges inside Card 3
    svg.append(f'<text x="{PAD+20}" y="{GRID_Y3+135}" fill="{MUTED}" font-family="monospace" font-size="12" font-weight="600">LANGUAGES &amp; RUNTIMES:</text>')
    
    tags = [
        ("TypeScript", BLUE),
        ("Python", "#3572A5"),
        ("JavaScript", "#f1e05a"),
        ("Dart", "#00B4AB"),
        ("Kotlin", "#A97BFF"),
        ("C++", "#f34b7d"),
        ("SQL", "#e38c00"),
        ("Swift", "#F05138")
    ]
    cur_x = PAD + 20
    tag_y = GRID_Y3 + 148
    for name, col in tags:
        tw = len(name) * 8 + 20
        svg.append(f'<rect x="{cur_x}" y="{tag_y}" width="{tw}" height="24" rx="12" fill="#21262d" stroke="{FRAME}" stroke-width="1"/>')
        svg.append(f'<circle cx="{cur_x+10}" cy="{tag_y+12}" r="3.5" fill="{col}"/>')
        svg.append(f'<text x="{cur_x+18}" y="{tag_y+16}" fill="{TEXT}" font-size="11" font-weight="600">{name}</text>')
        cur_x += tw + 8

    # Contact & Links row inside wide card
    svg.append(f'<line x1="{PAD+20}" y1="{GRID_Y3+190}" x2="{W-PAD-20}" y2="{GRID_Y3+190}" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.4"/>')
    svg.append(f'<text x="{PAD+20}" y="{GRID_Y3+215}" fill="{MUTED}" font-size="12" font-family="monospace">PORTFOLIO: <tspan fill="{BLUE}">bencoder.netlify.app</tspan>   EMAIL: <tspan fill="{TEXT}">ben.coder.01@gmail.com</tspan></text>')
    svg.append(f'<text x="{W-PAD-20}" y="{GRID_Y3+215}" fill="{MUTED}" font-size="12" font-family="monospace" text-anchor="end">STATUS: <tspan fill="{GREEN}">ONLINE</tspan></text>')
    svg.append('</g>')

    # Bottom status bar (matching stats.svg)
    BOT_Y = H - 32
    svg.append(f'<line x1="{PAD}" y1="{BOT_Y-10}" x2="{W-PAD}" y2="{BOT_Y-10}" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.5"/>')
    
    # 8 ANSI terminal color swatches
    ansi_colors = ["#21262d", "#f85149", "#3fb950", "#d29922", "#58a6ff", "#bc8cff", "#39c5cf", "#e6edf3"]
    for i, col in enumerate(ansi_colors):
        svg.append(f'<rect x="{PAD + i*32}" y="{BOT_Y}" width="24" height="14" rx="3" fill="{col}"/>')
        
    svg.append(f'<text x="{W-PAD}" y="{BOT_Y+11}" font-family="monospace" font-size="11" fill="{MUTED}" text-anchor="end">Terminal: Ghostty · Shell: zsh · Platform: Darwin arm64</text>')

    svg.append('</svg>')
    return "".join(svg)

if __name__ == "__main__":
    out = render()
    with open(OUT_PATH, "w") as f:
        f.write(out)
    print(f"Generated professional profile-card.svg: {len(out)} bytes, size: {W} x {H}")
