#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 / 刷新 GitHub 主页的「数据面板」两张卡：

    assets/stats.svg    项目数 / Star 数 / 近一年贡献 / 加入年份
    assets/langs.svg    语言构成（按代码量）

数据全部来自公开接口，无需任何 token 也能跑；仓库内由
.github/workflows/stats.yml 每天自动执行并提交更新。

    python3 tools/gen_stats.py
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
USER = "mrsongzhaoyang"

LINE = "#1E3A5F"
GOLD = "#FFD93D"
TEXT = "#E8EEF6"
MUTED = "#8FA6BE"

FONT = ("Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', "
        "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif")
MONO = ("'SFMono-Regular', ui-monospace, 'JetBrains Mono', Menlo, Consolas, "
        "'PingFang SC', monospace")

PALETTE = ["#FFD93D", "#FF9F1C", "#12B7F5", "#2DD4BF", "#A78BFA", "#64748B"]

TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "profile-readme-stats",
}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def get_json(url: str, timeout: int = 25, retries: int = 3):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            last = exc
            if attempt + 1 < retries:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"GET {url} failed: {last}")


def get_text(url: str, timeout: int = 25, retries: int = 3) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; profile-readme-stats)"}
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", "ignore")
        except Exception as exc:  # noqa: BLE001
            last = exc
            if attempt + 1 < retries:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"GET {url} failed: {last}")


def fetch_contributions() -> int:
    """优先读 GitHub 自己页面上的「近一年贡献」数字，保证和主页绿格子完全一致。"""
    try:
        html = get_text(f"https://github.com/users/{USER}/contributions")
        m = re.search(r"([\d,]+)\s+contributions?\s+in\s+the\s+last\s+year", html)
        if m:
            return int(m.group(1).replace(",", ""))
    except Exception as exc:  # noqa: BLE001
        print(f"  ! profile contributions: {exc}", file=sys.stderr)

    try:
        c = get_json(f"https://github-contributions-api.jogruber.de/v4/{USER}?y=last")
        return int(c.get("total", {}).get("lastYear", 0))
    except Exception as exc:  # noqa: BLE001
        print(f"  ! contributions fallback: {exc}", file=sys.stderr)
    return 0


def collect() -> dict:
    user = get_json(f"https://api.github.com/users/{USER}")
    all_repos = get_json(f"https://api.github.com/users/{USER}/repos?per_page=100&sort=pushed")

    # Profile 仓库本身不算「作品」，统计里排除掉
    repos = [r for r in all_repos if not r.get("fork") and r["name"] != USER]

    langs: dict[str, int] = {}
    for repo in repos:
        # 这里失败必须报错：宁可让 workflow 红掉，也不要提交一份缺了仓库的假数据
        data = get_json(f"https://api.github.com/repos/{USER}/{repo['name']}/languages")
        for name, size in data.items():
            langs[name] = langs.get(name, 0) + int(size)

    since = 2017
    try:
        since = int(user["created_at"][:4])
    except Exception:  # noqa: BLE001
        pass

    return {
        "repos": len(repos),
        "stars": sum(int(r.get("stargazers_count", 0)) for r in repos),
        "contributions": fetch_contributions(),
        "since": since,
        "langs": langs,
    }


# ------------------------------------------------------------------ stats card
def stats_svg(d: dict) -> str:
    cells = [
        (f"{d['repos']}", "PROJECTS", "公开项目"),
        (f"{d['stars']}", "STARS", "被收藏"),
        (f"{d['contributions']}", "CONTRIBUTIONS", "近 12 个月"),
        (f"{d['since']}", "ON GITHUB", "加入年份"),
    ]
    xs = [150.5, 383.5, 616.5, 849.5]
    dividers = "".join(
        f'\n  <line x1="{x}" y1="44" x2="{x}" y2="116" stroke="{LINE}" '
        f'stroke-opacity="0.55" stroke-dasharray="3 5"/>'
        for x in (267, 500, 733)
    )
    body = []
    for (value, label, sub), cx in zip(cells, xs):
        body.append(f'''  <text class="mono" x="{cx}" y="46" text-anchor="middle" font-size="11.5"
        letter-spacing="2.2" fill="#D4AF37" fill-opacity="0.85">{label}</text>
  <text class="ink" x="{cx}" y="96" text-anchor="middle" font-size="42"
        font-weight="700" fill="{TEXT}">{value}</text>
  <text class="ink" x="{cx}" y="122" text-anchor="middle" font-size="12"
        fill="{MUTED}">{sub}</text>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="150"
     viewBox="0 0 1000 150" fill="none" role="img" aria-label="GitHub 数据面板">
  <title>GitHub 数据面板</title>
  <defs>
    <linearGradient id="sbg" x1="0" y1="0" x2="1000" y2="150" gradientUnits="userSpaceOnUse">
      <stop stop-color="#0E2136"/>
      <stop offset="1" stop-color="#081524"/>
    </linearGradient>
    <linearGradient id="sbar" x1="0" y1="0" x2="0" y2="150" gradientUnits="userSpaceOnUse">
      <stop stop-color="{GOLD}" stop-opacity="0.95"/>
      <stop offset="1" stop-color="{GOLD}" stop-opacity="0.12"/>
    </linearGradient>
    <clipPath id="sclip"><rect width="1000" height="150" rx="18"/></clipPath>
    <style>
      .ink {{ font-family: {FONT}; }}
      .mono {{ font-family: {MONO}; }}
    </style>
  </defs>

  <g clip-path="url(#sclip)">
    <rect width="1000" height="150" fill="url(#sbg)"/>
    <rect x="0" y="0" width="5" height="150" fill="url(#sbar)"/>
    <circle cx="980" cy="0" r="90" fill="#FFD93D" fill-opacity="0.05"/>
  </g>
  <rect x="0.75" y="0.75" width="998.5" height="148.5" rx="17.25"
        stroke="{LINE}" stroke-opacity="0.85" stroke-width="1.5"/>{dividers}

{chr(10).join(body)}
</svg>
'''


def text_w(text: str, size: float) -> float:
    w = 0.0
    for ch in text:
        w += size if ord(ch) > 0x2E80 else size * 0.60
    return w


# ------------------------------------------------------------------- langs card
def langs_svg(d: dict) -> str:
    total = sum(d["langs"].values()) or 1
    ranked = sorted(d["langs"].items(), key=lambda kv: kv[1], reverse=True)

    segments = ranked[:5]
    rest = sum(v for _, v in ranked[5:])
    if rest:
        segments.append(("其他", rest))

    # 中文名 / 图标用统一配色，保证整页色调一致
    x = 34.0
    bars, legend = [], []
    max_w = 932.0
    step = max_w / len(segments)
    for i, (name, size) in enumerate(segments):
        pct = size / total * 100
        w = max(max_w * size / total, 0)
        color = PALETTE[i % len(PALETTE)]
        bars.append(f'  <rect x="{x:.1f}" y="60" width="{w:.1f}" height="16" fill="{color}"/>')
        lx = 34 + i * step
        nw = text_w(name, 13)
        legend.append(f'''  <g>
    <circle cx="{lx + 4:.1f}" cy="112" r="4.5" fill="{color}"/>
    <text class="ink" x="{lx + 17:.1f}" y="116" font-size="13" fill="#D6E1ED">{name}</text>
    <text class="mono" x="{lx + 17 + nw + 8:.1f}" y="116" font-size="12"
          fill="{MUTED}" fill-opacity="0.9">{pct:.1f}%</text>
  </g>''')
        x += w

    kb = total / 1024

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="150"
     viewBox="0 0 1000 150" fill="none" role="img" aria-label="语言构成">
  <title>语言构成</title>
  <defs>
    <linearGradient id="lbg" x1="0" y1="0" x2="1000" y2="150" gradientUnits="userSpaceOnUse">
      <stop stop-color="#0E2136"/>
      <stop offset="1" stop-color="#081524"/>
    </linearGradient>
    <clipPath id="lclip"><rect width="1000" height="150" rx="18"/></clipPath>
    <clipPath id="track"><rect x="34" y="60" width="932" height="16" rx="8"/></clipPath>
    <style>
      .ink {{ font-family: {FONT}; }}
      .mono {{ font-family: {MONO}; }}
    </style>
  </defs>

  <g clip-path="url(#lclip)">
    <rect width="1000" height="150" fill="url(#lbg)"/>
    <circle cx="960" cy="10" r="88" fill="#12B7F5" fill-opacity="0.05"/>
  </g>
  <rect x="0.75" y="0.75" width="998.5" height="148.5" rx="17.25"
        stroke="{LINE}" stroke-opacity="0.85" stroke-width="1.5"/>

  <text class="mono" x="34" y="40" font-size="11.5" letter-spacing="2.2"
        fill="#D4AF37" fill-opacity="0.85">LANGUAGES / 语言构成</text>
  <text class="mono" x="966" y="40" text-anchor="end" font-size="11.5"
        fill="{MUTED}" fill-opacity="0.8">≈ {kb:,.0f} KB of code</text>

  <g clip-path="url(#track)">
    <rect x="34" y="60" width="932" height="16" fill="#12293F"/>
{chr(10).join(bars)}
  </g>

{chr(10).join(legend)}
</svg>
'''


def main() -> None:
    os.makedirs(ASSETS, exist_ok=True)
    data = collect()
    print(json.dumps({k: v for k, v in data.items() if k != "langs"}, ensure_ascii=False))
    print("langs:", sorted(data["langs"].items(), key=lambda kv: -kv[1])[:6])
    data["generated"] = dt.date.today().isoformat()

    with open(os.path.join(ASSETS, "stats.svg"), "w", encoding="utf-8") as f:
        f.write(stats_svg(data))
    with open(os.path.join(ASSETS, "langs.svg"), "w", encoding="utf-8") as f:
        f.write(langs_svg(data))
    print("updated assets/stats.svg, assets/langs.svg")


if __name__ == "__main__":
    main()
