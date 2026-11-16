#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 GitHub 主页用的自定义 SVG 素材（不依赖任何第三方图床/服务）。

    python3 tools/gen_assets.py

产物：
    assets/hero.svg            顶部横幅（含 SMIL 动画）
    assets/projects/*.svg      项目卡片
改了文案之后重新跑一次即可。
"""

from __future__ import annotations

import os
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
PROJECTS_DIR = os.path.join(ASSETS, "projects")

# ---------------------------------------------------------------- design tokens
LINE = "#1E3A5F"
GOLD = "#FFD93D"
GOLD2 = "#D4AF37"
TEXT = "#E8EEF6"
MUTED = "#8FA6BE"
BODY = "#A9BCCE"

FONT = ("Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', "
        "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif")
MONO = ("'SFMono-Regular', ui-monospace, 'JetBrains Mono', Menlo, Consolas, "
        "'PingFang SC', monospace")


def text_width(text: str, size: float) -> float:
    w = 0.0
    for ch in text:
        w += size if ord(ch) > 0x2E80 else size * 0.58
    return w


# ---------------------------------------------------------------- hero banner
def hero() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="340"
     viewBox="0 0 1280 340" fill="none" role="img"
     aria-label="宋朝阳 SONG ZHAOYANG - 数据开发分析师 / 独立开发者">
  <title>宋朝阳 · SONG ZHAOYANG</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1280" y2="340" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#050D18"/>
      <stop offset="0.55" stop-color="#0A1A2C"/>
      <stop offset="1" stop-color="#0C263C"/>
    </linearGradient>
    <radialGradient id="glowGold" cx="0" cy="0" r="1"
        gradientTransform="translate(1080 30) rotate(118) scale(540 430)" gradientUnits="userSpaceOnUse">
      <stop stop-color="#FFD93D" stop-opacity="0.20"/>
      <stop offset="0.55" stop-color="#D4AF37" stop-opacity="0.06"/>
      <stop offset="1" stop-color="#D4AF37" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowBlue" cx="0" cy="0" r="1"
        gradientTransform="translate(90 340) rotate(-62) scale(520 340)" gradientUnits="userSpaceOnUse">
      <stop stop-color="#12B7F5" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#12B7F5" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="nameGrad" x1="72" y1="130" x2="330" y2="190" gradientUnits="userSpaceOnUse">
      <stop stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#FFE7A3"/>
    </linearGradient>
    <linearGradient id="codeGrad" x1="1010" y1="120" x2="1120" y2="210" gradientUnits="userSpaceOnUse">
      <stop stop-color="#FFE7A3"/>
      <stop offset="1" stop-color="#D4AF37"/>
    </linearGradient>
    <linearGradient id="rule" x1="76" y1="0" x2="220" y2="0" gradientUnits="userSpaceOnUse">
      <stop stop-color="#FFD93D" stop-opacity="0.95"/>
      <stop offset="1" stop-color="#FFD93D" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="bottomLine" x1="0" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop stop-color="#FFD93D" stop-opacity="0"/>
      <stop offset="0.25" stop-color="#D4AF37" stop-opacity="0.55"/>
      <stop offset="0.62" stop-color="#12B7F5" stop-opacity="0.40"/>
      <stop offset="1" stop-color="#12B7F5" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="spark" x1="0" y1="0" x2="150" y2="0" gradientUnits="userSpaceOnUse">
      <stop stop-color="#FFD93D" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#FFF3C4" stop-opacity="0.9"/>
      <stop offset="1" stop-color="#FFD93D" stop-opacity="0"/>
    </linearGradient>
    <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="#FFFFFF" fill-opacity="0.055"/>
    </pattern>
    <filter id="soft" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <filter id="glowText" x="-40%" y="-40%" width="180%" height="180%">
      <feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="#FFD93D" flood-opacity="0.45"/>
    </filter>
    <style>
      .ink {{ font-family: {FONT}; }}
      .mono {{ font-family: {MONO}; }}
      .blink {{ animation: blink 1.4s steps(1, end) infinite; }}
      .float {{ animation: floaty 5s ease-in-out infinite; }}
      @keyframes blink {{ 0%, 49.9% {{ opacity: 1 }} 50%, 100% {{ opacity: 0 }} }}
      @keyframes floaty {{ 0%, 100% {{ opacity: .45 }} 50% {{ opacity: 1 }} }}
    </style>
  </defs>

  <!-- background -->
  <rect width="1280" height="340" fill="url(#bg)"/>
  <rect width="1280" height="340" fill="url(#dots)"/>
  <rect width="1280" height="340" fill="url(#glowGold)"/>
  <rect width="1280" height="340" fill="url(#glowBlue)"/>

  <!-- hud corner brackets -->
  <g stroke="#D4AF37" stroke-opacity="0.40" stroke-width="1.4" fill="none">
    <path d="M30 58 V30 H58"/>
    <path d="M1222 30 H1250 V58"/>
    <path d="M1250 282 V310 H1222"/>
    <path d="M58 310 H30 V282"/>
  </g>

  <!-- left: identity -->
  <text class="mono" x="76" y="104" font-size="13.5" letter-spacing="4.2"
        fill="#FFD93D" fill-opacity="0.9">// HELLO, WORLD</text>
  <rect x="272" y="93" width="8" height="15" fill="#FFD93D" fill-opacity="0.85" class="blink"/>

  <text class="ink" x="72" y="186" font-size="68" font-weight="700"
        letter-spacing="2" fill="url(#nameGrad)">{escape("宋朝阳")}</text>

  <text class="mono" x="76" y="226" font-size="16.5" letter-spacing="7.6"
        fill="#D4AF37" fill-opacity="0.95">SONG ZHAOYANG</text>

  <rect x="76" y="252" width="190" height="2" fill="url(#rule)"/>

  <text class="ink" x="76" y="292" font-size="16.5" fill="#9FB3C8"
        letter-spacing="0.6">{escape("数据开发分析师 · 独立开发者 · 桌面工具 / AI 自动化")}</text>

  <text class="mono" x="76" y="323" font-size="13.5" letter-spacing="1.4"
        fill="#6E8399">github.com/mrsongzhaoyang</text>

  <!-- right: orbital code mark -->
  <g>
    <circle cx="1065" cy="165" r="150" fill="#D4AF37" fill-opacity="0.10" filter="url(#soft)"/>
    <circle cx="1065" cy="165" r="128" stroke="{LINE}" stroke-opacity="0.85"/>
    <circle cx="1065" cy="165" r="128" stroke="#FFD93D" stroke-opacity="0.55"
            stroke-width="2" stroke-linecap="round" stroke-dasharray="2 16">
      <animateTransform attributeName="transform" type="rotate"
                        from="0 1065 165" to="360 1065 165" dur="36s" repeatCount="indefinite"/>
    </circle>
    <circle cx="1065" cy="165" r="100" fill="#0A1A2C" fill-opacity="0.92" stroke="{LINE}"/>
    <text class="mono" x="1065" y="186" text-anchor="middle" font-size="46"
          font-weight="700" fill="url(#codeGrad)" filter="url(#glowText)">&lt;/&gt;</text>

    <g>
      <circle cx="1065" cy="37" r="4.5" fill="#FFD93D"/>
      <animateTransform attributeName="transform" type="rotate"
                        from="0 1065 165" to="360 1065 165" dur="18s" repeatCount="indefinite"/>
    </g>
    <g>
      <circle cx="1193" cy="165" r="3" fill="#12B7F5" fill-opacity="0.9"/>
      <animateTransform attributeName="transform" type="rotate"
                        from="0 1065 165" to="-360 1065 165" dur="26s" repeatCount="indefinite"/>
    </g>

    <g fill="#FFE7A3">
      <circle cx="905" cy="74" r="2.6" class="float"/>
      <circle cx="1195" cy="262" r="2.2" class="float" style="animation-delay:.9s"/>
      <circle cx="982" cy="286" r="2.0" class="float" style="animation-delay:1.8s"/>
    </g>
  </g>

  <!-- bottom light -->
  <rect x="0" y="337" width="1280" height="2" fill="url(#bottomLine)"/>
  <rect x="-150" y="336" width="150" height="3" fill="url(#spark)" opacity="0.9">
    <animateTransform attributeName="transform" type="translate"
                      from="0 0" to="1430 0" dur="9s" repeatCount="indefinite"/>
  </rect>
</svg>
'''


# ---------------------------------------------------------------- project card
def project_card(idx: int, title: str, en: str, desc: str,
                 tags: list[str], stars: int, accent: str) -> str:
    px = 34.0
    pills = []
    for t in tags:
        w = text_width(t, 12.5) + 22
        pills.append(f'''  <g>
    <rect x="{px:.1f}" y="113" width="{w:.1f}" height="25" rx="12.5"
          fill="{accent}" fill-opacity="0.09" stroke="{accent}" stroke-opacity="0.30"/>
    <text class="mono" x="{px + 11:.1f}" y="130" font-size="12.5"
          fill="{accent}" fill-opacity="0.92">{escape(t)}</text>
  </g>''')
        px += w + 9

    tw = text_width(title, 26) + 2
    en_text = ""
    if en and en.lower() != title.lower():
        en_text = (f'\n  <text class="mono" x="{34 + tw + 10:.1f}" y="70" font-size="13.5" '
                   f'fill="{MUTED}" fill-opacity="0.85" letter-spacing="0.5">{escape(en)}</text>')

    star = ""
    if stars > 0:
        star = (f'''  <g>
    <circle cx="900" cy="70" r="17" fill="#FFD93D" fill-opacity="0.08" stroke="#D4AF37" stroke-opacity="0.35"/>
    <text class="mono" x="900" y="75" text-anchor="middle" font-size="12.5"
          fill="#FFD93D">{stars}★</text>
  </g>
''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="158"
     viewBox="0 0 1000 158" fill="none" role="img" aria-label="{escape(title)}">
  <title>{escape(title)} — {escape(en)}</title>
  <defs>
    <linearGradient id="card{idx}" x1="0" y1="0" x2="1000" y2="158" gradientUnits="userSpaceOnUse">
      <stop stop-color="#0E2136"/>
      <stop offset="1" stop-color="#081524"/>
    </linearGradient>
    <linearGradient id="bar{idx}" x1="0" y1="0" x2="0" y2="158" gradientUnits="userSpaceOnUse">
      <stop stop-color="{accent}" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0.12"/>
    </linearGradient>
    <clipPath id="clip{idx}">
      <rect width="1000" height="158" rx="18"/>
    </clipPath>
    <style>
      .ink {{ font-family: {FONT}; }}
      .mono {{ font-family: {MONO}; }}
    </style>
  </defs>

  <g clip-path="url(#clip{idx})">
    <rect width="1000" height="158" fill="url(#card{idx})"/>
    <rect x="0" y="0" width="5" height="158" fill="url(#bar{idx})"/>
    <circle cx="966" cy="4" r="86" fill="{accent}" fill-opacity="0.07"/>
    <text class="mono" x="986" y="145" text-anchor="end" font-size="116" font-weight="700"
          fill="#FFFFFF" fill-opacity="0.035">{idx:02d}</text>
  </g>
  <rect x="0.75" y="0.75" width="998.5" height="156.5" rx="17.25"
        stroke="{LINE}" stroke-opacity="0.85" stroke-width="1.5"/>

  <text class="mono" x="34" y="36" font-size="11.5" letter-spacing="2.4"
        fill="{accent}" fill-opacity="0.8">PROJECT {idx:02d}</text>

  <text class="ink" x="34" y="70" font-size="26" font-weight="700"
        fill="{TEXT}">{escape(title)}</text>{en_text}

  <text class="ink" x="34" y="99" font-size="15" fill="{BODY}">{escape(desc)}</text>
{chr(10).join(pills)}
{star}  <g>
    <circle cx="952" cy="79" r="18" fill="#0F2438" stroke="{LINE}"/>
    <text x="952" y="86" text-anchor="middle" font-size="16" fill="{accent}">↗</text>
  </g>
</svg>
'''


PROJECTS = [
    dict(
        title="垂钓鸭", en="ChuiDuck",
        desc="在网页世界里垂钓数据：选技能包 → 建任务 → 自动执行 → 导出结果",
        tags=["TypeScript", "Electron", "Vue 3", "SQLite"],
        stars=2, accent="#FFD93D",
    ),
    dict(
        title="Mirscope", en="Mirscope",
        desc="本地优先的 AI Prompt 全景分析平台，对话数据默认不出本机",
        tags=["TypeScript", "AI", "Local-first"],
        stars=0, accent="#12B7F5",
    ),
    dict(
        title="WinNav", en="WinNav",
        desc="Rust 打造的桌面导航工具，把窗口、文件与命令收进一条入口",
        tags=["Rust", "Desktop", "CLI"],
        stars=0, accent="#FF9F1C",
    ),
    dict(
        title="DeepForge", en="deepforge",
        desc="沙盘推演，模拟预策事情走向 —— 动手之前先把事情走一遍",
        tags=["Batch", "Simulation"],
        stars=0, accent="#7DD3FC",
    ),
    dict(
        title="Project Manager", en="project_manager",
        desc="用 Python 把项目、任务与进度收进一个自己顺手的工具里",
        tags=["Python", "Tooling"],
        stars=0, accent="#A7F3D0",
    ),
]


def main() -> None:
    os.makedirs(PROJECTS_DIR, exist_ok=True)

    with open(os.path.join(ASSETS, "hero.svg"), "w", encoding="utf-8") as f:
        f.write(hero())

    for i, p in enumerate(PROJECTS, start=1):
        svg = project_card(i, p["title"], p["en"], p["desc"], p["tags"],
                           p["stars"], p["accent"])
        slug = p["en"].lower().replace(" ", "-")
        with open(os.path.join(PROJECTS_DIR, f"{slug}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)

    print("generated:", os.path.join(ASSETS, "hero.svg"))
    print("generated:", len(PROJECTS), "project cards")


if __name__ == "__main__":
    main()
