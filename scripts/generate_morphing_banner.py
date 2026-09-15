#!/usr/bin/env python3
"""
Generate the Morphing Cyberpunk / Neovim Terminal banner for itsluuis
Morphs every 20 seconds between Moon ASCII and Spider Lily ASCII
Palette: #2F2F2F frame & structure, no emojis, clean monochrome + crimson flower
"""

import html
from pathlib import Path

ROOT = Path(r"c:\Users\HP\Documents\Vs Code\apps\Yio")
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

W, H = 1180, 620

MOON_RAW = """                                :::                                 
                              ==-.                                  
                            ++=-.                                   
                          +*+-:..                                   
                        :*+=--::.                                   
                       -*+=---::                                    
                      -*+-=+=:.                                     
                     ++=:-+=..                                      
                    :+===++=:                                       
                    ==---+=-..                                      
                   :=----=-:...                                     
                   +-----:::...                                     
                   =--:---::::.                                     
                  ------=--::.  :.                                  
                  ---:--++--............                            
                  ==-::-+*=-:....--:::-=.                           
                  -=-:::--::--:.::-----:.                           
                  :=--:::::::::-:.::::::.                           
                   +--.::..:.:-==-:::::....                         
                   +=:::......-===:::....                           
                   :*=-:::::...::::......  . ..                     
                    +#+---::.:..... ....:.                          
                     %#*=:...:.. ... ...-.                          
                      ###=::..:... ... .    ::                      
                       ###+=:..:.....::.. . .. .                    
                        *#=**=:.:::---=-.. :.. .                    
                         *###**+-=---=+-.   ....  :.... .           
                          .*##***++++++-..   .-: . .:::...          
                            -##*###****+=:::::--.:::-::::           
                              -###%%%#*##**+==---=---:::... .       
                                .+####*****++=======-=-:..:.   :    
                                   .*##*****+=++=------:::::: ..    
                                       :*******++===---==----:.     
                                             .--===+++=---.         """

FLOWER_RAW = """                       .         .                                  
                      ..         .                                     .    ..
   .          .                                                        .    .         .
   .         .                    .       .                                           .    .
   .  .       .        .          .       .                           .     .         .    .
      .   .    .        .         .       .                          ..     .        .    ..
    . .   .    .        ..        .:      :                          ..    .        ..    ..  .
   ... .   .    .        :        .=      :   ...                    .    ..        .    ..  ..
   . ....   .   ..       .:        .-     =:+----=  :-...-:         :.   ..        ..   ...  .
   .  ....  ..   .:       ..       .-. =++*+=#+:::.:=+#**##+=.     :.    .        ..   ...  . .
    . .....  ..   .:       ::      .:- =----#: ... .::--::--+-.::::.    ..       .:   ...  . .
    ...... .. ..   .-       .-.#####++=-:::=*.    .:::::::::+::::=++==::.       ..   :.:  ...  .
     ......... .:.   :-   .--*@@#*=-::=::::=*-=:  .:::::.::::::-=*-.::::.      :.  ...- .: .. ..
     .. .. .. :. .-.  .=..*-:: =:=-::::::::--:::. .::-+-:--::::=+.  ::.:.    .=   :..: .. ..  .
      .. ... .:.:: .-.  .+-::.  .=-::::-::::+::::.=:-::::-..:::=*= :::...   :.  ...:. ...:.   ..
        .  ... .: .=. -- .::::. *+--::::::::-::::---:::::...:::-..:::.....-.  ...-.  ..:.    ...
      .  .. .... .-..=-..++::=#*=::::::::::::.:::==-::::...:::::.::::..:.. ....:.. :..:     . ..
      .   ..  ..... .::.:-=+***+-::::::::::.::-::+=:.......:-::::::::::. ....:...:.::.  ...... .
       .    ..  .. .:: ..-=::::-::::.:::::::::.-:=:.......:::::..::::.....:..:-..=.     ..::. ..
       ..     ..  .....:--:::::...:::.::::.:::::--::....::::::..::::......::..-:       .::..  .
        ..      ...   .::.-::=++====:::::::.::-.-::::.::--:::::::::........:.        ::..:.  .
         ..       .-:+****++--==-::----::::::::-.:::.-==.:::::-:..........        :-. :-:   :.
          ..   .===++**=::-----::::::::. .:::::-::::--..::::.  ...............==:. .-:..  ..
            .  -+*+++*=. .....:::::::::::::::::::::::--:::::::......:::::::::..:::....   :.
             .=+.          .-:::::::::::::--:::::.-:----:..-:.::==:..::---::::....-.   :.
            =-:..       :-:::::--====--:...------.:.=:::::::::--:=-.:-+++===--:=-.. .=.
           :::.  ..    .:::-=*++:..  ...:::.:-==::-=. ::-----::::---...-----::::::-..
          .-::.    ....:::=*-:..:...:::...=..--=.:-=-   ...:+++=-:::::::::::.... ....
           ::....    ..:::+::::::.......:. .=:+.:-====.      .===::::::.          ..
           ........:::.:+-::::..:::....   .-.- ::===++-         :-::::..:.        ...
             ..........-::::-+.          .:.: .::-=--=-           .:.......      ::..
               ......::::::-*= .        :.-.  ::::::---.          ...........:-==-:.
                     .:::::=.    .....::..    ::::::::-:           ........::::::::
                      ::.::.                  ::.::::::.            ........:::::.
                       ...::       .          .:...:.::.      ..    ........
                         .......:::..          .........     ..............
                           ..........          ..........     ...::::.....
                            .......            ..........      .::--.
                                                :........--      ..
                                                :.......:::
                                                : .........
                                                :  ....   .
                                                .
                                                .
                                                .
                                                .
                                                .
                                                .
                                                .
                                                ."""

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

def format_ascii_lines(text: str, start_x: float, start_y: float, line_step: float) -> str:
    lines = text.split('\n')
    tspans = []
    for i, line in enumerate(lines):
        escaped = html.escape(line)
        y = start_y + (i * line_step)
        tspans.append(f'<tspan x="{start_x}" y="{y:.1f}">{escaped}</tspan>')
    return "\n      ".join(tspans)

def generate_banner():
    # Format Moon lines: 34 lines. Center in Y (140 to 510 is 370px).
    # 34 lines * 10.5px = 357px. start_y = 150
    # Moon width is 68 chars. At 6.2px per char = 421px. start_x = 44
    moon_tspans = format_ascii_lines(MOON_RAW, start_x=48, start_y=155, line_step=10.6)

    # Format Flower lines: 50 lines.
    # 50 lines * 7.4px = 370px. start_y = 145
    # Flower width is 96 chars. At 4.2px per char = 403px. start_x = 42
    flower_tspans = format_ascii_lines(FLOWER_RAW, start_x=40, start_y=142, line_step=7.5)

    # Key-value rows for SYSTEM.INFO
    rows_svg = []
    start_y = 158
    line_spacing = 34

    for i, (key, val) in enumerate(INFO_ROWS):
        curr_y = start_y + (i * line_spacing)
        
        # Leader dots in #2F2F2F
        dots = []
        for dot_x in range(612, 700, 7):
            dots.append(f"M{dot_x} {curr_y - 4}h1")
        dots_d = "".join(dots)
        
        # Values in clean technical high-contrast text
        val_color = "#E6EDF3"
        if "Building" in val:
            val_color = "#10B981"
        elif "TypeScript" in val:
            val_color = "#DDE7F5"
            
        rows_svg.append(f"""
    <!-- Row: {key} -->
    <text x="492" y="{curr_y}" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" font-weight="600">{key}</text>
    <path d="{dots_d}" stroke="#2F2F2F" stroke-width="1.5" shape-rendering="crispEdges"/>
    <text x="715" y="{curr_y}" fill="{val_color}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" font-weight="500">{val}</text>
        """)

    rows_str = "\n".join(rows_svg)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">Lu's Terminal Profile</title>
  <desc id="desc">Stealth terminal profile with morphing Moon and Spider Lily ASCII art.</desc>

  <defs>
    <!-- Background & Panel Fills -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#141414"/>
      <stop offset="100%" stop-color="#0D0D0D"/>
    </linearGradient>

    <linearGradient id="panelGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#181818"/>
      <stop offset="100%" stop-color="#111111"/>
    </linearGradient>
  </defs>

  <style>
    @keyframes blinkDot {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.2; }}
    }}
    @keyframes statusPulse {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.45; }}
    }}

    /* 40s Total Cycle: 20s Moon, 20s Flower (Dissolve Morph) */
    @keyframes morphMoon {{
      0% {{ opacity: 1; }}
      45% {{ opacity: 1; }}
      50% {{ opacity: 0; }}
      95% {{ opacity: 0; }}
      100% {{ opacity: 1; }}
    }}
    @keyframes morphFlower {{
      0% {{ opacity: 0; }}
      45% {{ opacity: 0; }}
      50% {{ opacity: 1; }}
      95% {{ opacity: 1; }}
      100% {{ opacity: 0; }}
    }}

    .layer-moon {{
      animation: morphMoon 40s infinite ease-in-out;
    }}
    .layer-flower {{
      animation: morphFlower 40s infinite ease-in-out;
    }}
    .live-dot {{ animation: blinkDot 1.8s infinite ease-in-out; }}
    .status-dot {{ animation: statusPulse 2.5s infinite ease-in-out; }}
    .ascii-text {{
      font-family: ui-monospace, SFMono-Regular, "Courier New", monospace;
      font-weight: 600;
      white-space: pre;
    }}
  </style>

  <!-- ================= OUTER TERMINAL WINDOW ================= -->
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="10" fill="url(#bgGrad)" stroke="#2F2F2F" stroke-width="1.8"/>

  <!-- Window Title Bar -->
  <path d="M1 48 H{W - 1}" stroke="#2F2F2F" stroke-width="1.5"/>
  
  <!-- macOS Terminal Window Buttons (Minimalist / Subtle) -->
  <circle cx="32" cy="25" r="5.5" fill="#FF5F56" opacity="0.85"/>
  <circle cx="50" cy="25" r="5.5" fill="#FFBD2E" opacity="0.85"/>
  <circle cx="68" cy="25" r="5.5" fill="#27C93F" opacity="0.85"/>

  <!-- Centered Title -->
  <text x="{W // 2}" y="30" text-anchor="middle" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" font-weight="600" letter-spacing="0.6">profile.sh --live</text>


  <!-- ================= LEFT PANEL: VISUAL.MAP ================= -->
  <rect x="30" y="72" width="425" height="518" rx="6" fill="url(#panelGrad)" stroke="#2F2F2F" stroke-width="1.5"/>
  <path d="M30 110 H455" stroke="#2F2F2F" stroke-width="1.5"/>

  <!-- Left Header -->
  <text x="46" y="96" fill="#C9D1D9" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" font-weight="700" letter-spacing="1.2">[ VISUAL.MAP ]</text>
  <text x="438" y="96" text-anchor="end" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">ASCII / 20s MORPH</text>

  <!-- HUD Corner Brackets in #2F2F2F -->
  <g stroke="#3A3A3A" stroke-width="2" fill="none">
    <path d="M46 130 h14 M46 130 v14"/>
    <path d="M439 130 h-14 M439 130 v14"/>
    <path d="M46 540 h14 M46 540 v-14"/>
    <path d="M439 540 h-14 M439 540 v-14"/>
  </g>

  <!-- ================= MORPHING ASCII LAYER 1: MOON ================= -->
  <g class="layer-moon">
    <text class="ascii-text" font-size="6.1" fill="#DDE7F5" letter-spacing="0.2">
      {moon_tspans}
    </text>
    <!-- Label for Moon -->
    <text x="46" y="567" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" letter-spacing="0.6">MAP: LUNA // 34-LINE ASCII</text>
  </g>

  <!-- ================= MORPHING ASCII LAYER 2: SPIDER LILY ================= -->
  <g class="layer-flower">
    <text class="ascii-text" font-size="4.25" fill="#FF2A5F" letter-spacing="0.1">
      {flower_tspans}
    </text>
    <!-- Label for Flower -->
    <text x="46" y="567" fill="#FF2A5F" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" letter-spacing="0.6">MAP: HIGANBANA // 50-LINE ASCII</text>
  </g>

  <!-- Left Footer Divider & Status -->
  <path d="M30 550 H455" stroke="#2F2F2F" stroke-width="1.5"/>
  <text x="438" y="567" text-anchor="end" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">CYCLE: 20S</text>


  <!-- ================= RIGHT PANEL: SYSTEM.INFO ================= -->
  <rect x="475" y="72" width="675" height="518" rx="6" fill="url(#panelGrad)" stroke="#2F2F2F" stroke-width="1.5"/>
  <path d="M475 110 H1150" stroke="#2F2F2F" stroke-width="1.5"/>

  <!-- Right Header -->
  <text x="492" y="96" fill="#C9D1D9" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" font-weight="700" letter-spacing="1.2">SYSTEM.INFO</text>

  <!-- Live Indicator Dot -->
  <circle cx="985" cy="92" r="4.5" fill="#FF2A5F" class="live-dot"/>
  <text x="998" y="96" fill="#FF2A5F" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" font-weight="700" letter-spacing="0.5">LIVE</text>

  <!-- Clean Pill Badge in #2F2F2F -->
  <rect x="1042" y="82" width="90" height="22" rx="4" fill="#242424" stroke="#3A3A3A" stroke-width="1.2"/>
  <text x="1087" y="97" text-anchor="middle" fill="#E6EDF3" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" font-weight="600">@itsluuis</text>

  <!-- System Info Key-Value Rows -->
  {rows_str}

  <!-- Right Panel Footer Status Bar -->
  <path d="M475 550 H1150" stroke="#2F2F2F" stroke-width="1.5"/>
  
  <circle cx="496" cy="567" r="4" fill="#10B981" class="status-dot"/>
  <text x="508" y="571" fill="#10B981" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" font-weight="600" letter-spacing="0.6">ALL SYSTEMS NOMINAL</text>
  
  <text x="1132" y="571" text-anchor="end" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" letter-spacing="0.5">UTC+0 · PORTUGAL NODE</text>

</svg>"""

    out_file = ASSETS / "banner-dark.svg"
    out_file.write_text(svg_content, encoding="utf-8")
    print(f"Generated {out_file} ({len(svg_content)} bytes)")

if __name__ == "__main__":
    generate_banner()
