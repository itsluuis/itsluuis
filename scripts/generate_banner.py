#!/usr/bin/env python3
"""
Generate Cyberpunk / Terminal profile banners for itsluuis
Creates:
  - assets/banner-dark-lily.svg (Spider Lily in Crimson Neon)
  - assets/banner-dark-moon.svg (Moon in Cyan-White)
"""

import math
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

ROOT = Path(r"c:\Users\HP\Documents\Vs Code\apps\Yio")
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

IMG_MOON = Path(r"C:\Users\HP\.gemini\antigravity-ide\brain\eb81df58-e168-4112-b5d1-bdfe1169dce3\.user_uploaded\media_1789442615209.jpg")
IMG_LILY = Path(r"C:\Users\HP\.gemini\antigravity-ide\brain\eb81df58-e168-4112-b5d1-bdfe1169dce3\.user_uploaded\media_1789442615318.jpg")

W, H = 1180, 610

INFO_ROWS = [
    ("Subject", "Lu"),
    ("Role", "Frontend Developer · UI/UX Architect"),
    ("Origin", "Portugal"),
    ("Status", "Building Financial App + Learning Mechatronics Fundamentals"),
    ("ToolChain", "VS Code · Antigravity · Cosmos · Git"),
    ("Core.Lang", "TypeScript · Python"),
    ("Core.Focus", "Personal Finance App Architecture"),
    ("Grid.LinkedIn", "/in/luis-carlos-rodrigues-garcia"),
    ("Grid.GitHub", "itsluuis"),
    ("Grid.Instagram", "@luuis_inrl"),
]

def floyd_steinberg_dither(gray_arr: np.ndarray) -> np.ndarray:
    """Serpentine Floyd-Steinberg dithering. Returns boolean mask of lit pixels."""
    work = gray_arr.astype(np.float32) / 255.0
    h, w = work.shape
    out = np.zeros((h, w), dtype=bool)
    
    for y in range(h):
        left_to_right = (y % 2 == 0)
        xs = range(w) if left_to_right else range(w - 1, -1, -1)
        direction = 1 if left_to_right else -1
        
        for x in xs:
            old_val = work[y, x]
            new_val = 1.0 if old_val >= 0.45 else 0.0
            out[y, x] = bool(new_val)
            err = old_val - new_val
            
            nx = x + direction
            if 0 <= nx < w:
                work[y, nx] += err * (7.0 / 16.0)
            if y + 1 < h:
                if 0 <= x - direction < w:
                    work[y + 1, x - direction] += err * (3.0 / 16.0)
                work[y + 1, x] += err * (5.0 / 16.0)
                if 0 <= nx < w:
                    work[y + 1, nx] += err * (1.0 / 16.0)
                    
    return out

def process_spider_lily(img_path: Path, target_w=340, target_h=370):
    img = Image.open(img_path).convert("RGB")
    # Red spider lily: the flower is crimson red on black.
    # To get maximum floral detail, use a weighted combination of Red and Green channels
    r, g, b = img.split()
    r_arr = np.asarray(r, dtype=np.float32)
    g_arr = np.asarray(g, dtype=np.float32)
    b_arr = np.asarray(b, dtype=np.float32)
    # Flower intensity map:
    intensity = np.clip(r_arr * 1.3 - g_arr * 0.2 - b_arr * 0.2, 0, 255).astype(np.uint8)
    gray = Image.fromarray(intensity, "L")
    
    # Resize to fit VISUAL.MAP
    gray = gray.resize((target_w, target_h), Image.Resampling.LANCZOS)
    gray = ImageEnhance.Contrast(gray).enhance(1.6)
    gray = gray.filter(ImageFilter.UnsharpMask(radius=2, percent=160, threshold=2))
    
    bits = floyd_steinberg_dither(np.asarray(gray))
    ys, xs = np.where(bits)
    return xs, ys

def process_moon(img_path: Path, target_w=320, target_h=370):
    img = Image.open(img_path).convert("L")
    # Center crop the moon nicely
    w, h = img.size
    # Crop to focus on the moon crescent
    crop = img.crop((0, int(h * 0.05), w, int(h * 0.95)))
    crop = crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
    crop = ImageEnhance.Contrast(crop).enhance(1.4)
    crop = crop.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=1))
    
    bits = floyd_steinberg_dither(np.asarray(crop))
    ys, xs = np.where(bits)
    return xs, ys

def build_svg(variant_name: str, xs: np.ndarray, ys: np.ndarray, art_color: str, tag_text: str) -> str:
    # Offset points into VISUAL.MAP frame
    # Frame is: x=35, y=88, width=418, height=472
    # Inner HUD area is around x=48 to 440, y=140 to 510
    offset_x = 74
    offset_y = 138
    
    # Convert points into SVG path commands: 'M{x} {y}h1'
    # Group by line or build continuous path
    path_cmds = []
    for x, y in zip(xs, ys):
        path_cmds.append(f"M{offset_x + x} {offset_y + y}h1")
    points_path = "".join(path_cmds)
    
    # Rows for SYSTEM.INFO
    rows_svg = []
    start_y = 156
    line_spacing = 33
    
    for i, (key, val) in enumerate(INFO_ROWS):
        curr_y = start_y + (i * line_spacing)
        
        # Leader dots between key and value
        # Key starts at 492. Leader starts at 610, ends at 680 (or dynamically based on val)
        # We can draw nice terminal dotted leader
        dots = []
        for dot_x in range(612, 700, 7):
            dots.append(f"M{dot_x} {curr_y - 4}h1")
        dots_d = "".join(dots)
        
        # Format values with slight neon emphasis
        val_color = "#DDE7F5"
        if "TypeScript" in val:
            val_color = "#22D3EE"
        elif "Building" in val:
            val_color = "#10B981"
            
        rows_svg.append(f"""
    <!-- Row: {key} -->
    <text x="492" y="{curr_y}" fill="#8291A8" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" font-weight="600">{key}</text>
    <path d="{dots_d}" stroke="#25344C" stroke-width="1.5" shape-rendering="crispEdges"/>
    <text x="715" y="{curr_y}" fill="{val_color}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" font-weight="500">{val}</text>
        """)
        
    rows_str = "\n".join(rows_svg)
    pts_count = len(xs)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">Lu's Live Terminal Profile</title>
  <desc id="desc">Cyberpunk terminal profile with dithered {variant_name} and system specs.</desc>

  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0A101F"/>
      <stop offset="100%" stop-color="#070C18"/>
    </linearGradient>

    <!-- Panel Gradient -->
    <linearGradient id="panelGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0E172C"/>
      <stop offset="100%" stop-color="#0A1122"/>
    </linearGradient>

    <!-- Glow Effect -->
    <filter id="artGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="pulseGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#FF2A5F" flood-opacity="0.8"/>
    </filter>
  </defs>

  <style>
    @keyframes blink {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.25; }}
    }}
    @keyframes pulseGreen {{
      0%, 100% {{ opacity: 1; filter: drop-shadow(0 0 3px #10B981); }}
      50% {{ opacity: 0.4; filter: none; }}
    }}
    .live-dot {{ animation: blink 1.8s infinite ease-in-out; }}
    .status-dot {{ animation: pulseGreen 2.2s infinite ease-in-out; }}
  </style>

  <!-- Outer Window Frame -->
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="url(#bgGrad)" stroke="#25344C" stroke-width="1.5"/>

  <!-- Title Bar -->
  <path d="M1 50 H{W - 1}" stroke="#1F2D42" stroke-width="1.2"/>
  
  <!-- macOS Terminal Buttons -->
  <circle cx="34" cy="26" r="6" fill="#FF5F56"/>
  <circle cx="54" cy="26" r="6" fill="#FFBD2E"/>
  <circle cx="74" cy="26" r="6" fill="#27C93F"/>

  <!-- Window Title -->
  <text x="{W // 2}" y="31" text-anchor="middle" fill="#8291A8" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" font-weight="600" letter-spacing="0.5">profile.sh --live</text>

  <!-- ================= LEFT PANEL: VISUAL.MAP ================= -->
  <rect x="35" y="76" width="418" height="494" rx="8" fill="url(#panelGrad)" stroke="#1F2D42" stroke-width="1.2"/>
  <path d="M35 114 H453" stroke="#1F2D42" stroke-width="1.2"/>
  
  <!-- Panel Header -->
  <text x="52" y="101" fill="#22D3EE" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" font-weight="700" letter-spacing="1.5">[ VISUAL.MAP ]</text>
  <text x="436" y="101" text-anchor="end" fill="#64748B" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">340x370 / 1-BIT</text>

  <!-- HUD Corner Brackets -->
  <g stroke="#22D3EE" stroke-width="1.8" fill="none" opacity="0.65">
    <!-- Top-Left -->
    <path d="M52 138 h16 M52 138 v16"/>
    <!-- Top-Right -->
    <path d="M436 138 h-16 M436 138 v16"/>
    <!-- Bottom-Left -->
    <path d="M52 522 h16 M52 522 v-16"/>
    <!-- Bottom-Right -->
    <path d="M436 522 h-16 M436 522 v-16"/>
  </g>

  <!-- Rendered Dithered Points -->
  <g shape-rendering="crispEdges" stroke="{art_color}" stroke-width="1.2" fill="none">
    <path d="{points_path}"/>
  </g>

  <!-- Left Panel Footer -->
  <path d="M35 534 H453" stroke="#1F2D42" stroke-width="1.2"/>
  <text x="52" y="555" fill="#64748B" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" letter-spacing="0.8">PTS: {pts_count} / {tag_text}</text>
  <text x="436" y="555" text-anchor="end" fill="#22D3EE" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" opacity="0.85">STATUS: RENDERED</text>


  <!-- ================= RIGHT PANEL: SYSTEM.INFO ================= -->
  <rect x="470" y="76" width="675" height="494" rx="8" fill="url(#panelGrad)" stroke="#1F2D42" stroke-width="1.2"/>
  <path d="M470 114 H1145" stroke="#1F2D42" stroke-width="1.2"/>

  <!-- Panel Header -->
  <text x="492" y="101" fill="#22D3EE" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" font-weight="700" letter-spacing="1.5">SYSTEM.INFO</text>

  <!-- Live Indicator -->
  <g class="live-dot">
    <circle cx="985" cy="97" r="4.5" fill="#FF2A5F"/>
  </g>
  <text x="998" y="101" fill="#FF2A5F" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" font-weight="700" letter-spacing="0.5">LIVE</text>

  <!-- User Badge Pill -->
  <rect x="1042" y="86" width="88" height="22" rx="11" fill="#22D3EE" fill-opacity="0.12" stroke="#22D3EE" stroke-width="1.2"/>
  <text x="1086" y="101" text-anchor="middle" fill="#22D3EE" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" font-weight="700">@itsluuis</text>

  <!-- System Info Key-Value Rows -->
  {rows_str}

  <!-- Right Panel Footer Status Bar -->
  <path d="M470 534 H1145" stroke="#1F2D42" stroke-width="1.2"/>
  
  <circle cx="496" cy="552" r="4" fill="#10B981" class="status-dot"/>
  <text x="510" y="556" fill="#10B981" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" font-weight="600" letter-spacing="0.6">ALL SYSTEMS NOMINAL</text>
  
  <text x="1125" y="556" text-anchor="end" fill="#64748B" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" letter-spacing="0.5">UTC+0 · PORTUGAL NODE</text>

</svg>"""
    return svg_content

def main():
    print("Processing Spider Lily...")
    xs_lily, ys_lily = process_spider_lily(IMG_LILY)
    svg_lily = build_svg("Spider Lily", xs_lily, ys_lily, "#FF2A5F", "FL:LYCORIS_1BIT")
    out_lily = ASSETS / "banner-dark-lily.svg"
    out_lily.write_text(svg_lily, encoding="utf-8")
    print(f"Generated {out_lily} ({len(svg_lily)} bytes, {len(xs_lily)} points)")

    print("Processing Moon...")
    xs_moon, ys_moon = process_moon(IMG_MOON)
    svg_moon = build_svg("Moon", xs_moon, ys_moon, "#22D3EE", "FL:LUNA_1BIT")
    out_moon = ASSETS / "banner-dark-moon.svg"
    out_moon.write_text(svg_moon, encoding="utf-8")
    print(f"Generated {out_moon} ({len(svg_moon)} bytes, {len(xs_moon)} points)")

if __name__ == "__main__":
    main()
