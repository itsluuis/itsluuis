#!/usr/bin/env python3
"""
Fetch GitHub user stats for itsluuis and generate stealth #2F2F2F overview.svg
Supports both GitHub GraphQL API (with ACCESS_TOKEN for private data) and REST API fallback.
Zero emojis, clean monospace numbers, professional terminal design.
"""

import os
import json
import urllib.request
from pathlib import Path

USERNAME = os.environ.get("GITHUB_USERNAME", "itsluuis")
TOKEN = os.environ.get("ACCESS_TOKEN", "").strip()

ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = ROOT / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)
OUT_SVG = GENERATED_DIR / "overview.svg"

def fetch_stats():
    stars = 0
    public_repos = 0
    followers = 0
    contributions = 0
    languages = {}

    headers = {
        "User-Agent": "itsluuis-stats-updater",
        "Accept": "application/vnd.github.v3+json"
    }
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"

    # 1. Fetch user profile
    try:
        req = urllib.request.Request(f"https://api.github.com/users/{USERNAME}", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            public_repos = data.get("public_repos", 0)
            followers = data.get("followers", 0)
    except Exception as e:
        print(f"Error fetching user profile: {e}")

    # 2. Fetch repos & stars & languages
    try:
        req = urllib.request.Request(f"https://api.github.com/users/{USERNAME}/repos?per_page=100", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            repos = json.loads(resp.read().decode())
            for repo in repos:
                stars += repo.get("stargazers_count", 0)
                lang = repo.get("language")
                if lang:
                    languages[lang] = languages.get(lang, 0) + 1
    except Exception as e:
        print(f"Error fetching repos: {e}")

    # 3. Fetch GraphQL contributions if token is available
    if TOKEN:
        gql_query = {
            "query": f"""
            query {{
              user(login: "{USERNAME}") {{
                contributionsCollection {{
                  contributionCalendar {{
                    totalContributions
                  }}
                }}
              }}
            }}
            """
        }
        try:
            req = urllib.request.Request(
                "https://api.github.com/graphql",
                data=json.dumps(gql_query).encode(),
                headers={"Authorization": f"bearer {TOKEN}", "User-Agent": "itsluuis-stats-updater"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                g_data = json.loads(resp.read().decode())
                contributions = g_data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
        except Exception as e:
            print(f"Error fetching GraphQL contributions: {e}")

    return {
        "stars": stars,
        "public_repos": public_repos,
        "followers": followers,
        "contributions": contributions,
        "languages": languages
    }

def render_svg(stats):
    stars_val = str(stats["stars"])
    repos_val = str(stats["public_repos"])
    followers_val = str(stats["followers"])
    contribs_val = str(stats["contributions"]) if stats["contributions"] > 0 else "--"
    
    # Calculate language percentages or defaults
    top_langs = sorted(stats["languages"].items(), key=lambda x: x[1], reverse=True)
    if not top_langs:
        # Default active stack
        top_langs = [("TypeScript", 70), ("Python", 20), ("JavaScript", 10)]

    total_pts = sum(v for _, v in top_langs[:3]) or 1
    l1_name, l1_pts = top_langs[0] if len(top_langs) > 0 else ("TypeScript", 1)
    l2_name, l2_pts = top_langs[1] if len(top_langs) > 1 else ("Python", 0)
    l3_name, l3_pts = top_langs[2] if len(top_langs) > 2 else ("JavaScript", 0)

    w1 = int(round((l1_pts / total_pts) * 624))
    w2 = int(round((l2_pts / total_pts) * 624)) if l2_pts else 0
    w3 = max(0, 624 - w1 - w2) if l3_pts else 0

    p1_pct = f"{int(round((l1_pts / total_pts) * 100))}%"
    p2_pct = f"{int(round((l2_pts / total_pts) * 100))}%" if l2_pts else ""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="680" height="340" viewBox="0 0 680 340" role="img" aria-labelledby="title desc">
  <title id="title">{USERNAME} at a glance</title>
  <desc id="desc">GitHub profile overview statistics card without emojis in stealth dark theme</desc>

  <defs>
    <linearGradient id="cardBg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#141414"/>
      <stop offset="100%" stop-color="#0E0E0E"/>
    </linearGradient>
  </defs>

  <!-- Card Border & Background in #2F2F2F -->
  <rect x="1" y="1" width="678" height="338" rx="6" fill="url(#cardBg)" stroke="#2F2F2F" stroke-width="1.6"/>

  <!-- Header -->
  <text x="28" y="38" fill="#E6EDF3" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="15" font-weight="700">{USERNAME}</text>
  <text x="652" y="38" text-anchor="end" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" letter-spacing="0.4">at a glance</text>

  <!-- 6 Metrics Grid (Purely numbers and labels, NO EMOJIS) -->
  <!-- Col 1 -->
  <text x="28" y="80" fill="#FFFFFF" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="22" font-weight="700">{stars_val}</text>
  <text x="28" y="98" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" letter-spacing="0.3">Total stars</text>

  <text x="28" y="136" fill="#FFFFFF" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="22" font-weight="700">{contribs_val}</text>
  <text x="28" y="154" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" letter-spacing="0.3">Contributions (1y)</text>

  <!-- Col 2 -->
  <text x="250" y="80" fill="#FFFFFF" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="22" font-weight="700">{repos_val}</text>
  <text x="250" y="98" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" letter-spacing="0.3">Public repos</text>

  <text x="250" y="136" fill="#FFFFFF" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="22" font-weight="700">--</text>
  <text x="250" y="154" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" letter-spacing="0.3">Current streak</text>

  <!-- Col 3 -->
  <text x="470" y="80" fill="#FFFFFF" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="22" font-weight="700">{followers_val}</text>
  <text x="470" y="98" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" letter-spacing="0.3">Followers</text>

  <text x="470" y="136" fill="#FFFFFF" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="22" font-weight="700">--</text>
  <text x="470" y="154" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" letter-spacing="0.3">Longest streak</text>

  <!-- Horizontal Divider in #2F2F2F -->
  <path d="M28 176 H652" stroke="#2F2F2F" stroke-width="1.4"/>

  <!-- Languages Section Header -->
  <text x="28" y="200" fill="#E6EDF3" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" font-weight="700">Languages</text>
  <text x="115" y="200" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12">· Most used languages</text>

  <!-- Clean Progress Bar -->
  <g shape-rendering="crispEdges">
    <rect x="28" y="214" width="{max(12, w1)}" height="7" rx="3" fill="#4B5563"/>
    <rect x="{28 + w1}" y="214" width="{max(0, w2)}" height="7" rx="0" fill="#6B7280"/>
    <rect x="{28 + w1 + w2}" y="214" width="{max(0, w3)}" height="7" rx="3" fill="#9CA3AF"/>
  </g>

  <!-- Languages List (2 Columns - Minimalist dots) -->
  <!-- Col 1 -->
  <circle cx="34" cy="248" r="3.5" fill="#4B5563"/>
  <text x="46" y="252" fill="#E6EDF3" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" font-weight="600">{l1_name}</text>
  <text x="155" y="252" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">{p1_pct} · Core</text>

  <circle cx="34" cy="276" r="3.5" fill="#9CA3AF"/>
  <text x="46" y="280" fill="#E6EDF3" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" font-weight="600">{l3_name}</text>
  <text x="155" y="280" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">Active</text>

  <!-- Col 2 -->
  <circle cx="350" cy="248" r="3.5" fill="#6B7280"/>
  <text x="362" y="252" fill="#E6EDF3" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" font-weight="600">{l2_name}</text>
  <text x="440" y="252" fill="#8B949E" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">{p2_pct} · Active</text>

  <!-- Card Footer -->
  <path d="M28 304 H652" stroke="#2F2F2F" stroke-width="1.2"/>
  <text x="340" y="324" text-anchor="middle" fill="#6B7280" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="10" letter-spacing="0.4">Built with love: github-stats</text>

</svg>"""
    return svg

def main():
    print(f"Fetching GitHub stats for {USERNAME}...")
    stats = fetch_stats()
    print("Stats fetched:", stats)
    svg_code = render_svg(stats)
    OUT_SVG.write_text(svg_code, encoding="utf-8")
    print(f"Successfully generated {OUT_SVG}")

if __name__ == "__main__":
    main()
